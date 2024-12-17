#include <Arduino.h>

// *** Déclaration des broches pour la simulation ***
// Pins simulant les lignes et signaux de contrôle
#define PRE_PIN 4           // Precharge
#define WL_PIN 5            // Word Line
#define SL_PIN 6            // Source Line
#define BL_PIN 7            // Base Line
#define CLOCK_PIN 8         // Horloge
#define SET_PARALLEL_PIN 9  // Activation parallèle
#define SC_SEL_ZERO_PIN 10  // Sélection Scan Chain 0
#define SC_SEL_UN_PIN 11    // Sélection Scan Chain 1
#define SA_PIN 12           // Sense Amplifier
#define SC_IN_PIN 13        // Entrée Scan Chain

// *** Variables globales ***
bool memory[32][16] = {false}; // Représentation mémoire : 32 lignes, 16 colonnes ---- 128 lignes ne marche pas car pas assez de mémoire dans la Arduino
int currentRow = -1;     // Ligne actuellement sélectionnée

// *** Déclarations des fonctions ***
void testScanChainSignals();
void configureScanChain(uint8_t row);
void checkScanChainSelection();
int selectScanChainRow();
void simulateMemoryOperations();
void writeToMemory(int row);
void readFromMemory(int row);
void waitForClock();

// *** Initialisation des broches et de la simulation ***
void setup() {
  Serial.begin(9600);
  // Vérifiez si la communication série est correctement établie
  while (!Serial) {
    // Attente pour la connexion au port série (utilisé principalement avec les cartes Arduino Leonardo ou Micro)
  }
  Serial.println("Simulation de mémoire FeRAM prête.");

  // Configuration des broches en tant qu'entrées ou sorties
  pinMode(PRE_PIN, OUTPUT);
  pinMode(WL_PIN, OUTPUT);
  pinMode(SL_PIN, OUTPUT);
  pinMode(BL_PIN, OUTPUT);
  pinMode(SET_PARALLEL_PIN, OUTPUT);
  pinMode(SA_PIN, OUTPUT);

  pinMode(CLOCK_PIN, INPUT);
  pinMode(SC_IN_PIN, INPUT);

  // Initialisation de l'état des signaux
  digitalWrite(PRE_PIN, LOW);
  digitalWrite(WL_PIN, LOW);
  digitalWrite(SL_PIN, LOW);
  digitalWrite(BL_PIN, LOW);
  digitalWrite(SET_PARALLEL_PIN, LOW);
  digitalWrite(SA_PIN, LOW);

  // Essai débuggage
  pinMode(SC_SEL_ZERO_PIN, INPUT_PULLUP);   // était INPUT
  pinMode(SC_SEL_UN_PIN, INPUT_PULLUP);     // était INPUT

  digitalWrite(SC_SEL_ZERO_PIN, LOW);
  pinMode(SC_SEL_ZERO_PIN, OUTPUT);
  digitalWrite(SC_SEL_UN_PIN, LOW);
  pinMode(SC_SEL_UN_PIN, OUTPUT);

  // Test des signaux de chaînes de scan
  testScanChainSignals();
}

// *** Boucle principale ***
void loop() {
  // Vérifie et sélectionne la chaîne de scan
  checkScanChainSelection();

  // Lecture de l'état des broches pour simuler les actions
  simulateMemoryOperations();
}

// *** Test des signaux de chaînes de scan ***
void testScanChainSignals() {
  Serial.println("Test des signaux de chaînes de scan...");

  // Test SC_SEL_ZERO
  digitalWrite(SC_SEL_ZERO_PIN, HIGH); // Activer
  delay(1000);
  if (digitalRead(SC_SEL_ZERO_PIN) == HIGH) {
    Serial.println("SC_SEL_ZERO fonctionne correctement.");
  } else {
    Serial.println("SC_SEL_ZERO ne fonctionne pas !");
  }
  digitalWrite(SC_SEL_ZERO_PIN, LOW); // Désactiver

  // Test SC_SEL_UN
  digitalWrite(SC_SEL_UN_PIN, HIGH); // Activer
  delay(1000);
  if (digitalRead(SC_SEL_UN_PIN) == HIGH) {
    Serial.println("SC_SEL_UN fonctionne correctement.");
  } else {
    Serial.println("SC_SEL_UN ne fonctionne pas !");
  }
  digitalWrite(SC_SEL_UN_PIN, LOW); // Désactiver
}

// *** Configuration de la chaîne de scan ***
void configureScanChain(uint8_t row) {
  if (row % 2 == 0) {
    digitalWrite(SC_SEL_ZERO_PIN, HIGH);
    digitalWrite(SC_SEL_UN_PIN, LOW);
    Serial.println("SC_SEL_ZERO activé, SC_SEL_UN désactivé.");
  } else {
    digitalWrite(SC_SEL_ZERO_PIN, LOW);
    digitalWrite(SC_SEL_UN_PIN, HIGH);
    Serial.println("SC_SEL_ZERO désactivé, SC_SEL_UN activé.");
  }
  delay(50); // Ajout d'un délai pour laisser le temps aux signaux de se stabiliser

  verificationdesetats();
}

void verificationdesetats() {
  bool sc_sel_zero = digitalRead(SC_SEL_ZERO_PIN);
  bool sc_sel_un = digitalRead(SC_SEL_UN_PIN);

  // Debugging : Affiche l'état des broches
  Serial.print("État SC_SEL_ZERO_PIN : ");
  Serial.println(sc_sel_zero);
  Serial.print("État SC_SEL_UN_PIN : ");
  Serial.println(sc_sel_un);
  delay(1000);
}


// *** Vérification de la sélection de la chaîne de scan ***
void checkScanChainSelection() {
  verificationdesetats();

  bool sc_sel_zero = digitalRead(SC_SEL_ZERO_PIN);
  bool sc_sel_un = digitalRead(SC_SEL_UN_PIN);

  if (sc_sel_zero && !sc_sel_un) {
    // Simulation de la sélection d'une ligne via la chaîne de scan
    currentRow = selectScanChainRow();
  } else if (!sc_sel_zero && sc_sel_un) {
    // Traitement pour les colonnes (ou une autre fonctionnalité)
    Serial.println("Mode colonne activé.");
  } else {
    Serial.println("Erreur : Les signaux SC_SEL_ZERO et SC_SEL_UN ne sont pas correctement configurés.");
  }

  verificationdesetats();
}

// *** Sélection d'une ligne dans la chaîne de scan ***
int selectScanChainRow() {
  Serial.println("Sélection de la ligne via la chaîne de scan...");
  for (int i = 0; i < 128; i++) {
    waitForClock(); // Attend un signal d'horloge
    if (digitalRead(SC_IN_PIN)) {
      Serial.print("Ligne sélectionnée : ");
      Serial.println(i);
      return i;
    }
  }
  Serial.println("Aucune ligne sélectionnée.");
  return -1; // Aucun index valide sélectionné
}

// *** Simulation des opérations de mémoire ***
void simulateMemoryOperations() {
  if (currentRow == -1) {
    return;
  }

  if (digitalRead(SET_PARALLEL_PIN)) {
    Serial.print("Opération parallèle sur la ligne : ");
    Serial.println(currentRow);

    bool writeMode = digitalRead(BL_PIN);
    if (writeMode) {
      writeToMemory(currentRow);
    } else {
      readFromMemory(currentRow);
    }
  }
}

// *** Écriture dans la mémoire simulée ***
void writeToMemory(int row) {
  Serial.print("Écriture dans la ligne ");
  Serial.println(row);

  for (int col = 0; col < 16; col++) {
    waitForClock(); // Attente de l'horloge pour synchronisation
    bool bitValue = digitalRead(SC_IN_PIN); // Lire les bits depuis SC_IN
    memory[row][col] = bitValue;
  }
  Serial.println("Écriture terminée.");
}

// *** Lecture depuis la mémoire simulée ***
void readFromMemory(int row) {
  Serial.print("Lecture depuis la ligne ");
  Serial.println(row);

  for (int col = 0; col < 16; col++) {
    waitForClock(); // Attente de l'horloge pour synchronisation
    bool bitValue = memory[row][col]; // Récupérer la valeur stockée
    Serial.print(bitValue ? "1" : "0");
    Serial.print(" "); // Séparation des colonnes
  }
  Serial.println("\nLecture terminée.");
}

// *** Attente pour synchronisation avec l'horloge ***
void waitForClock() {
  while (digitalRead(CLOCK_PIN) == LOW) {
    // Attente pour que l'horloge passe à HIGH
  }
  delayMicroseconds(2); // Délai pour simuler la stabilité du signal
  while (digitalRead(CLOCK_PIN) == HIGH) {
    // Attente pour que l'horloge repasse à LOW
  }
}
