"""
mainprog.py

This Flask web application serves as a REST API for agricultural user management and crop prediction.
It includes endpoints for user signup, login, and predicting crops based on user inputs.
The crop prediction uses a simple k-nearest neighbors (KNN) algorithm on agricultural data stored in CSV files.
"""

import os
import csv
import math
import operator
import pandas as pd
import sqlite3 as sql
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from flask import Flask, request, session, jsonify
from flask_cors import CORS

app = Flask(__name__)
# Explicitly allow requests from the frontend origin
CORS(app, supports_credentials=True, origins=["http://localhost:3000", "http://localhost:3001"])  
app.secret_key = os.urandom(12)
app.permanent_session_lifetime = timedelta(minutes=30)

# Add login required decorator
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'logged_in' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

# ---------------------
# Helper Functions
# ---------------------

def euclidean_distance(instance1, instance2, length):
    """
    Calculate the Euclidean distance between two instances.
    """
    distance = 0
    for x in range(length):
        distance += (float(instance1[x]) - float(instance2[x])) ** 2
    return math.sqrt(distance)

def get_neighbors(training_set, test_instance, k):
    """
    Find the k nearest neighbors of a test instance within the training set.
    """
    distances = []
    length = len(test_instance) - 1
    for record in training_set:
        dist = euclidean_distance(test_instance, record, length)
        distances.append((record, dist))
    distances.sort(key=operator.itemgetter(1))
    return [distances[i][0] for i in range(k)]

def get_response(neighbors):
    """
    Determine the predicted class from the nearest neighbors.
    """
    class_votes = {}
    for neighbor in neighbors:
        response = neighbor[-1]
        class_votes[response] = class_votes.get(response, 0) + 1
    sorted_votes = sorted(class_votes.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_votes[0][0]

# ---------------------
# Flask Routes
# ---------------------

@app.route('/api/register', methods=['POST'])
def add_record():
    """
    Process the signup form and add a new user record to the database.
    """
    try:
        data = request.get_json()
        nm = data.get('name')
        phonno = data.get('mobileNumber')
        email = data.get('email')
        unm = data.get('username')
        passwd = data.get('password')
        
        if not all([nm, phonno, email, unm, passwd]):
            return jsonify({'error': 'All fields are required'}), 400
            
        # Hash password before storing
        hashed_password = generate_password_hash(passwd)
        
        with sql.connect("agricultureuser.db") as con:
            cur = con.cursor()
            # Check if username already exists
            cur.execute("SELECT username FROM agriuser WHERE username = ?", (unm,))
            if cur.fetchone():
                return jsonify({'error': 'Username already exists'}), 400
                
            cur.execute(
                "INSERT INTO agriuser(name, phono, email, username, password) VALUES (?, ?, ?, ?, ?)",
                (nm, phonno, email, unm, hashed_password)
            )
            con.commit()
            return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        return jsonify({'error': f'Error in registration: {str(e)}'}), 500

@app.route('/api/login', methods=['POST'])
def login_details():
    """
    Process the login form and authenticate the user.
    """
    try:
        data = request.get_json()
        usrname = data.get('username')
        passwd = data.get('password')
        
        if not all([usrname, passwd]):
            return jsonify({'error': 'Username and password are required'}), 400
            
        with sql.connect("agricultureuser.db") as con:
            cur = con.cursor()
            cur.execute("SELECT username, password FROM agriuser WHERE username = ?", (usrname,))
            account = cur.fetchone()
            
            if account and check_password_hash(account[1], passwd):
                session.clear()
                session['logged_in'] = True
                session['username'] = usrname
                session.permanent = True
                return jsonify({'message': 'Login successful', 'username': usrname}), 200
            else:
                return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        return jsonify({'error': f'Login error: {str(e)}'}), 500

@app.route('/api/logout', methods=['POST'])
def logout():
    """
    Logout the user and clear the session.
    """
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200

@app.route('/api/predict', methods=['POST'])
@login_required
def predict_crop():
    """
    Process the crop prediction request using a simple KNN algorithm.
    """
    try:
        data = request.get_json()
        location = data.get('location')
        soil_type = data.get('soil_type')
        area_input = int(data.get('area'))
        
        if not all([location, soil_type, area_input]):
            return jsonify({'error': 'All fields are required'}), 400

        # Load data and filter based on inputs
        data_df = pd.read_csv("data/maindata.csv")
        # Make location and soil type matching case-insensitive and more flexible
        filtered_df = data_df[data_df['Location'].str.lower().str.contains(location.lower())]
        filtered_df = filtered_df[filtered_df['Soil'].str.lower().str.contains(soil_type.lower())]

        # If no matches found, return an error
        if filtered_df.empty:
            return jsonify({'error': f'No data found for location "{location}" with soil type "{soil_type}". Please check your inputs.'}), 400

        # Calculate estimated values
        res2 = filtered_df['price'] / filtered_df['yeilds']
        res3 = res2 * area_input
        res = filtered_df['yeilds'] / filtered_df['Area']
        res4 = res * area_input

        # Update CSV with calculations
        filtered_df.insert(11, "calculation", res3)
        filtered_df.insert(12, "res4", res4)
        filtered_df.to_csv('data/file.csv', index=False)

        # Prepare training data
        data_train = pd.read_csv("data/file.csv", usecols=range(13))
        crop_series = []
        for crop in data_train["Crops"]:
            # Normalize crop names if needed
            if crop in ["Coconut", "Cocoa", "Coffee", "Cardamum", "Pepper", "Arecanut", "Ginger", "Tea", "Groundnut", "Blackgram", "Cashew"]:
                crop_series.append(crop)
            else:
                crop_series.append(crop)
        data_train["Crop_val"] = crop_series
        data_train.drop(["Year", "Location", "Soil", "Irrigation", "Crops", "yeilds", "calculation", "price"], axis=1, inplace=True)
        data_train.to_csv("data/train.csv", header=False, index=False)

        # Calculate average weather values for test data
        avg_rainfall = data_train['Rainfall'].mean()
        avg_temp = data_train['Temperature'].mean()
        avg_humidity = data_train['Humidity'].mean()
        print('Rainfall avg:', "{:.2f}".format(avg_rainfall))
        print('Temperature avg:', "{:.2f}".format(avg_temp))
        print('Humidity avg:', "{:.2f}".format(avg_humidity))

        testdata = {
            'Area': area_input,
            'Rainfall': avg_rainfall,
            'Temperature': avg_temp,
            'Humidity': avg_humidity
        }
        pd.DataFrame([testdata]).to_csv('data/test.csv', header=False, index=False)

        # Helper: Load CSV as a list of lists (training and test sets)
        def load_dataset(csv_path, num_features):
            dataset = []
            with open(csv_path, 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in list(reader):  # Removed slicing to include all rows
                    # Check if row has enough elements
                    if len(row) >= num_features:
                        try:
                           for i in range(num_features):
                               # Ensure row[i] is not empty before converting to float
                               if row[i].strip():
                                   row[i] = float(row[i])
                               else:
                                   # Handle empty value - e.g., skip row or use default
                                   print(f"Warning: Empty value found in row: {row}, column: {i}. Skipping row.") 
                                   raise ValueError("Empty value") # Skip this row
                        except ValueError as ve:
                            print(f"Warning: Could not process row: {row}. Error: {ve}")
                            continue # Skip to next row if conversion fails
                        dataset.append(row)
                    else:
                         print(f"Warning: Row {row} has fewer than {num_features} features. Skipping.")        
            return dataset

        training_set = load_dataset('data/train.csv', 5)
        test_set = load_dataset('data/test.csv', 4)
        
        # Ensure test_set is not empty before proceeding
        if not test_set or not test_set[0]:
            return jsonify({'error': 'Could not prepare test data. Check input or CSV files.'}), 500
            
        if not training_set:
             return jsonify({'error': 'Could not prepare training data. Check CSV files.'}), 500

        # Apply KNN with k = 1
        k = 1
        neighbors = get_neighbors(training_set, test_set[0], k)
        response = get_response(neighbors)
        # Format the neighbor's price (assumed to be at index 4) to 2 decimal places
        res10 = ["{:.2f}".format(record[4]) for record in neighbors]
        res12 = ", ".join(res10)
        print("KNN Neighbors:", neighbors)
        print("Predicted Crop:", response)

        # Second round of KNN (if needed) using train1.csv
        data_full = pd.read_csv("data/file.csv", usecols=range(13))
        # Use .loc for safer indexing and assignment
        train1 = data_full.loc[data_full["Crops"] != response].copy()
        
        # Ensure crop_series aligns with train1 index if filtering occurred
        # Recreating crop_series based on the filtered train1 might be safer if needed
        # For now, assume crop_series was based on data_train and use indices accordingly
        # Safely assign 'Crop_val' based on potentially reduced train1 DataFrame
        if not train1.empty:
            # Re-calculate or align crop_series if necessary. Example: Assume indices match
            # This part might need adjustment depending on how crop_series relates to data_full
            aligned_crop_series = [cs for i, cs in enumerate(crop_series) if i in train1.index]
            train1.loc[:, "Crop_val"] = aligned_crop_series[:len(train1)] # Use aligned series
            
            train1.drop(["Year", "Location", "Soil", "Irrigation", "Crops", "yeilds", "calculation", "price"], axis=1, inplace=True)
            train1.to_csv("data/train1.csv", header=False, index=False)

            training_set_2 = load_dataset('data/train1.csv', 5)
            test_set_2 = load_dataset('data/test.csv', 4) # Reload test set just in case
            
            if training_set_2 and test_set_2 and test_set_2[0]:
                neighbors_2 = get_neighbors(training_set_2, test_set_2[0], k)
                response2 = get_response(neighbors_2)
                res11 = ["{:.2f}".format(record[4]) for record in neighbors_2]
                res13 = ", ".join(res11)
                print("Second KNN Neighbors:", neighbors_2)
                print("Second Predicted Crop:", response2)
            else:
                response2 = "N/A"
                res13 = "N/A"
                print("Could not perform second KNN prediction.")
        else:
             response2 = "N/A" # No alternative if train1 is empty
             res13 = "N/A"
             print("No alternative crops found for second KNN prediction.")

        # Return prediction results in JSON format
        return jsonify({
            'prediction': response,
            'price': res12,
            'prediction1': response2,
            'price1': res13
        }), 200
        
    except FileNotFoundError as fnf_error:
        print(f"Error: Data file not found - {fnf_error}")
        return jsonify({'error': f'Data file not found: {fnf_error.filename}. Please ensure data files are present.'}), 500
    except pd.errors.EmptyDataError as ede:
        print(f"Error: Empty data file - {ede}")
        return jsonify({'error': f'Data file is empty: {ede}. Please check the CSV files.'}), 500
    except KeyError as ke:
         print(f"Error: Missing column in CSV - {ke}")
         return jsonify({'error': f'Missing expected column in data file: {ke}. Please check CSV headers.'}), 500
    except Exception as e:
        print(f"Prediction error: {str(e)}") # Log the full error
        return jsonify({'error': f'Prediction error: {str(e)}'}), 500

@app.route('/api/user', methods=['GET'])
@login_required
def get_user():
    """
    Get current user information.
    """
    return jsonify({
        'username': session.get('username'),
        'logged_in': session.get('logged_in', False)
    }), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)
