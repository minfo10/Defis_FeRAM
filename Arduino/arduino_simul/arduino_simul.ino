#include <Arduino.h>

// Pin definitions for the probe card simulation
#define PRE_PIN 4
#define WL_PIN 5
#define SL_PIN 6
#define BL_PIN 7
#define CLOCK_PIN 8
#define SET_PARALLEL_PIN 9
#define SC_SEL_ZERO_PIN 10
#define SC_SEL_UN_PIN 11
#define SA_PIN 12
#define SC_IN_PIN 13

void waitForClk() {
  while (digitalRead(CLOCK_PIN) == LOW) {
    // Wait for clock to go HIGH
  }
  delayMicroseconds(2);
  while (digitalRead(CLOCK_PIN) == HIGH) {
  }
}

void selectScanChain() {
  bool sc_sel_zero = digitalRead(SC_SEL_ZERO_PIN);
  bool sc_sel_un = digitalRead(SC_SEL_UN_PIN);

  if (sc_sel_zero && !sc_sel_un) {
    for (int i = 0; i < 128; i++) {
      bool sc_in = digitalRead(SC_IN_PIN);
      if (sc_in) {
        Serial.print("Selected scan chain for row ");
        Serial.println(i);
      }
      waitForClk();
    }
    Serial.println("Scan chain selection successful.");
  } else {
    // If the selection signals are incorrect
    if (!sc_sel_zero) {
      Serial.println("Error: SC_SEL_ZERO is not set correctly.");
    }
    if (sc_sel_un) {
      Serial.println("Error: SC_SEL_UN should be LOW but it is HIGH.");
    }
  }
}

void setup() {
  // Initialize pins
  pinMode(PRE_PIN, OUTPUT);
  pinMode(WL_PIN, OUTPUT);
  pinMode(SL_PIN, OUTPUT);
  pinMode(BL_PIN, OUTPUT);
  pinMode(SET_PARALLEL_PIN, OUTPUT);
  pinMode(SA_PIN, OUTPUT);

  // Pins that receive signals from the controller Arduino
  pinMode(CLOCK_PIN, INPUT);
  pinMode(SC_SEL_ZERO_PIN, INPUT);
  pinMode(SC_SEL_UN_PIN, INPUT);
  pinMode(SC_IN_PIN, INPUT);

  Serial.begin(9600);
  Serial.println("FeRAM Probe Card Simulation Ready");
}

void loop() {
  // Continuously check for scan chain selection
  selectScanChain();
}
