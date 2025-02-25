#include <Arduino.h>

// ----- READER PIN ASSIGNMENTS for Arduino Mega -----
const byte READER_CLOCK_PIN    = 2; // Use digital pin 2 (supports interrupt on Mega)
const byte READER_SEL_UN_PIN   = 3; // Use digital pin 3 (supports interrupt on Mega)
const byte READER_SC_IN_PIN    = 4; // Regular digital input pin

const int TOTAL_CLOCKS = 128;  // Total clock cycles in the scan chain

// Volatile variables used in interrupts:
volatile bool scanActive = false;      // Flag to indicate a column write scan has begun.
volatile int clockCount = 0;           // Count of clock pulses captured.
volatile byte scanData[TOTAL_CLOCKS];  // Array to store the SC_IN value at each clock.
volatile bool scanDone = false;        // True when 128 bits have been captured.

// ISR: Triggered when the writer asserts SC_SEL_UN (indicating start of column write)
void selUnISR() {
  if (!scanActive) {
    scanActive = true;
    clockCount = 0;
    scanDone = false;
  }
}

// ISR: Triggered on each rising edge of the CLOCK signal.
void clockISR() {
  if (scanActive && (clockCount < TOTAL_CLOCKS)) {
    byte bitVal = digitalRead(READER_SC_IN_PIN);
    scanData[clockCount] = bitVal;
    clockCount++;
    if (clockCount >= TOTAL_CLOCKS) {
      scanActive = false;
      scanDone = true;
    }
  }
}

void setup() {
  Serial.begin(2000000);
  Serial.println("=== FeRAM Control Bus Sniffer (Mega) Starting ===");
  
  // Set up the reader pins:
  pinMode(READER_CLOCK_PIN, INPUT);
  pinMode(READER_SEL_UN_PIN, INPUT);
  pinMode(READER_SC_IN_PIN, INPUT);
  
  // Attach interrupts:
  // For rising edge on SC_SEL_UN (to start a new scan)
  attachInterrupt(digitalPinToInterrupt(READER_SEL_UN_PIN), selUnISR, RISING);
  // For rising edge on CLOCK (to sample SC_IN)
  attachInterrupt(digitalPinToInterrupt(READER_CLOCK_PIN), clockISR, RISING);
  
  Serial.println("Sniffer ready. Awaiting a write operation on the writer Arduino...");
}

void loop() {
  if (scanDone) {
    Serial.println("\n--- Complete scan captured (128 bits) ---");
    
    // (Optional) Uncomment to print all 128 bits for debugging:
    
    Serial.print("Scanned data: ");
    for (int i = 0; i < TOTAL_CLOCKS; i++) {
      Serial.print(scanData[i] ? "1" : "0");
      if ((i + 1) % 8 == 0) Serial.print(" ");
    }
    Serial.println();
    
    
    Serial.println("Enter the column number (1-16) to decode:");
    while (!Serial.available()) {
      ; // Wait for user input.
    }
    String colInput = Serial.readStringUntil('\n');
    colInput.trim();
    int col = colInput.toInt();
    if (col < 1 || col > 16) {
      Serial.println("Invalid column number. Please try again.");
    } else {
      int startIndex = (col - 1) * 8;
      byte value = 0;
      // Bits are transmitted LSB first.
      for (int bit = 0; bit < 8; bit++) {
        int index = startIndex + bit;
        // In your control code, a written '0' drives SC_IN HIGH and a written '1' drives it LOW.
        // Invert the sampled bit to recover the original bit.
        byte recoveredBit = (scanData[index] == HIGH) ? 0 : 1;
        value |= (recoveredBit << bit);
      }
      Serial.print("Decoded value for column ");
      Serial.print(col);
      Serial.print(": ");
      Serial.print(value);
      Serial.print(" (0x");
      if (value < 16) Serial.print("0");
      Serial.print(value, HEX);
      Serial.println(")");
    }
    
    // Reset for the next scan.
    scanDone = false;
    Serial.println("\nWaiting for a new write operation...");
  }
}
