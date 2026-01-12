
#include <esp_now.h>
#include <ESP32Servo.h>

#define THRESHOLD 700

#define SERVO_PIN1 25
#define SERVO_PIN2 26
#define SERVO_PIN3 27
#define SERVO_PIN4 13
#define SERVO_PIN5 15


Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;

typedef struct receive_signal {
  int value;
} receive_signal;

receive_signal mySignal = {0};

void onDataRecv(uint8_t *mac, uint8_t *incomingData, uint8_t len)
{
  if(len == sizeof(mySignal)) {
    memcpy(&mySignal, incomingData, sizeof(mySignal));
    Serial.println(mySignal.value);
  } else {
    Serial.println("Received data length mismatch");
  }
}

void setup() 
{
  Serial.begin(9600);
  
  servo1.attach(SERVO_PIN1);  // thumb
  servo2.attach(SERVO_PIN2);  // little
  servo3.attach(SERVO_PIN3);  // ring
  servo4.attach(SERVO_PIN4);  // middle
  servo5.attach(SERVO_PADAWiFi.mode(WIFI_STA);

  if(esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
  esp_now_register_recv_cb(onDataRecv);
  
}

void loop() 
{
  if(mySignal.value > THRESHOLD) {
    servo1.write(180);
    servo2.write(180);
    servo3.write(180);
    servo4.write(180);
    servo5.write(180);
  }
  else if(mySignal.value < THRESHOLD) {
    servo1.write(0);
    servo2.write(0);
    servo3.write(0);
    servo4.write(0);
    servo5.write(0);
  }

  delay(400);
}
