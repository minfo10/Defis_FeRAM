/*
  Fast Acquisition of 13 Signals Using Direct Port Manipulation

  This code uses direct register access to rapidly read 13 signals.
  Each signal is monitored for transitions to LOW (assumed to be pulses).
  When a LOW pulse is detected, the code logs:
    - The pin number
    - The pulse (impulse) count for that pin
    - The precise time (in microseconds) when the pulse occurred

  For best performance:
    - Arrange your hardware so that as many signals as possible share the same port.
    - Consider buffering the pulse data instead of printing to Serial in real time.
*/

struct Signal {
  uint8_t pin;                  // Arduino digital pin number
  volatile uint8_t *pinReg;     // Pointer to the port input register for this pin
  uint8_t bitMask;              // Bit mask for this pin in the port
  uint8_t lastState;            // Last known state (HIGH or LOW)
  uint32_t impulseCount;        // Number of detected LOW pulses
};

#define NUM_SIGNALS 13

// Define your 13 signals. Adjust the pin numbers as needed.
Signal signals[NUM_SIGNALS] = {
  {2,  0, 0, HIGH, 0},
  {3,  0, 0, HIGH, 0},
  {4,  0, 0, HIGH, 0},
  {5,  0, 0, HIGH, 0},
  {6,  0, 0, HIGH, 0},
  {7,  0, 0, HIGH, 0},
  {8,  0, 0, HIGH, 0},
  {9,  0, 0, HIGH, 0},
  {10, 0, 0, HIGH, 0},
  {11, 0, 0, HIGH, 0},
  {12, 0, 0, HIGH, 0},
  {13, 0, 0, HIGH, 0},
  {22, 0, 0, HIGH, 0}  // Example extra signal; modify as needed.
};

void setup() {
  Serial.begin(2000000);
  // Initialize each signal pin and store its port register pointer and bit mask.
  for (int i = 0; i < NUM_SIGNALS; i++) {
    pinMode(signals[i].pin, INPUT_PULLUP);
    // Obtain the pointer to the PIN register for this pin.
    signals[i].pinReg = portInputRegister(digitalPinToPort(signals[i].pin));
    // Obtain the bit mask for this pin.
    signals[i].bitMask = digitalPinToBitMask(signals[i].pin);
    // Read the initial state directly.
    signals[i].lastState = (*signals[i].pinReg & signals[i].bitMask) ? HIGH : LOW;
  }
  Serial.println("Signal acquisition started.");
}

void loop() {
  uint32_t now = micros();  // Get the current time (in microseconds)
  // Loop over each signal quickly.
  for (int i = 0; i < NUM_SIGNALS; i++) {
    // Read the current state directly from the port register.
    uint8_t currentState = (*signals[i].pinReg & signals[i].bitMask) ? HIGH : LOW;
    if (currentState != signals[i].lastState) {
      signals[i].lastState = currentState;
      // Only log a pulse when the signal goes LOW.
      if (currentState == LOW) {
        signals[i].impulseCount++;
        // Print the pulse data.
        Serial.print("Pin ");
        Serial.print(signals[i].pin);
        Serial.print(" LOW impulse #");
        Serial.print(signals[i].impulseCount);
        Serial.print(" at time ");
        Serial.println(now);
        
        // Optionally, here you could combine these pulses into a binary data word.
        // For example, you might shift in a bit per pulse, or store timestamps
        // for later decoding.
      }
    }
  }
}

// ------------------------------------------------------------------------
bool pin_access(int col, int line, bool value) {
  if (col < 0 || col >= 4) return false;  // Vérifie si la colonne est valide
  if (line < 0 || line >= 4) return false;  // Vérifie si la colonne est valide
  if (value != HIGH && value != LOW) return false;  // Vérifie si la valeur est valide

  bool allHigh = true;  // Vérifie si tous les signaux sont HIGH

  for (int i = 0; i < sizeof(monitoredPins)/sizeof(monitoredPins[0]); i++) {
    if (digitalRead(monitoredPins[i].arduinoPin) == LOW) { // Si un signal est bas, refus
      Serial.print("Pin ");
      Serial.print(monitoredPins[i].arduinoPin);
      Serial.println(" fermé");
      allHigh = false;
    }
  }

  return allHigh;
}

// Sans doute trop lent avec lecture séquentielle des ports, il faut une lecture simultanée des ports
// ------------------------------------------------------------------------

struct Capture {
  uint8_t portB;
  uint8_t portC;
  uint8_t portD;
  uint16_t clockCycle;
};

Capture captures[100];  // Stocke jusqu'à 100 cycles
uint16_t cycleCount = 0;

void stockerLecture() {
  captures[cycleCount].portB = PINB;
  captures[cycleCount].portC = PINC;
  captures[cycleCount].portD = PIND;
  captures[cycleCount].clockCycle = cycleCount;
  cycleCount++;
}

void loop() {
  while (cycleCount < 100) { // Exemple avec 100 cycles
      stockerLecture();
      clk();  // Synchronisation avec l'horloge
  }
}

// Mode avec 100 cycles de sauvegardés mais est toujours trop lent il faut un écrasement de la mémoire => Buffer Circulaire
// ------------------------------------------------------------------------

#define BUFFER_SIZE 100  // Nombre de cycles stockés avant écrasement

struct Capture {
    uint8_t portB;
    uint8_t portC;
    uint8_t portD;
    uint16_t clockCycle;
};

// Buffer circulaire
Capture buffer[BUFFER_SIZE];
volatile uint8_t writeIndex = 0;
volatile uint8_t readIndex = 0;

void stockerLecture() {
  buffer[writeIndex].portB = PINB;
  buffer[writeIndex].portC = PINC;
  buffer[writeIndex].portD = PIND;
  buffer[writeIndex].clockCycle = writeIndex; // Ou millis() pour un timestamp

  writeIndex = (writeIndex + 1) % BUFFER_SIZE; // Incrément circulaire
}

Capture lireLecture() {
  Capture data = buffer[readIndex]; // Lire la valeur actuelle

  readIndex = (readIndex + 1) % BUFFER_SIZE; // Avancer dans le buffer
  return data;
}

void analyserDonnees() {
  for (int i = 0; i < BUFFER_SIZE; i++) {
      Capture data = lireLecture();
      Serial.print("Cycle: ");
      Serial.print(data.clockCycle);
      Serial.print(" - PortB: ");
      Serial.print(data.portB, BIN);
      Serial.print(" - PortC: ");
      Serial.print(data.portC, BIN);
      Serial.print(" - PortD: ");
      Serial.println(data.portD, BIN);
  }
}

void loop() {
  stockerLecture(); // Stocker une lecture
  analyserDonnees(); // Analyser les données
  clk(); // Horloge
}
