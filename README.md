## E-Commerce Trends Analyzer
**1. Project Overview**

The E-Commerce Trends Analyzer is a full-stack web application designed to help online retailers make data-driven decisions. It combines external market intelligence (Google Trends) with internal sales data (CSV/Kaggle) to visualize product popularity and forecast future sales using Machine Learning.
**2. Technical Architecture**

The application uses a Headless Architecture where the frontend and backend are decoupled, communicating via a REST API.

    Development Environment: Visual Studio Code (VSCode).

    Backend: Python (Flask) handling API requests, data processing, and ML modeling.

    Frontend: JavaScript (Vue.js 3 + Vite) for a reactive user interface.

    Database: MongoDB (NoSQL) for storing unstructured sales records.

**3. Technology Stack**
Component	Technology	Purpose
Frontend	Vue.js 3, Vite, Axios	User Interface, API communication, State management.
Backend API	Flask, Flask-Cors	REST API endpoints, routing, and request handling.
Database	MongoDB, PyMongo	Storing historical sales data uploaded by the user.
Data Processing	Pandas, NumPy	Cleaning CSV data and preparing datasets for ML.
Machine Learning	Scikit-Learn	Linear Regression model for predicting future sales.
Visualization	Matplotlib, Seaborn	Generating static charts on the server (rendered as Base64 images).
External API	Pytrends	Unofficial API to fetch real-time search interest data from Google.
**4. Key Features**
A. Real-Time Market Analysis (Google Trends)

    Function: Users enter a product keyword (e.g., "Winter Jacket").

    Process: The backend queries Google Trends for interest over the last 12 months.

    Output: A line chart displaying seasonal demand spikes and general popularity trends.

B. Admin Data Dashboard

    Function: Admin users can upload historical retail datasets (CSV format).

    Process: The system parses the CSV (using Pandas), validates columns (Date, Sales), and stores the structured data in MongoDB.

    Output: Persistent storage of sales history, replacing old data sets dynamically.

C. AI-Powered Sales Forecasting

    Function: Predicts sales performance for the upcoming 30 days.

    Process:

        Fetches historical data from MongoDB.

        Trains a Linear Regression model using Scikit-Learn.

        Extrapolates the trend line into the future.

    Output: A visualization overlaying actual historical sales (Blue) vs. predicted future sales (Red dashed line).

**5. Data Flow Diagram**

    User Action: User interacts with the Vue UI (Search, Upload, or Predict).

    API Call: Vue sends an HTTP Request (POST/GET) to the Flask Server.

    Processing:

        If Trends: Flask queries Google.

        If Upload: Flask parses CSV → Saves to MongoDB.

        If Predict: Flask loads from MongoDB → Runs Regression Model.

    Visualization: Flask generates a graph using Matplotlib → Converts it to a Base64 string.

    Response: The JSON response (containing the image string) is sent back to Vue.

    Display: Vue renders the image string as a visual chart in the browser.
<img width="1372" height="1090" alt="image" src="https://github.com/user-attachments/assets/39fb5895-08f3-4ef0-9083-91535bfcec55" />
<img width="1342" height="1073" alt="image" src="https://github.com/user-attachments/assets/e69b0d5a-7b02-4ea7-acdd-af5b15a44d57" />

