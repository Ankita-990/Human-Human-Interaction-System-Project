# Design and Study of Human-Hand Interaction System to Control Movements of Paralyzed Hands
Stroke, a life-threatening condition caused by the death of brain cells, often results in paralysis, affecting many people physically and emotionally. The loss of hand function can significantly hinder daily activities. The rehabilitation system is design to assist patients to regain their muscle strength and improve their ability to perform daily task by activating their lost motor function.

![system_design](https://github.com/user-attachments/assets/36e859de-9743-4297-b989-040210a47f5a)

## Project Phase
The system consists of three primary phase: 
  1. The sensor phase utilizes an electromyography (EMG) sensor connected to a microcontroller on the unaffected hand to capture muscle activity
  2. The actuator phase employs servo motors and a microcontroller to control the movements of the paralyzed hand
  3. Machine Learning deployment on microcontroller

## Dataset
The dataset is collected using EMG Sensor to detect the hand movements of a well-lit person, which is used to train the model and understand the movements of a non-paralyzed hand. The dataset is collected for open and close hand gestures and saved into CSV file.

## Hardware
•	The system uses two ESP32 microcontroller communicating via an ESP NOW protocol

•	An EMG Sensor to collect data from non-paralyzed hand

•	Servo motors attach to every finger via strings to control hand movements

•	Adafruit PCA9685 Servo Driver for better motor control

## Machine Learning Approach
An Artificial Neural Network (ANN) is used to classify hand gestures and then send the results to the microcontroller operating the servo motor. Tensorflow Lite module in used to communicate ANN model with C programming of ESP32.

## Conclusion
In this research work, a basic prototype of a rehabilitation system is designed and developed for a patient suffering from hand paralysis. This system will help them to regain their motor functions by practicing daily exercises conducted by doctor remotely. The system is designed in such a way, so that doctor can assist the patient from a long distance. Further enhancements can be made by collecting more data including paralyzed hand using EMG sensor.
