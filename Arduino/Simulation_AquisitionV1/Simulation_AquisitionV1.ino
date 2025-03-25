#include <Arduino.h>

// ----- PIN ASSIGNMENTS for the Simulation (Arduino Mega) -----
// These pins must be wired to the corresponding controller pins.
const byte SIM_CLOCK_PIN = 2;    // Controller CLOCK (pin 7) → SIM_CLOCK_PIN
const byte SIM_SEL_UN_PIN = 3;   // Controller SC_SEL_UN (pin 11) → SIM_SEL_UN_PIN
const byte SIM_SC_IN_PIN = 4;    // Controller SC_IN (pin 8) → SIM_SC_IN_PIN
const byte SIM_SC_OUT_PIN = 5;   // SIM_SC_OUT will drive Controller SC_OUT (pin 9)
const byte SIM_SA_PIN = 18;      // Controller SA (pin A1) → SIM_SA_PIN

// ----- Parameters for Scan Chain (Write Capture) -----
const int TOTAL_CLOCKS = 128;    // Total clock pulses for a complete scan chain write cycle
const int TOTAL_COLUMNS = 16;    // Number of columns (each column is 8 bits)

// ----- Global Variables for Write Capture -----
volatile bool scanActive = false;        // True when a write (scan) cycle is in progress
volatile int clockCount = 0;             // Counts clock pulses during a write cycle
volatile byte scanData[TOTAL_CLOCKS];    // Buffer to store captured scan-chain bits
volatile bool scanDone = false;          // Set when a complete scan cycle has been captured
byte storedColumns[TOTAL_COLUMNS];       // Last stored (raw/inverted) 8-bit value for each column

// ----- Global Variables for Read Operation -----
volatile bool readActive = false;  // True when a read cycle is active
volatile int readBitCount = 0;     // Number of bits output so far in the read cycle
byte readValue = 0;                // The computed 8-bit value (after conversion) to output
const int readColumn = 1;          // Fixed column number to read (change if needed)

// ----- Debug Flags (set in ISRs, printed in loop) -----
volatile bool debugWriteTriggered = false;
volatile bool debugReadTriggered = false;

// ----- Interrupt Service Routines -----
// ISR for SC_SEL_UN rising edge: triggers write capture
void selUnISR() {
  // Only start a new scan if one is not already in progress.
  if (!scanActive) {
    scanActive = true;
    clockCount = 0;
    scanDone = false;
    debugWriteTriggered = true; // Flag for debug message in loop()
  }
}

// ISR for the clock: used for both write capture and read output.
// This ISR is called on each rising edge of the clock signal.
void clockISR() {
  // If a read cycle is active, output one bit (LSB first) on SIM_SC_OUT_PIN.
  if (readActive) {
    int bitVal = (readValue >> readBitCount) & 0x01;
    digitalWrite(SIM_SC_OUT_PIN, bitVal ? HIGH : LOW);
    readBitCount++;
    if (readBitCount >= 8) {
      readActive = false;
      // Optionally clear the stored value for the read column.
      storedColumns[readColumn - 1] = 0;
      digitalWrite(SIM_SC_OUT_PIN, LOW);
    }
    return; // Exit ISR so we don’t process write-capture on this clock pulse.
  }
  
  // If a write capture cycle is active, capture the bit from SIM_SC_IN_PIN.
  if (scanActive && clockCount < TOTAL_CLOCKS) {
    byte bitVal = digitalRead(SIM_SC_IN_PIN);
    scanData[clockCount] = bitVal;
    clockCount++;
    if (clockCount >= TOTAL_CLOCKS) {
      scanActive = false;
      scanDone = true;
    }
  }
}

// ISR for SA rising edge: triggers a read cycle.
void readTriggerISR() {
  if (!readActive) {
    readActive = true;
    readBitCount = 0;
    // Compute the "real" value from the stored raw data using your inversion logic.
    readValue = 255 - storedColumns[readColumn - 1];
    debugReadTriggered = true; // Set flag for debug printing in loop()
  }
}

// Helper function to decode the 128-bit scan data into 16 columns (8 bits each).
void decodeScanData() {
  for (int col = 0; col < TOTAL_COLUMNS; col++) {
    int startIndex = col * 8;
    byte newVal = 0;
    for (int bit = 0; bit < 8; bit++) {
      int idx = startIndex + bit;
      byte rawBit = (scanData[idx] == HIGH) ? 1 : 0;
      newVal |= (rawBit << bit);
    }
    storedColumns[col] = newVal;
  }
}

void setup() {
  Serial.begin(2000000);
  Serial.println("=== Simulation Debug Start ===");

  // Initialize stored columns to zero.
  for (int i = 0; i < TOTAL_COLUMNS; i++) {
    storedColumns[i] = 0;
  }
  
  // Set pin modes.
  pinMode(SIM_CLOCK_PIN, INPUT);
  pinMode(SIM_SEL_UN_PIN, INPUT);
  pinMode(SIM_SC_IN_PIN, INPUT);
  pinMode(SIM_SC_OUT_PIN, OUTPUT);
  digitalWrite(SIM_SC_OUT_PIN, LOW);
  pinMode(SIM_SA_PIN, INPUT);
  
  // Attach interrupts.
  attachInterrupt(digitalPinToInterrupt(SIM_SEL_UN_PIN), selUnISR, RISING);
  attachInterrupt(digitalPinToInterrupt(SIM_CLOCK_PIN), clockISR, RISING);
  attachInterrupt(digitalPinToInterrupt(SIM_SA_PIN), readTriggerISR, RISING);
  
  Serial.println("Setup complete. Waiting for signals...");
}

void loop() {
  // If a write scan has been captured, decode it and print the stored columns.
  if (scanDone) {
    decodeScanData();
    Serial.println("\n--- Write scan captured ---");
    Serial.print("Stored columns (raw values): ");
    for (int i = 0; i < TOTAL_COLUMNS; i++) {
      Serial.print("C");
      Serial.print(i + 1);
      Serial.print(":");
      Serial.print(storedColumns[i]);
      Serial.print("  ");
    }
    Serial.println();
    scanDone = false;
  }
  
  // Print a message if a write trigger (SC_SEL_UN rising edge) was detected.
  if (debugWriteTriggered) {
    Serial.println("Write trigger detected via SC_SEL_UN.");
    debugWriteTriggered = false;
  }
  
  // Print a message if a read trigger (SA rising edge) was detected.
  if (debugReadTriggered) {
    Serial.print("Read trigger detected via SA. ");
    Serial.print("Outputting value from column ");
    Serial.print(readColumn);
    Serial.print(" => raw: ");
    Serial.print(storedColumns[readColumn - 1]);
    Serial.print(", real: ");
    Serial.println(readValue);
    debugReadTriggered = false;
  }
  
  // Every second, print the current state of SA and SC_SEL_UN for additional debugging.
  static unsigned long lastPrint = 0;
  if (millis() - lastPrint > 1000) {
    lastPrint = millis();
    int saState = digitalRead(SIM_SA_PIN);
    int selUnState = digitalRead(SIM_SEL_UN_PIN);
    /*Serial.print("DEBUG: SA state = ");
    Serial.print(saState);
    Serial.print(" | SC_SEL_UN state = ");
    Serial.println(selUnState);*/
  }
  
  delay(10); // Small delay to reduce Serial spam.
}
