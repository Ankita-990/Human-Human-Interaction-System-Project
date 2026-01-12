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
  Serial.println(value);
  delay(200);
}