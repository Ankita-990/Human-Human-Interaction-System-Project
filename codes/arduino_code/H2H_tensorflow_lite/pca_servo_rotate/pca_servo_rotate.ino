/*
  ESP32 PCA9685 Servo Control
  esp32-pca9685.ino
  Driving multiple servo motors with ESP32 and PCA9685 PWM module
  Use I2C Bus

  DroneBot Workshop 2020
  https://dronebotworkshop.com
*/

// Include Wire Library for I2C
#include <Wire.h>
#include <WiFi.h>

// Include Adafruit PCA9685 Servo Library
#include <Adafruit_PWMServoDriver.h>

#include <esp_now.h>

#define THRESHOLD 1000

// Creat object to represent PCA9685 at default I2C address
Adafruit_PWMServoDriver pca9685 = Adafruit_PWMServoDriver(0x40);

// Define maximum and minimum number of "ticks" for the servo motors
// Range from 0 to 4095
// This determines the pulse width

#define SERVOMIN  200  // Minimum value
#define SERVOMAX  600  // Maximum value

// Define servo motor connections (expand as required)
#define SER0  0   //Servo Motor 0 on connector 0
#define SER1  1  //Servo Motor 1 on connector 1
#define SER2  2  //Servo Motor 1 on connector 2
#define SER3  3  //Servo Motor 1 on connector 3
#define SER4  4  //Servo Motor 1 on connector 4

// Variables for Servo Motor positions (expand as required)
int pwm0;
int pwm1;
int pwm2;
int pwm3;
int pwm4;

typedef struct receive_signal {
  float open;
  float closed;
} receive_signal;

receive_signal mySignal = {0};

void onDataRecv(const esp_now_recv_info *mac, const uint8_t *incomingData, int len)
{
  if(len == sizeof(mySignal)) {
    memcpy(&mySignal, incomingData, sizeof(mySignal));
    if(mySignal.closed > mySignal.open){
      Serial.println(mySignal.closed);  
    }
    else{
      Serial.println(mySignal.open);
    }
  } else {
    Serial.println("Received data length mismatch");
  }
}

void setup() {

  // Serial monitor setup
  Serial.begin(9600);

  // Initialize PCA9685
  pca9685.begin();

  // Set PWM Frequency to 50Hz
  pca9685.setPWMFreq(50);

  WiFi.mode(WIFI_STA);

  if(esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_recv_cb(onDataRecv);

}

void loop() {

  if(mySignal.closed < mySignal.open) {
    // Calculate PWM for all servos
    int pwm0 = map(180, 0, 180, SERVOMIN, SERVOMAX);
    int pwm1 = map(180, 0, 180, SERVOMIN, SERVOMAX);
    int pwm2 = map(180, 0, 180, SERVOMIN, SERVOMAX);
    int pwm3 = map(180, 0, 180, SERVOMIN, SERVOMAX);
    int pwm4 = map(180, 0, 180, SERVOMIN, SERVOMAX);
      
    // Update all servos simultaneously
    pca9685.setPWM(SER0, 180, pwm0);
    pca9685.setPWM(SER1, 180, pwm1);
    pca9685.setPWM(SER2, 180, pwm2);
    pca9685.setPWM(SER3, 180, pwm3);
    pca9685.setPWM(SER4, 180, pwm4);
  } 
  else {
    // Calculate PWM for all servos
    int pwm0 = map(0, 0, 180, SERVOMIN, SERVOMAX);
    int pwm1 = map(0, 0, 180, SERVOMIN, SERVOMAX);
    int pwm2 = map(0, 0, 180, SERVOMIN, SERVOMAX);
    int pwm3 = map(0, 0, 180, SERVOMIN, SERVOMAX);
    int pwm4 = map(0, 0, 180, SERVOMIN, SERVOMAX);
      
    // Update all servos simultaneously
    pca9685.setPWM(SER0, 0, pwm0);
    pca9685.setPWM(SER1, 0, pwm1);
    pca9685.setPWM(SER2, 0, pwm2);
    pca9685.setPWM(SER3, 0, pwm3);
    pca9685.setPWM(SER4, 0, pwm4);
  }
}