// Sources/References consulted while writing this code:
// 1. Arduino Mega pinout documentation: https://store.arduino.cc/products/arduino-mega-2560-rev3
// 2. Arduino Reference for pinMode() and digitalRead(): https://www.arduino.cc/reference/en/

// Define the list of pins to monitor (25 pins).
// You can choose any set of 25 valid digital pins on the Mega (e.g., 2 to 26).
const int pinsToMonitor[25] = {
  2, 3, 4, 5, 6,
  7, 8, 9, 10, 11,
  12, 13, 22, 23, 24,
  25, 26, 27, 28, 29,
  30, 31, 32, 33, 34
};

// Array to store the last known state of each pin (LOW or HIGH).
int lastStates[25];

void setup() {
  Serial.begin(9600);

  // Initialize each pin as input and set the last state to whatever the pin currently reads.
  for (int i = 0; i < 25; i++) {
    pinMode(pinsToMonitor[i], INPUT);
    lastStates[i] = digitalRead(pinsToMonitor[i]);
  }
}

void loop() {
  // Check each pin for a LOW -> HIGH transition.
  for (int i = 0; i < 25; i++) {
    int currentState = digitalRead(pinsToMonitor[i]);

    // Detect rising edge
    if (lastStates[i] == LOW && currentState == HIGH) {
      Serial.print("Impulse detected on pin ");
      Serial.println(pinsToMonitor[i]);
    }

    // Update the last known state
    lastStates[i] = currentState;
  }
}
