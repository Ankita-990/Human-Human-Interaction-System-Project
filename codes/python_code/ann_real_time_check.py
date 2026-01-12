# -*- coding: utf-8 -*-
"""
Created on Sat Apr 26 08:46:01 2025

@author: ankita
"""

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import serial
import time
import numpy as np
import pandas as pd
import datetime
import csv
import tensorflow as tf
from keras.models import model_from_json, Model, load_model
# from tensorflow.keras import Sequential

com_port = serial.Serial('COM6', 9600, timeout=1)

json_file = open(r"E:\ankita\ankita_giroti_project_files\codes\python_code\ann_model.json",'r')
loaded_model_json = json_file.read()
json_file.close()

# tf.keras.Model.load_weights(r"E:\ankita\ankita_giroti_project_files\codes\python_code\ann_model.h5")
model = load_model(r"E:\ankita\ankita_giroti_project_files\codes\python_code\ann_model.h5")
print("Loaded model from disk")

labels = ["Open", "Close"]

input_emg = []

a = input("Start collecting data(y/n)").lower()
if a=='y':
    print("Wait for 2 sec...")
    time.sleep(2)
    
    print("[START ACTION]")
    time.sleep(0.5)
    print(time.ctime())
    
    while True:
        raw_data = com_port.readline().decode('utf-8', errors='ignore').strip()
        if raw_data=='':
            continue
        try:
            sensor_data = float(raw_data)
        except ValueError:
            print("Invalid data")
            continue
                
        
        
        # create DataFrame with single value (2D array)
        df = pd.DataFrame([[sensor_data]], columns=['emgValue'], dtype=np.float32)
        
        input_data = df.values
        
        # predict
        prediction = model.predict(input_data)
        pred_class = int(prediction > 0.5)
        
        status = labels[pred_class]
        
        print(f"\rEMG: {sensor_data:6.1f} | Status: {status}", end='', flush=True)
        
com_port.close()
        
    #     # # convert to float and preprocess
    #     # for val in sensor_data:
    #     #     val = float(val)
    #     #     scaled_value = scaler.transform([[emg_value]])
    #     #     data.append(val)
            
    #     row.append = data
    #     print(x, "Data: ", data)
        
    #     df = pd.DataFrame()(row, columns=np.arange(11))
        
    #     input_emg.append(df.values)
    #     df.size
        
    #     x = x + 1
    #     c = c + 1
        
    #     if c==500:
    #         break
        
    # print(time.ctime())
    
    # else:
    #     print("OK!!")
    #     exit()
        
    # print("\nData collected\n\n")
    # print("Collected data is: \n", input_emg)
    
    # input_emg = np.array(input_emg)
    # input_emg.shape
    # # input_emg = input_emg.reshape(1, shape)
    
    # prediction = loade_model.predict(input_emg)
    # pred = list(prediction[0])
    
    # p = max(pred)
    # i = pred.index(p)
    # pred_lable = labels[i]
    
    # engine.say(pred_label)
    # engine.runAndWait()
    # print(p, i, pred_label)
