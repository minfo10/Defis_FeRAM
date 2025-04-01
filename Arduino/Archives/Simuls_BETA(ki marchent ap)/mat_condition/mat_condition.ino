const int numSignals = 2;  // Nombre de bits
const int signalPins[numSignals] = {2,3};  // Exemple avec 8 pins définis
const int clockInterval = 10;  // Intervalle de l'horloge en ms
unsigned long lastClock = 0;  // Dernière mise à jour du clock

// Matrice mémoire (8x4) : 8 lignes pour 4 octets
int memoryMatrix[8][4] = {0};  // Initialisation à 0

// Vérifie si l'accès à une colonne est autorisé
bool accessGranted(int col) {
    if (col < 0 || col >= 4) return false;  // Vérifie si la colonne est valide

    for (int i = 1; i < numSignals; i++) {
      if(digitalRead(signalPins[i]) == HIGH){ // Si un signal est OFF, refus*
        Serial.print("Pin ");
        Serial.print(i);
        Serial.print(" ouvert\n");
      }
    }
    return true;
}

// Modifie une valeur dans la mémoire si l'accès est autorisé
void setMemoryValue(int row, int col, int value) {
    if (accessGranted(col)) {
        memoryMatrix[row][col] = value;
        Serial.print("Mémoire mise à jour : (");
        Serial.print(row);
        Serial.print(",");
        Serial.print(col);
        Serial.print(") -> ");
        Serial.println(value, BIN);  // Affichage en binaire
        Serial.print("\n");
    } else {
        Serial.println("Accès refusé : Signaux insuffisants !");
    }
}

// Lit une valeur de la mémoire
int getMemoryValue(int row, int col) {
    return memoryMatrix[row][col];
}

// Affiche la mémoire en binaire
void printMemory() {
    Serial.println("État actuel de la mémoire :");
    Serial.println("-----------------------------");
    for (int i = 0; i < 8; i++) {
        for (int j = 0; j < 4; j++) {
            Serial.print(memoryMatrix[i][j], BIN);
            Serial.print("\t");
        }
        Serial.println();
    }
    Serial.println("-----------------------------");
}

void setup() {
    Serial.begin(2000000);
    
    // Configuration des pins d'entrée avec pull-up interne
    for (int i = 0; i < numSignals; i++) {
        pinMode(signalPins[i], INPUT_PULLUP);
    }

    Serial.print("Système mémoire prêt !\n");
    printMemory();
}

void loop() {
    // Vérification périodique
    unsigned long currentMillis = millis();
    if (currentMillis - lastClock >= clockInterval) {
        lastClock = currentMillis;
    }
    // Lecture des commandes série
    if (Serial.available() > 0) {
        String command = Serial.readStringUntil('\n');
        command.trim();

        if (command.startsWith("SET")) {
            // Format attendu : SET ligne colonne valeur
            int row, col, value;
            if (sscanf(command.c_str(), "SET %d %d %d", &row, &col, &value) == 3) {
                setMemoryValue(row, col, value);
              
            } else {
                Serial.println("Commande invalide. Format : SET ligne colonne valeur");
            }
        } else if (command.startsWith("GET")) {
            // Format attendu : GET ligne colonne
            int row, col;
            if (sscanf(command.c_str(), "GET %d %d", &row, &col) == 2) {
                Serial.print("Valeur en (");
                Serial.print(row);
                Serial.print(",");
                Serial.print(col);
                Serial.print(") : ");
                Serial.println(getMemoryValue(row, col), BIN);
            } else {
                Serial.println("Commande invalide. Format : GET ligne colonne");
            }
        } else if (command == "PRINT") {
            printMemory();
        } else {
            Serial.println("Commande inconnue. Utilisez :");
            Serial.println(" - SET ligne colonne valeur");
            Serial.println(" - GET ligne colonne");
            Serial.println(" - PRINT");
        }
    }
}
