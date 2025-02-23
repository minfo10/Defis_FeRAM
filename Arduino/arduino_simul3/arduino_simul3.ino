#define BUFFER_SIZE 100  // Nombre de cycles stockés

// Définition des broches des signaux
#define WL 2   // Word Line
#define PRE 3  // Precharge
#define SL 4   // Source Line
#define BL 5   // Bit Line

// Structure pour stocker les lectures
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

// Fonction d’horloge
void clk() {
    digitalWrite(6, HIGH);
    delayMicroseconds(10);
    digitalWrite(6, LOW);
    delayMicroseconds(10);
}

// Fonction pour stocker une lecture dans le buffer
void stockerLecture() {
    buffer[writeIndex].portB = PINB;
    buffer[writeIndex].portC = PINC;
    buffer[writeIndex].portD = PIND;
    buffer[writeIndex].clockCycle = writeIndex;  // Ou millis() pour un timestamp

    writeIndex = (writeIndex + 1) % BUFFER_SIZE; // Incrément circulaire
}

// Fonction pour lire une donnée du buffer
Capture lireLecture() {
    Capture data = buffer[readIndex];
    readIndex = (readIndex + 1) % BUFFER_SIZE;
    return data;
}

// Fonction pour interpréter les signaux et extraire ligne, colonne, valeur
void interpreterSignaux() {
    for (int i = 0; i < BUFFER_SIZE; i++) {
        Capture data = buffer[i];

        // Décodage de la ligne (Word Line)
        int ligne = (data.portB & (1 << WL)) ? 1 : 0;

        // Décodage de la colonne (Bit Line)
        int colonne = (data.portB & (1 << BL)) ? 1 : 0;

        // Détection de la valeur stockée
        int valeur = 0;
        
        if ((data.portB & (1 << PRE)) && (data.portB & (1 << WL))) {
            valeur = (data.portB & (1 << SL)) ? 0 : 1;
        }

        // Affichage du résultat interprété
        Serial.print("Cycle: ");
        Serial.print(data.clockCycle);
        Serial.print(" - Ligne: ");
        Serial.print(ligne);
        Serial.print(" - Colonne: ");
        Serial.print(colonne);
        Serial.print(" - Valeur: ");
        Serial.println(valeur);
    }
}

void setup() {
    Serial.begin(115200);
    
    // Initialisation des broches
    pinMode(WL, INPUT);
    pinMode(PRE, INPUT);
    pinMode(SL, INPUT);
    pinMode(BL, INPUT);
}

void loop() {
    stockerLecture();  // Stocke une lecture
    clk();             // Fait avancer l’horloge

    if (writeIndex == 0) { // Lorsque le buffer est plein, on analyse
        interpreterSignaux();
    }
}


// Autre fonction possible : captures
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

// ------------------------------------------------------------------------
/* On peut aussi faire quelques autres améliorations

 Augmenter BUFFER_SIZE si plus de cycles sont nécessaires avant analyse.
 Utiliser millis() pour les timestamps au lieu d’un simple compteur.
 Optimiser l’interprétation en comparant directement des séquences plutôt que bit à bit.*/