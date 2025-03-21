# Agriculture Crop Prediction System

A web application that helps farmers predict suitable crops based on their land conditions using machine learning. The system analyzes soil type, location, and area to suggest the most profitable crops.

## Features

- **User Management**
  - Secure signup and login
  - Password hashing
  - Session management
  - User authentication

- **Crop Prediction**
  - Location-based analysis
  - Soil type consideration
  - Area-based calculations
  - Price and yield estimates
  - Multiple crop suggestions
  - KNN-based predictions

- **Crop Information**
  - Detailed pages for major crops:
    - Coconut
    - Cocoa
    - Arecanut
    - Paddy
    - Coffee
    - Cardamum
    - Ginger
    - Tea
    - Groundnut
    - Blackgram
    - Cashew
  - Disease identification
  - Treatment recommendations
  - Prevention tips

## Tech Stack

- **Backend**: Python Flask
- **Database**: SQLite3
- **Frontend**: HTML, CSS
- **ML Algorithm**: K-Nearest Neighbors (KNN)
- **Data Processing**: Pandas

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd agriculture-crop-prediction
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Initialize the database:
```bash
python createdb.py
```

4. Start the application:
```bash
python main.py
```

The app will be available at `http://localhost:5000`

## Project Structure

```
agriculture-crop-prediction/
│
├── main.py               # Main Flask application
├── createdb.py           # Database initialization
├── requirements.txt      # Python dependencies
│
├── data/
│   ├── maindata.csv      # Training data for predictions
│   ├── file.csv          # Temporary processing file
│   ├── train.csv         # KNN training data
│   ├── train1.csv        # Secondary KNN training data
│   └── test.csv          # KNN test data
│
├── static/
│   ├── css/              # Stylesheet files
│   └── img/              # Image assets
│
└── templates/
    ├── index.html        # Landing page
    ├── login.html        # User login
    ├── signup.html       # User registration
    ├── home.html         # Dashboard
    ├── services.html     # Available services
    ├── info.html         # Prediction input
    ├── resultpred.html   # Prediction results
    ├── about.html        # About page
    ├── error.html        # Error handling
    ├── errlogin.html     # Login error
    ├── result.html       # Registration result
    │
    │ # Crop Information Pages
    ├── coconut.html      # Coconut details and diseases
    ├── cocoa.html        # Cocoa details and diseases
    ├── arecanut.html     # Arecanut details and diseases
    ├── paddy.html        # Paddy details and diseases
    ├── coffee.html       # Coffee details and diseases
    ├── cardamum.html     # Cardamum details and diseases
    ├── ginger.html       # Ginger details and diseases
    ├── tea.html          # Tea details and diseases
    ├── groundnut.html    # Groundnut details and diseases
    ├── blackgram.html    # Blackgram details and diseases
    └── cashew.html       # Cashew details and diseases
```

## How It Works

1. **User Registration & Authentication**
   - Users create an account with name, email, phone
   - Passwords are securely hashed
   - Login creates a session
   - Protected routes require authentication

2. **Crop Prediction Process**
   - User inputs:
     - Location
     - Soil type
     - Land area
   - System processes:
     - Filters relevant data
     - Calculates yield estimates
     - Determines price projections
     - Uses KNN to find similar cases
   - Outputs:
     - Primary recommended crop
     - Alternative crop suggestion
     - Expected yield
     - Estimated revenue

3. **Crop Information**
   - Each crop has a dedicated page with:
     - Common diseases and symptoms
     - Treatment recommendations
     - Prevention tips
   - Users can access these pages:
     - From the Services page
     - By clicking "View Details" in prediction results

4. **Data Processing**
   - Uses historical data of crops
   - Considers multiple parameters:
     - Rainfall
     - Temperature
     - Humidity
     - Soil conditions
   - Normalizes and processes data
   - Applies KNN algorithm

## Database Schema

```sql
CREATE TABLE agriuser (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phono TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## API Routes

- `/`: Landing page
- `/home`: User dashboard
- `/services`: Available services
- `/signup`: User registration
- `/register`: Process registration
- `/login`: User login
- `/login-details`: Process login
- `/predict-info`: Prediction input form
- `/predict`: Process prediction
- `/logout`: User logout
- `/<crop_name>`: Crop-specific information pages (case-insensitive)

## Security Features

- Password hashing using Werkzeug
- CSRF protection
- Session management
- SQL injection prevention
- Input validation
- Error handling

## Data Requirements

The system needs the following CSV files in the `data` folder:
- `maindata.csv`: Historical crop data
  - Columns: Location, Soil, Area, Rainfall, Temperature, Humidity, Crops, Yields, Price

## Error Handling

- User-friendly error messages
- Proper validation feedback
- Secure error logging
- Graceful failure handling

## Future Enhancements

- Weather API integration
- More crop varieties
- Real-time market prices