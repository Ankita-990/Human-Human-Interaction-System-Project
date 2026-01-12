int emg_pin = 32;

String emg_value = "EMG value";
String threshold = "Threshold";

void setup()
{
  Serial.begin(9600);
  pinMode(emg_pin, INPUT);
}

void loop()
{
  int value = analogRead(emg_pin);
  Serial.print(value);
  Serial.print(",");
  if(value > 1000) {
    Serial.print("Close");
  } else {
    Serial.print("Open");
  }
  Serial.println();
  // delay(100);
}