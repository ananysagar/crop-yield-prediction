"""
mainprog.py

This Flask web application serves a website for agricultural user management and crop prediction.
It includes routes for user signup, login, and predicting crops based on user inputs.
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
from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.urandom(12)
app.permanent_session_lifetime = timedelta(minutes=30)

# Add login required decorator
def login_required(f):
    def wrapper(*args, **kwargs):
        if 'logged_in' not in session:
            return redirect(url_for('user_login'))
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

@app.route('/')
def home():
    """Render the landing page."""
    return render_template('index.html')

@app.route('/home')
@login_required
def homepage():
    """Render the homepage."""
    return render_template('home.html')

@app.route('/services')
@login_required
def service_page():
    """Render the services page."""
    return render_template('services.html')

@app.route('/coconut')
def coconut_page():
    """Render the Coconut page."""
    return render_template('coconut.html')

@app.route('/cocoa')
def cocoa_page():
    """Render the Cocoa page."""
    return render_template('cocoa.html')

@app.route('/arecanut')
def arecanut_page():
    """Render the Arecanut page."""
    return render_template('arecanut.html')

@app.route('/paddy')
def paddy_page():
    """Render the Paddy page."""
    return render_template('paddy.html')

@app.route('/coffee')
def coffee_page():
    """Render the Coffee page."""
    return render_template('coffee.html')

@app.route('/cardamum')
def cardamum_page():
    """Render the Cardamum page."""
    return render_template('cardamum.html')

@app.route('/ginger')
def ginger_page():
    """Render the Ginger page."""
    return render_template('ginger.html')

@app.route('/tea')
def tea_page():
    """Render the Tea page."""
    return render_template('tea.html')

@app.route('/groundnut')
def groundnut_page():
    """Render the Groundnut page."""
    return render_template('groundnut.html')

@app.route('/blackgram')
def blackgram_page():
    """Render the Blackgram page."""
    return render_template('blackgram.html')

@app.route('/cashew')
def cashew_page():
    """Render the Cashew page."""
    return render_template('cashew.html')

@app.route('/about')
def about_page():
    """Render the About page."""
    return render_template('about.html')

@app.route('/signup')
def new_user():
    """Render the user signup page."""
    return render_template('signup.html')

@app.route('/register', methods=['POST', 'GET'])
def add_record():
    """
    Process the signup form and add a new user record to the database.
    """
    msg = ""
    if request.method == 'POST':
        try:
            nm = request.form['Name']
            phonno = request.form['MobileNumber']
            email = request.form['email']
            unm = request.form['Username']
            passwd = request.form['password']
            
            # Hash password before storing
            hashed_password = generate_password_hash(passwd)
            
            with sql.connect("agricultureuser.db") as con:
                cur = con.cursor()
                # Check if username already exists
                cur.execute("SELECT username FROM agriuser WHERE username = ?", (unm,))
                if cur.fetchone():
                    msg = "Username already exists"
                    return render_template("signup.html", error=msg)
                    
                cur.execute(
                    "INSERT INTO agriuser(name, phono, email, username, password) VALUES (?, ?, ?, ?, ?)",
                    (nm, phonno, email, unm, hashed_password)
                )
                con.commit()
                msg = "Record successfully added"
        except Exception as e:
            con.rollback()
            msg = f"Error in insert operation: {e}"
        finally:
            return render_template("result.html", msg=msg)

@app.route('/login')
def user_login():
    """Render the login page."""
    return render_template("login.html")

@app.route('/login-details', methods=['POST', 'GET'])
def login_details():
    """
    Process the login form and authenticate the user.
    If credentials are valid, redirect to the homepage.
    """
    if request.method == 'POST':
        usrname = request.form['username']
        passwd = request.form['password']
        
        with sql.connect("agricultureuser.db") as con:
            cur = con.cursor()
            cur.execute("SELECT username, password FROM agriuser WHERE username = ?", (usrname,))
            account = cur.fetchone()
            
            if account and check_password_hash(account[1], passwd):
                # Create new session
                session.clear()
                session['logged_in'] = True
                session['username'] = usrname
                session.permanent = True
                return redirect(url_for('homepage'))
            else:
                return render_template('errlogin.html')
                
    return render_template('login.html')

@app.route('/predict-info')
@login_required
def predict_info():
    """Render the crop prediction input page."""
    return render_template('info.html')

@app.route('/predict', methods=['POST', 'GET'])
@login_required
def predict_crop():
    """
    Process the crop prediction request using a simple KNN algorithm.
    The function:
    - Reads input values from the form.
    - Filters and processes agricultural data from CSV files.
    - Computes price and yield estimations.
    - Applies KNN to suggest crops.
    - Renders the prediction result page.
    """
    if request.method == 'POST':
        # Retrieve user inputs
        location = request.form['comment']
        soil_type = request.form['comment1']
        area_input = int(request.form['comment2'])
        print("Location:", location)
        print("Soil Type:", soil_type)
        print("Area:", area_input)

        # Load data and filter based on inputs
        data_df = pd.read_csv("data/maindata.csv")
        filtered_df = data_df[data_df['Location'].str.contains(location)]
        filtered_df = filtered_df[filtered_df['Soil'].str.contains(soil_type)]

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
        data = pd.read_csv("data/file.csv", usecols=range(13))
        crop_series = []
        for crop in data["Crops"]:
            # Normalize crop names if needed
            if crop in ["Coconut", "Cocoa", "Coffee", "Cardamum", "Pepper", "Arecanut", "Ginger", "Tea", "Groundnut", "Blackgram", "Cashew"]:
                crop_series.append(crop)
            else:
                crop_series.append(crop)
        data["Crop_val"] = crop_series
        data.drop(["Year", "Location", "Soil", "Irrigation", "Crops", "yeilds", "calculation", "price"], axis=1, inplace=True)
        data.to_csv("data/train.csv", header=False, index=False)

        # Calculate average weather values for test data
        avg_rainfall = data['Rainfall'].mean()
        avg_temp = data['Temperature'].mean()
        avg_humidity = data['Humidity'].mean()
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
                    for i in range(num_features):
                        row[i] = float(row[i])
                    dataset.append(row)
            return dataset

        training_set = load_dataset('data/train.csv', 5)
        test_set = load_dataset('data/test.csv', 4)
        print("Training set:", training_set)
        print("Test set:", test_set)

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
        train1 = data_full[data_full["Crops"] != response]
        train1["Crop_val"] = crop_series[:len(train1)]
        train1.drop(["Year", "Location", "Soil", "Irrigation", "Crops", "yeilds", "calculation", "price"], axis=1, inplace=True)
        train1.to_csv("data/train1.csv", header=False, index=False)

        training_set_2 = load_dataset('data/train1.csv', 5)
        test_set = load_dataset('data/test.csv', 4)
        neighbors_2 = get_neighbors(training_set_2, test_set[0], k)
        response2 = get_response(neighbors_2)
        res11 = ["{:.2f}".format(record[4]) for record in neighbors_2]
        res13 = ", ".join(res11)
        print("Second KNN Neighbors:", neighbors_2)
        print("Second Predicted Crop:", response2)

        return render_template('resultpred.html', prediction=response, price=res12,
                            prediction1=response2, price1=res13,
                            comment=location, comment1=soil_type, comment2=area_input)
    return render_template('info.html')

@app.route('/logout')
def logout():
    """
    Log out the user by clearing the session.
    """
    # Clear the entire session
    session.clear()
    return redirect(url_for('home'))

# Add a special route to handle case insensitive crop names
@app.route('/<crop_name>')
def crop_page_handler(crop_name):
    """
    Handle crop page requests with case-insensitive matching.
    This ensures links like /coconut or /Coconut both work.
    """
    crop_routes = {
        'coconut': 'coconut_page',
        'cocoa': 'cocoa_page',
        'coffee': 'coffee_page',
        'cardamum': 'cardamum_page',
        'pepper': 'pepper_page',
        'arecanut': 'arecanut_page',
        'ginger': 'ginger_page',
        'tea': 'tea_page',
        'groundnut': 'groundnut_page',
        'blackgram': 'blackgram_page',
        'cashew': 'cashew_page',
        'paddy': 'paddy_page'
    }
    
    # Normalize the crop name to lowercase
    crop_name_lower = crop_name.lower()
    
    # Check if we have a route for this crop
    if crop_name_lower in crop_routes:
        # Call the appropriate route handler function
        return globals()[crop_routes[crop_name_lower]]()
    
    # If no matching crop, return 404
    return render_template('error.html', message=f"Crop '{crop_name}' not found"), 404

if __name__ == '__main__':
    app.run(debug=True)
