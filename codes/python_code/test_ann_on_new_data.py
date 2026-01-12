# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 18:55:41 2025

@author: USER8
"""

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pandas as pd
from tensorflow.keras.models import load_model
from sklearn.preprocessing import MinMaxScaler
import pickle

# Load pre-trained model and scaler
with open("model_pkl", "rb") as f:
    model = pickle.load(f)
with open("scaler_pkl", "rb") as f:  # Scaler used during training
    scaler = pickle.load(f)

# Load new dataset
new_data = pd.read_csv(r"E:\ankita\ankita_giroti_project_files\dataset\emg_test.csv")

X_new = new_data['emgValue']
# emg_value = float(X_new)

 # Normalization
scaled_value = scaler.transform([[X_new]])
 
 # Prediction
prediction = model.predict(scaled_value)
predicted_status = 'Close' if prediction.round().astype(int)[0] == 1 else 'Open'
 
 # Accuracy calculation
if predicted_status == true_status.strip():
    correct_predictions += 1
     
accuracy = (correct_predictions / sample_size) * 100
print(f"\nSystem Accuracy: {accuracy:.2f}%")