#define SC_SEL_ZERO_PIN 10  // Broche à connecter à SC_SEL_ZERO_PIN du simulateur
#define SC_SEL_UN_PIN 11    // Broche à connecter à SC_SEL_UN_PIN du simulateur

void setup() {
  pinMode(SC_SEL_ZERO_PIN, INPUT);
  pinMode(SC_SEL_UN_PIN, INPUT);
  
  Serial.begin(9600);
  Serial.println("Arduino principal prêt.");
}

void loop() {
  bool sc_sel_zero = digitalRead(SC_SEL_ZERO_PIN);
  bool sc_sel_un = digitalRead(SC_SEL_UN_PIN);
  
  Serial.print("SC_SEL_ZERO_PIN : ");
  Serial.println(sc_sel_zero);
  Serial.print("SC_SEL_UN_PIN : ");
  Serial.println(sc_sel_un);
  Serial.print("\n");
  delay(2000);  // Attendre 1 seconde pour afficher les résultats
}
