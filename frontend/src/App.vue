<template>
  <div class="container">
    <h1>🛒 E-Commerce Trends Analyzer</h1>

    <!-- Google Trends Section -->
    <div class="card">
      <h2>1. Market Popularity (Google Trends)</h2>
      <div class="input-group">
        <input v-model="keyword" placeholder="Enter Product (e.g., iPhone, Hoodie)" />
        <button @click="fetchTrends">Analyze Trend</button>
      </div>
      <div v-if="trendImage" class="chart-container">
        <img :src="`data:image/png;base64,${trendImage}`" alt="Trend Chart" />
      </div>
    </div>

    <!-- Upload Section -->
    <div class="card">
      <h2>2. Admin: Upload Retail Data</h2>
      <p>CSV Requirements: Columns 'Date' (YYYY-MM-DD) and 'Sales' (Numeric)</p>
      <input type="file" @change="handleFileUpload" />
      <button @click="uploadFile">Upload to MongoDB</button>
      <p v-if="uploadMessage" class="success">{{ uploadMessage }}</p>
    </div>

    <!-- Prediction Section -->
    <div class="card">
      <h2>3. Sales Prediction (AI Regression)</h2>
      <button @click="fetchPrediction">Generate Forecast</button>
      <div v-if="predictImage" class="chart-container">
        <img :src="`data:image/png;base64,${predictImage}`" alt="Prediction Chart" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

// State
const keyword = ref('');
const trendImage = ref(null);
const file = ref(null);
const uploadMessage = ref('');
const predictImage = ref(null);

// 1. Fetch Trends
const fetchTrends = async () => {
  try {
    const res = await axios.post(`${API_URL}/google-trends`, { keyword: keyword.value });
    trendImage.value = res.data.image;
  } catch (err) {
    alert('Error fetching trends. Google API limits may apply.');
  }
};

// 2. Upload File
const handleFileUpload = (event) => {
  file.value = event.target.files[0];
};

const uploadFile = async () => {
  if (!file.value) return alert('Please select a file');
  const formData = new FormData();
  formData.append('file', file.value);

  try {
    const res = await axios.post(`${API_URL}/upload`, formData);
    uploadMessage.value = res.data.message;
  } catch (err) {
    alert('Upload failed');
  }
};

// 3. Fetch Prediction
const fetchPrediction = async () => {
  try {
    const res = await axios.get(`${API_URL}/predict`);
    predictImage.value = res.data.image;
  } catch (err) {
    alert('Prediction failed. Make sure data is uploaded.');
  }
};
</script>

<style scoped>
.container { font-family: sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
.card { border: 1px solid #ddd; padding: 20px; margin-bottom: 20px; border-radius: 8px; background: #f9f9f9; }
.input-group { display: flex; gap: 10px; margin-bottom: 10px; }
input { padding: 8px; border: 1px solid #ccc; border-radius: 4px; }
button { padding: 8px 16px; background: #42b883; color: white; border: none; border-radius: 4px; cursor: pointer; }
button:hover { background: #33a06f; }
.chart-container img { max-width: 100%; border: 1px solid #eee; margin-top: 10px; }
.success { color: green; font-weight: bold; }
</style>