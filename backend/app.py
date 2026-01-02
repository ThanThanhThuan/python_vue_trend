import os
import io
import base64
import pandas as pd
import matplotlib
matplotlib.use('Agg') # Backend-only (no GUI)
import matplotlib.pyplot as plt
import seaborn as sns
from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from pytrends.request import TrendReq
from sklearn.linear_model import LinearRegression
import numpy as np

app = Flask(__name__)
CORS(app) # Allow Vue to talk to Flask

# MongoDB Setup
client = MongoClient('mongodb://localhost:27017/')
db = client['ecommerce_db']
sales_collection = db['sales_data']

# 1. GOOGLE TRENDS API
@app.route('/api/google-trends', methods=['POST'])
def get_trends():
    try:
        data = request.json
        keyword = data.get('keyword', 'Laptop')
        pytrends = TrendReq(hl='en-US', tz=360)
        pytrends.build_payload([keyword], timeframe='today 12-m')
        
        # Get interest over time
        df = pytrends.interest_over_time()
        if df.empty:
            return jsonify({'error': 'No data found'}), 404

        # Convert plot to Base64 image
        plt.figure(figsize=(10, 5))
        sns.lineplot(data=df, x=df.index, y=keyword)
        plt.title(f'Google Trends: {keyword}')
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        plt.close()

        return jsonify({'image': plot_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 2. UPLOAD DATASET (Kaggle CSV)
@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    try:
        df = pd.read_csv(file)
        # Simplify: Assume CSV has 'Date' and 'Sales' columns
        if 'Date' in df.columns and 'Sales' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            records = df.to_dict(orient='records')
            sales_collection.delete_many({}) # Clear old data for demo
            sales_collection.insert_many(records)
            return jsonify({'message': 'Dataset uploaded and stored in MongoDB!'})
        else:
            return jsonify({'error': 'CSV must contain Date and Sales columns'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# 3. PREDICT SALES (Regression)
@app.route('/api/predict', methods=['GET'])
def predict_sales():
    data = list(sales_collection.find({}, {'_id': 0}))
    if not data:
        return jsonify({'error': 'No data uploaded yet'}), 404
    
    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Prepare Data for Regression (Convert Date to Ordinal)
    df['DateOrdinal'] = df['Date'].map(pd.Timestamp.toordinal)
    X = df[['DateOrdinal']]
    y = df['Sales']
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next 30 days
    last_date = df['DateOrdinal'].max()
    future_dates = np.array([last_date + i for i in range(1, 31)]).reshape(-1, 1)
    predictions = model.predict(future_dates)
    
    # Visualize Historical + Prediction
    plt.figure(figsize=(10, 5))
    plt.scatter(df['Date'], df['Sales'], color='blue', label='Actual')
    future_dates_dt = [pd.Timestamp.fromordinal(int(d[0])) for d in future_dates]
    plt.plot(future_dates_dt, predictions, color='red', linestyle='--', label='Forecast')
    plt.legend()
    plt.title("Sales Forecast (Linear Regression)")
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return jsonify({'image': plot_url})

if __name__ == '__main__':
    app.run(debug=True, port=5000)