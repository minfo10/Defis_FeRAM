/*
  Example code for Arduino Mega 2560 that:
    - Uses the correct port-bit mapping for pins 2–13, 22–34 on the Mega.
    - Detects rising edges on pin 7 (PH4).
    - Reads all relevant ports at once, then prints the state of each monitored pin.
    - Uses INPUT_PULLUP on each monitored pin (so unconnected pins will read HIGH).
      Remove INPUT_PULLUP if you want them to float or use external pull-down resistors.

  References:
    1) Arduino Mega Pinout Diagram (latest):
       https://content.arduino.cc/assets/Pinout-Mega2560rev3_latest.pdf
    2) ATmega2560 datasheet:
       http://ww1.microchip.com/downloads/en/DeviceDoc/Atmel-2549-8-bit-AVR-Microcontroller-ATmega640-1280-1281-2560-2561_datasheet.pdf
*/

// ------------------------------------------------------------------------
// 1) Define the clock pin (for rising-edge detection)
const int CLOCK_PIN = 7; // On Arduino Mega, this is PH4 internally.

// 2) Data structure to hold pin -> (register, bitmask, portName)
struct PinDefinition {
  uint8_t arduinoPin;           // e.g. 2, 3, 22, ...
  volatile uint8_t* pinReg;     // e.g. &PINE, &PINH, &PINA, etc.
  uint8_t bitMask;              // e.g. (1 << 4) for PE4
  const char* portName;         // for printing, e.g. "PORTE"
};

// We define macros to map e.g. PE4 -> 4, PB6 -> 6, etc.
#define PE4 4
#define PE5 5
#define PG5 5
#define PE3 3
#define PH3 3
#define PH4 4
#define PH5 5
#define PH6 6
#define PB4 4
#define PB5 5
#define PB6 6
#define PB7 7
#define PA0 0
#define PA1 1
#define PA2 2
#define PA3 3
#define PA4 4
#define PA5 5
#define PA6 6
#define PA7 7
#define PC7 7
#define PC6 6
#define PC5 5
#define PC4 4
#define PC3 3

// ------------------------------------------------------------------------
// 3) Create our table of monitored pins (with correct port-bit mapping):
PinDefinition monitoredPins[] = {
  // Pin 2 = PE4
  {  2, &PINE, (1 << PE4), "PORTE" },
  // Pin 3 = PE5
  {  3, &PINE, (1 << PE5), "PORTE" },
  // Pin 4 = PG5
  {  4, &PING, (1 << PG5), "PORTG" },
  // Pin 5 = PE3
  {  5, &PINE, (1 << PE3), "PORTE" },
  // Pin 6 = PH3
  {  6, &PINH, (1 << PH3), "PORTH" },
  // Pin 7 = PH4
  {  7, &PINH, (1 << PH4), "PORTH" },
  // Pin 8 = PH5
  {  8, &PINH, (1 << PH5), "PORTH" },
  // Pin 9 = PH6
  {  9, &PINH, (1 << PH6), "PORTH" },
  // Pin 10 = PB4
  { 10, &PINB, (1 << PB4), "PORTB" },
  // Pin 11 = PB5
  { 11, &PINB, (1 << PB5), "PORTB" },
  // Pin 12 = PB6
  { 12, &PINB, (1 << PB6), "PORTB" },
  // Pin 13 = PB7
  { 13, &PINB, (1 << PB7), "PORTB" },

  // Pin 22 = PA0
  { 22, &PINA, (1 << PA0), "PORTA" },
  // Pin 23 = PA1
  { 23, &PINA, (1 << PA1), "PORTA" },
  // Pin 24 = PA2
  { 24, &PINA, (1 << PA2), "PORTA" },
  // Pin 25 = PA3
  { 25, &PINA, (1 << PA3), "PORTA" },
  // Pin 26 = PA4
  { 26, &PINA, (1 << PA4), "PORTA" },
  // Pin 27 = PA5
  { 27, &PINA, (1 << PA5), "PORTA" },
  // Pin 28 = PA6
  { 28, &PINA, (1 << PA6), "PORTA" },
  // Pin 29 = PA7
  { 29, &PINA, (1 << PA7), "PORTA" },
  // Pin 30 = PC7
  { 30, &PINC, (1 << PC7), "PORTC" },
  // Pin 31 = PC6
  { 31, &PINC, (1 << PC6), "PORTC" },
  // Pin 32 = PC5
  { 32, &PINC, (1 << PC5), "PORTC" },
  // Pin 33 = PC4
  { 33, &PINC, (1 << PC4), "PORTC" },
  // Pin 34 = PC3
  { 34, &PINC, (1 << PC3), "PORTC" },
};

// ------------------------------------------------------------------------
void setup() {
  Serial.begin(2000000);

  // 4) Configure the clock pin for rising-edge detection
  pinMode(CLOCK_PIN, INPUT); // or INPUT_PULLUP if needed

  // 5) Configure monitored pins as inputs with pull-up
  for (unsigned i = 0; i < sizeof(monitoredPins)/sizeof(monitoredPins[0]); i++) {
    pinMode(monitoredPins[i].arduinoPin, INPUT_PULLUP);
  }
}

// ------------------------------------------------------------------------
void loop() {
  static int lastClockState = LOW;
  int currentClockState = digitalRead(CLOCK_PIN);

  // Detect rising edge on pin 7
  if (lastClockState == LOW && currentClockState == HIGH) {
    // 6) On rising edge, read the relevant ports *once*
    //    We only need to read each port we actually use.
    //    This ensures we capture all pin states "at the same instant".
    uint8_t portAVal = PINA;
    uint8_t portBVal = PINB;
    uint8_t portCVal = PINC;
    uint8_t portGVal = PING;
    uint8_t portHVal = PINH;
    uint8_t portEVal = PINE;
    // (If needed, add PIND, PINF, PINJ, PINL, etc. for other pins.)

    // Print a timestamp to show when this read happened
    Serial.print(millis());
    Serial.println(" ms: Reading all monitored pins...");

    // 7) For each monitored pin, figure out if it was HIGH or LOW
    for (unsigned i = 0; i < sizeof(monitoredPins)/sizeof(monitoredPins[0]); i++) {
      // Grab info from the table
      uint8_t pinNumber    = monitoredPins[i].arduinoPin;
      volatile uint8_t* reg= monitoredPins[i].pinReg;
      uint8_t bitMask      = monitoredPins[i].bitMask;
      const char* portName = monitoredPins[i].portName;

      // Based on which register pointer it is, use the cached port values:
      uint8_t portVal;
      if (reg == &PINA) {
        portVal = portAVal;
      } else if (reg == &PINB) {
        portVal = portBVal;
      } else if (reg == &PINC) {
        portVal = portCVal;
      } else if (reg == &PING) {
        portVal = portGVal;
      } else if (reg == &PINH) {
        portVal = portHVal;
      } else if (reg == &PINE) {
        portVal = portEVal;
      } else {
        // If you ever add pins from other ports, add them here
        portVal = 0; // default
      }

      // Check if the bit is set
      bool isHigh = (portVal & bitMask) != 0;

      // Print the result
      Serial.print(portName);
      Serial.print(" (pin ");
      Serial.print(pinNumber);
      Serial.print("): ");
      Serial.println(isHigh ? "HIGH" : "LOW");
    }

    Serial.println();
  }

  lastClockState = currentClockState;
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