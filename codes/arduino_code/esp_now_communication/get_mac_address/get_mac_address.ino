#include <WiFi.h>
#include <esp_wifi.h>

void setup(){
  Serial.begin(9600);
  delay(1000);

  Serial.print("ESP Board MAC Address: ");
  WiFi.mode(WIFI_STA);
  WiFi.begin();
  delay(100);

  uint8_t baseMac[6];
  esp_err_t ret = esp_wifi_get_mac(WIFI_IF_STA, baseMac);

  if (ret == ESP_OK) {
    Serial.printf("%02x:%02x:%02x:%02x:%02x:%02x\n",
                  baseMac[0], baseMac[1], baseMac[2],
                  baseMac[3], baseMac[4], baseMac[5]);
  } else {
    Serial.println("Failed to read MAC address");
  }
  Serial.print("ESP Board MAC Address (WiFi.macAddress): ");
  Serial.println(WiFi.macAddress());
}
 
void loop(){
  // Serial.begin(9600);
  // delay(1000);
  // WiFi.mode(WIFI_STA);
  // Serial.println(WiFi.macAddress());
}

// #include <WiFi.h>

// void setup() {
//   Serial.begin(9600);
//   delay(1000);
//   WiFi.mode(WIFI_STA);
//   Serial.println(WiFi.macAddress());
// }

// void loop() {}
