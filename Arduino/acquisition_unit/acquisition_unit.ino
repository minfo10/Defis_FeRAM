/*
  Test to verify whether pin 7 on an Arduino Mega receives 130 clock pulses.
  - Captures pulses with a 10ms HIGH and 10ms LOW period.
  - Improves precision by eliminating unnecessary delays.
  - Uses `micros()` for better timing resolution.
  - Ensures accurate impulse counting.
*/

int previous_state = HIGH;  // Track previous pin state
int impulse_count = 0;      // Counter for LOW impulses
unsigned long lastChangeTime = 0;  // Time tracking for state changes

void setup() {
  Serial.begin(2000000);
  pinMode(7, INPUT_PULLUP);  // Ensures pin naturally reads HIGH if not driven LOW
}

void loop() {
  int state = digitalRead(7);
  unsigned long currentTime = micros();  // Get precise time

  // Detect rising or falling edges
  if (state != previous_state) {
    lastChangeTime = currentTime;  // Update the time of last transition
    
    if (state == LOW) {
      impulse_count++;  // Increment impulse count on LOW transition
      Serial.print("Pin 7 is LOW - Impulse #");
      Serial.println(impulse_count);
    }
    
    previous_state = state;  // Update previous state
  }

  // Stop counting once 130 pulses are detected
  if (impulse_count >= 130) {
    Serial.println("130 pulses detected. Stopping...");
    while (true);  // Stop execution
  }
}
