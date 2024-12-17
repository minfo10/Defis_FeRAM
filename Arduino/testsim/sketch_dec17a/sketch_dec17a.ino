#define SC_SEL_ZERO_PIN 10  // Broche à connecter à SC_SEL_ZERO_PIN de l'Arduino principal
#define SC_SEL_UN_PIN 11    // Broche à connecter à SC_SEL_UN_PIN de l'Arduino principal

void setup() {
  pinMode(SC_SEL_ZERO_PIN, OUTPUT);
  pinMode(SC_SEL_UN_PIN, OUTPUT);
  
  Serial.begin(9600);
  Serial.println("Simulateur prêt.");
}

void loop() {
  // Simuler des impulsions
  digitalWrite(SC_SEL_ZERO_PIN, HIGH);
  digitalWrite(SC_SEL_UN_PIN, LOW);
  Serial.println("SC_SEL_ZERO : 1");
  Serial.println("SC_SEL_UN : 0");
  delay(2000);  // Maintenir pendant 1 seconde
  Serial.print("\n");
  
  digitalWrite(SC_SEL_ZERO_PIN, LOW);
  digitalWrite(SC_SEL_UN_PIN, HIGH);
  Serial.println("SC_SEL_ZERO : 0");
    Serial.println("SC_SEL_UN : 1");
  delay(2000);  // Maintenir pendant 1 seconde
  Serial.print("\n");
  
}
