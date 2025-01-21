const int pinToMonitor = 8; // Pin to monitor
int lastState = LOW;        // Variable to store the last state of the pin

void setup() {
  pinMode(pinToMonitor, INPUT); // Set pin 7 as input
  Serial.begin(9600);          // Start serial communication
}

void loop() {
  int currentState = digitalRead(pinToMonitor); // Read the current state of pin 7

  // Detect rising edge (LOW to HIGH transition)
  if (lastState == LOW && currentState == HIGH) {
    Serial.println("Impulse detected on pin 7!");
  }

  // Update the last state
  lastState = currentState;
}
