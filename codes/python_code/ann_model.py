# -*- coding: utf-8 -*-
"""
Created on Fri Apr 25 16:07:46 2025

@author: USER8
"""
import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"
import pandas as pd 
# import numpy as np
# import h5py
import tensorflow as tf
from keras import Sequential
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score
from sklearn import metrics 
import pickle
from keras.layers import Dense, Dropout
import json

data = pd.read_csv(r"E:\ankita\ankita_giroti_project_files\dataset\emg_train_status.csv")

print(f"Dataset length : {len(data)}")

X = data["EMG Value"]
y = data['Status'].map({'Open': 0, 'Close': 1})

# print(y.shape)

scaler = MinMaxScaler()
X = X.to_frame()
X = scaler.fit_transform(X)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
# print("Count y_train labels")
# print(y_train.value_counts())

# # Model training
# model = tf.keras.Sequential()
# model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

# Model training with Dense layer and dropout feature
model = tf.keras.Sequential([
    tf.keras.layers.Dense(32, input_shape=(1,)),
    Dropout(0.25),
    # Add Batch Normalization layer
    tf.keras.layers.BatchNormalization(),  
    tf.keras.layers.Activation('relu'),
    Dropout(0.5),
    tf.keras.layers.Dense(1),
    tf.keras.layers.Activation('sigmoid')
])

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
model.fit(X_train, y_train, batch_size=32, epochs=50, validation_data=(X_val, y_val))

y_pred = model.predict(X_val)
y_pred = y_pred.round()
y_pred = y_pred.reshape(len(y_pred))
print(y_pred)

# Evaluate on training data
train_loss, train_acc = model.evaluate(X_train, y_train, verbose=0)
print(f"Training Accuracy: {train_acc:.4f}")

# Evaluate on test data
loss, accuracy = model.evaluate(X_val, y_val, verbose=0)
print(f"Model Accuracy: {accuracy:.4f}")
print(f"Loss: {loss:.4f}")

print()

confusion_matrix = metrics.confusion_matrix(y_val, y_pred)
print("Confusion Matrix: ")
print(confusion_matrix)

print()

f1 = f1_score(y_val, y_pred)
print(f"F1 Score: {f1}")

# Converting to tensorflow lite model

model_converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = model_converter.convert()

# # Save to TensorFlow Lite model
open(r"E:\ankita\ankita_giroti_project_files\codes\python_code\ann_model.tflite", "wb").write(tflite_model)

# # Save model to disk using pickle
# with open("model_pkl", "wb") as f:
#     pickle.dump(model, f)
#     
# # Save the scaler for later use
# with open('scaler_pkl', 'wb') as f:
#     pickle.dump(scaler, f)

# After training the model, save architecture + weights
model_json = model.to_json()  # Convert model architecture to JSON
with open("ann_model.json", "w", encoding='utf-8') as json_file:
    json.dump(model_json, json_file, ensure_ascii=False, indent=4)
#     json_file.write(model_json)
    
model.save("ann_model.h5")  # Save weights separately
print("Saved model architecture (JSON) and weights.")
