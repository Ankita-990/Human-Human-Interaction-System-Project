# -*- coding: utf-8 -*-
"""
Created on Thu May  1 08:11:55 2025

@author: Asus
"""

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, classification_report
import pickle

# Load pre-trained components
with open("model_pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler_pkl", "rb") as f:
    scaler = pickle.load(f)

# Load new dataset (features only)
new_data = pd.read_csv("D:\\msc_rtmnu\\major_project\\final_project_code\\datasets\\emg_test.csv")
X_new = new_data[['EMG Value']]  # Maintain 2D structure

# Normalization
scaled_values = scaler.transform(X_new)

# Batch prediction
predictions = model.predict(scaled_values)
predicted_statuses = ['Close' if pred.round().astype(int)[0] == 1 else 'Open' for pred in predictions]

# Create prediction report
results = pd.DataFrame({
    'EMG_Value': new_data['EMG Value'],
    'Predicted_Status': predicted_statuses
})

print(f"Accuracy: {predictions}")

print("\nPrediction Report:")
print(results.head(20))  # Show first 20 predictions

# Save predictions
results.to_csv("emg_predictions.csv", index=False)
print("\nPredictions saved to 'emg_predictions1.csv'")

