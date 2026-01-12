#include <esp_now.h>
#include <WiFi.h>

#include "tensorflow/lite/micro/micro_mutable_op_resolver.h"
#include "tensorflow/lite/micro/micro_interpreter.h"
#include "tensorflow/lite/micro/system_setup.h"
#include "tensorflow/lite/schema/schema_generated.h"

#include "model.h"

namespace {
  const tflite::Model *model = tflite::GetModel(g_model);
  // static tflite::MicroInterpreter static_interpreter(model, resolver, tensor_arena, kTensorArenaSize);
  tflite::MicroInterpreter *interpreter;
  TfLiteTensor *input;
  TfLiteTensor *output;
  int inference_count = 0;
  const int kInferencesPerCycle = 20;

  constexpr int kTensorArenaSize = 1000;
  uint8_t tensor_arena[kTensorArenaSize];
}

// 7C:9E:BD:E3:A6:BC
// E8:6B:EA:DF:4A:00
uint8_t sendDataToMacAddr[] = {0x7C, 0x9E, 0xBD, 0xE3, 0xA6, 0XBC};

typedef struct emg_signal {
  float open;
  float closed;
} emg_signal;

emg_signal mySignal;
esp_now_peer_info_t peerInfo;

void onDataSend(const uint8_t *macaddr, esp_now_send_status_t sendStatus) {
  Serial.print("Delivery Status: ");
  Serial.println(sendStatus == ESP_NOW_SEND_SUCCESS ? "Delivery Successful" : "Delivery Fail");
}

void setup() {

  Serial.begin(9600);
  WiFi.mode(WIFI_STA);

  if(esp_now_init() != 0) {
    Serial.println("Error initializing ESP-NOW");
    return;
  }

  esp_now_register_send_cb(onDataSend);

  memcpy(peerInfo.peer_addr, sendDataToMacAddr, 6);
  peerInfo.channel = 0;
  peerInfo.encrypt = false;

  if(esp_now_add_peer(&peerInfo) != ESP_OK) {
    Serial.println("Failed to add peer");
    return;
  }
  
  pinMode(2, OUTPUT);

  // model mapping
  // model = tflite::GetModel(g_model);
  if(model->version() != TFLITE_SCHEMA_VERSION) {
    MicroPrintf(
        "model provided is schema version %d not equal to supported "
        "version %d.",
        model->version(), TFLITE_SCHEMA_VERSION
      );
      return;
  }

  // Add op resolver for tflite
  static tflite::MicroMutableOpResolver<2> resolver;
  if (resolver.AddFullyConnected() != kTfLiteOk) {
    MicroPrintf("Failed to add Fully Connected op");
    return;
  }
  if (resolver.AddLogistic() != kTfLiteOk) {
    MicroPrintf("Failed to add Logistic op");
    return;
  }
  resolver.AddFullyConnected();
  resolver.AddLogistic();

  // Build interpreter and run model
  static tflite::MicroInterpreter static_interpreter(model, resolver, tensor_arena, kTensorArenaSize);
  interpreter = &static_interpreter;

  // Allocate memory from the tensor_arena for the model's tensors.
  TfLiteStatus allocate_status = interpreter->AllocateTensors();
  if (allocate_status != kTfLiteOk) {
    MicroPrintf("AllocateTensors() failed");
    return;
  }

  // Obtain pointers to the model's input and output tensors.
  input = interpreter->input(0);
  output = interpreter->output(0);

  // Keep track of how many inferences we have performed.
  inference_count = 0;  

}

void loop() {
  
  // Raw EMG sensor values
  int emg_raw = analogRead(32);
  // Serial.println(mySignal.value);

  // Normalize the raw EMG data
  float emg_normalized = (float) emg_raw / 4096.0;

  // Model input
  input -> data.f[0] = emg_normalized;

  // run inferences, and report the error (if exist)
  TfLiteStatus invoke_status = interpreter -> Invoke();
  if(invoke_status != kTfLiteOk) {
    MicroPrintf("Invoke failed \n");
    return;
  }



  mySignal.open = output -> data.f[0];
  mySignal.closed = output -> data.f[1];

  Serial.print("Open: \t");
  Serial.print(mySignal.open);
  Serial.println();
  Serial.print("Closed: ");
  Serial.print(mySignal.closed);
  Serial.println();

  // esp_now_send(sendDataToMacAddr, (uint8_t *) &mySignal, sizeof(mySignal));
  esp_now_send(sendDataToMacAddr, (uint8_t *) &mySignal, sizeof(mySignal));
  delay(100);

  // increment thte inference count
  inference_count += 1;

  // reset the count if it reached the total number per cycle
  if(inference_count >= kInferencesPerCycle) {
    inference_count = 0;
  }
}












