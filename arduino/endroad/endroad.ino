void setup() {
  Serial.begin(9600);
  pinMode(2, INPUT);
  pinMode(3, INPUT);
  Serial.println("Test");
}

void loop() {
  Serial.println(String(digitalRead(2)) + String(digitalRead(3)));
}