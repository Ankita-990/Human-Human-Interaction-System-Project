# -*- coding: utf-8 -*-
"""
Created on Tue Apr 29 08:30:53 2025

@author: USER8
"""

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import serial
import csv
import time
from keras import Sequential
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from keras.models import model_from_json
import pickle

esp_port = 'COM6'
baud = 9600
fileName = r"E:\ankita\ankita_giroti_project_files\dataset\real_time_emg_data_collection_with_ann.csv"

# Load model from disk using pickle
with open("model_pkl", "rb") as f:
    model = pickle.load(f)


ser = serial.Serial(esp_port, baud)
print("Connected to ESP32 at port " + esp_port)

sample = 7000
line = 0

prompt = input("Start collecting data (y/n): ")

if prompt == 'y':
    print("Wait for 1 second....")
    time.sleep(1)
    print("Start collecting EMG data")
    
    # To print data with label and status
    with open(fileName, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["EMG Value", "Status"])
        
        while line < sample:
            raw_data = ser.readline()
            data_str = raw_data.decode('utf-8').strip()
            
            scaler = MinMaxScaler()
            # X = data_str.to_frame()
            X = scaler.fit_transform(data_str)
            
            # Split "value,status" format
            if ',' in data_str:
                value, status = data_str.split(',', 1)
                # print(value + ',' + status)
                # print()
                writer.writerow([value, status])
                y_pred = model.predict(value)
                y_pred = y_pred.round()
                y_pred = y_pred.reshape(len(y_pred))
                print(y_pred)
                line += 1
    
    
    # # To print data without label and sensor
    # # Open CSV file in append mode to avoid overwriting previous data
    # with open(fileName, 'w', newline='') as csvfile:
    #     writer = csv.writer(csvfile)
    #     value = writer.writerow("EMG Value")

    #     while line < sample:
    #         getData = ser.readline()
    #         dataString = getData.decode('utf-8').strip()  # Decode and strip whitespace/newlines
            
    #         # Convert reading into a list before writing it to CSV
    #         reading = [dataString]
    #         print(reading)
    #         writer.writerow(reading)  # Write as a new row
            
    #         line += 1
            
    #     print("Data Collection Completed")
        
else:
    print("Don't have to print anything!")




# #             time.sleep(0.005)


