
#include <esp_now.h>

#include <WiFi.h>

#define EMG_PIN 32

uint8_t sendDataToMacAddr[] = {0xE8, 0x6B, 0xEA, 0xDF, 0x4A, 0x00};

typedef struct emg_signal {
  int value;
} emg_signal;

emg_signal mySignal;

esp_now_peer_info_t peerInfo;

void onDataSend(const uint8_t *macaddr, esp_now_send_status_t sendStatus)
{
  Serial.print("Delivery Status: ");
  Serial.println(sendStatus == ESP_NOW_SEND_SUCCESS  ? "Delivery Successeful" : "Delivery Fail");
}

void setup() 
{
  Serial.begin(9600);
  WiFi.mode(WIFI_STA);

  if (esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_send_cb(onDataSend);

  memcpy(peerInfo.peer_addr, sendDataToMacAddr, 6);
  peerInfo.channel = 0;  
  peerInfo.encrypt = false;

   if (esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }
}

void loop() 
{
  mySignal.value = analogRead(EMG_PIN);
  Serial.println(mySignal.value);
  
  esp_now_send(sendDataToMacAddr, (uint8_t *) &mySignal, sizeof(mySignal));
  delay(400);
}


