# -*- coding: utf-8 -*-
"""
Created on Wed Apr 30 16:34:03 2025

@author: USER8
"""

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import serial
import csv
import time
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import pickle



# Serial configuration
esp_port = 'COM3'
baud = 9600
fileName = "D:\\ankita\\ankita_project\\final_project_code\\datasets\\predictions1.csv"

ser = serial.Serial(esp_port, baud)
print(f"Connected to ESP32 at {esp_port}")

sample_size = 2000
current_sample = 0
correct_predictions = 0

prompt = input("Start collecting data (y/n): ")

if prompt.lower() == 'y':
    print("Initializing...")
    time.sleep(1)
    
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["EMG Value", "True Status", "Predicted Status"])
        
        while current_sample < sample_size:
            raw_data = ser.readline()
            try:
                data_str = raw_data.decode('utf-8').strip()
                if ',' not in data_str:
                    continue
                    
                value_str, true_status = data_str.split(',', 1)
                emg_value = float(value_str)
                
                # Normalization
                scaled_value = scaler.transform([[emg_value]])
                
                # Prediction
                prediction = model.predict(scaled_value)
                predicted_status = 'Close' if prediction.round().astype(int)[0] == 1 else 'Open'
                
                # Accuracy calculation
                if predicted_status == true_status.strip():
                    correct_predictions += 1
                
                # Write and display
                writer.writerow([emg_value, true_status, predicted_status])
                print(f"Value: {emg_value:.2f} | Prediction: {predicted_status}")
                
                current_sample += 1
                
            except (ValueError, UnicodeDecodeError) as e:
                continue

    # Final accuracy report
    accuracy = (correct_predictions / sample_size) * 100
    print(f"\nSystem Accuracy: {accuracy:.2f}%")
    
else:
    print("Operation cancelled.")
