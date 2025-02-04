const int CLOCK_PIN = 7;      // Clock pin for synchronization

// List of monitored pins (example: pins 2–13, 22–34)
const uint8_t monitoredPins[] = {2,3,4,5,6,7,8,9,10,11,12,13,22,23,24,25,26,27,28,29,30,31,32,33,34};

// Ports to read (PORTD, PORTB, PORTL for Arduino Mega)
volatile uint8_t* ports[] = { &PIND, &PINB, &PINL };

void setup() {
  Serial.begin(115200);
  pinMode(CLOCK_PIN, INPUT);
  
  // Set all monitored pins as INPUT_PULLUP
  for (uint8_t i = 0; i < sizeof(monitoredPins)/sizeof(monitoredPins[0]); i++) {
    pinMode(monitoredPins[i], INPUT_PULLUP);
  }
  
}

void loop() {
  static int lastClockState = LOW;
  int currentClockState = digitalRead(CLOCK_PIN);

  // Detect rising edge of the clock signal
  if (lastClockState == LOW && currentClockState == HIGH) {
    // Read all port registers at once
    uint8_t portD = PIND; // Pins 0–7 (but avoid 0/1 for Serial)
    uint8_t portB = PINB; // Pins 8–13
    uint8_t portL = PINL; // Pins 22–37

    // Print timestamp
    Serial.print(millis());
    Serial.println(":");

    // Loop through monitored pins and read their state from the port registers
    for (uint8_t i = 0; i < sizeof(monitoredPins)/sizeof(monitoredPins[0]); i++) {
      uint8_t pin = monitoredPins[i];
      uint8_t state;
      const char* portName;

      // Determine which port the pin belongs to and read its state
      if (pin >= 2 && pin <= 7) {         // PORTD (pins 2–7)
        state = (portD & (1 << (pin - 2))) ? HIGH : LOW;
        portName = "PORTD";
      } else if (pin >= 8 && pin <= 13) { // PORTB (pins 8–13)
        state = (portB & (1 << (pin - 8))) ? HIGH : LOW;
        portName = "PORTB";
      } else if (pin >= 22 && pin <= 37) {// PORTL (pins 22–37)
        state = (portL & (1 << (pin - 22))) ? HIGH : LOW;
        portName = "PORTL";
      } else {
        state = LOW; // Default if pin is not in monitored range
        portName = "UNKNOWN";
      }

      // Print port, pin, and state
      Serial.print(portName);
      Serial.print(" Pin ");
      Serial.print(pin);
      Serial.print(": ");
      Serial.println(state == HIGH ? "HIGH" : "LOW");
    }

    Serial.println(); // Add a blank line for readability
  }

  lastClockState = currentClockState;
}
