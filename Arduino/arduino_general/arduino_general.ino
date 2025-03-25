#include <math.h>

// *** Declaration of PINs ***
// Assumes Arduino UNO-like board
const int WB = A0;           // Write Back
const int SA = A1;           // Sense Amplifier
const int SL = 2;            // Source Line
const int WL = 3;            // Word Line
const int PRE = 4;           // Precharge
const int BL = 5;            // Bit Line
const int SET_PARA = 6;      // Set Parallel
const int CLOCK = 7;         // Clock
const int SC_IN = 8;         // Scan Chain IN
const int SC_OUT = 9;        // Scan Chain OUT
const int SC_SEL_ZERO = 10;  // Scan Chain Select 0 -> position x
const int SC_SEL_UN = 11;    // Scan Chain Select 1 -> position y

// *** Functions ***
void affMenu(bool premAff);
void ecriture();
void lecture();
int obtenirPosition(const char* message, int min, int max);
bool testRepValide(String reponse, int min, int max);
uint8_t stringToIntToBytes(String rep);
void clk();
void scWLSL(int ligne);
int scOut();
void scBL(uint8_t repByte, int colonne);
void zeroPara(int ligne);
void unPara(int ligne);
void zeroUnitaire();

// *** Setup ***
void setup() {
  // Set all pins as OUTPUT or INPUT
  pinMode(WB, OUTPUT);
  pinMode(SA, OUTPUT);
  pinMode(SL, OUTPUT);
  pinMode(WL, OUTPUT);
  pinMode(PRE, OUTPUT);
  pinMode(BL, OUTPUT);
  pinMode(CLOCK, OUTPUT);
  pinMode(SC_IN, OUTPUT);
  pinMode(SC_SEL_ZERO, OUTPUT);
  pinMode(SC_SEL_UN, OUTPUT);

  pinMode(SC_OUT, INPUT);

  // Set all output pins to LOW initially
  digitalWrite(WB, LOW);
  digitalWrite(SA, LOW);
  digitalWrite(SL, LOW);
  digitalWrite(WL, LOW);
  digitalWrite(PRE, LOW);
  digitalWrite(BL, LOW);
  digitalWrite(CLOCK, LOW);
  digitalWrite(SC_IN, LOW);
  digitalWrite(SC_SEL_ZERO, LOW);
  digitalWrite(SC_SEL_UN, LOW);

  Serial.begin(2000000);
  affMenu(true);
}

// *** Boucle principale : Interface utilisateur ***
void loop() {
  if (Serial.available() > 0) {
    String reponse = Serial.readStringUntil('\n'); // Lecture de la réponse
    int repInt = reponse.toInt(); // Conversion en entier

    //Serial.print("Réponse : ");
    switch (repInt) {
      case 1:
        ecriture();
        break;
      case 2:
        lecture();
        break;
      case 3:
        Serial.println("// Export des données pas encore implémenté.");
        break;
      default:
        Serial.println("Option incorrecte. Veuillez réessayer.");
        break;
    }
  }
}

// *** Gestion des I/O ***
void clk() {
  // Simule un coup d'horloge.
  digitalWrite(CLOCK, HIGH);
  delayMicroseconds(10);
  digitalWrite(CLOCK, LOW);
  delayMicroseconds(10);

}

// *** Menu interactif ***
void affMenu(bool premAff) {
  if (!premAff) {
    Serial.println("\n");
  }
  Serial.println("\n");
  Serial.println("1. Écriture");
  Serial.println("2. Lecture");
  Serial.println("3. Export des données contenues dans la mémoire vers un fichier .txt");
}

// *** Écriture dans la mémoire ***
void ecriture() {
  bool repValide = false; // Vérification de la validité de la réponse
  uint8_t repByte = 0; // Octet à écrire
  String reponse; // Réponse de l'utilisateur

  // 1. Obtenir un entier à écrire
  Serial.println("Entier non signé 8 bits (0 <= nb <= 255) à écrire :");
  while (!repValide) {
    while (!Serial.available())
      ; // Attendre une réponse
    reponse = Serial.readStringUntil('\n');
    repValide = testRepValide(reponse, 0, 255);
    if (repValide) {
      repByte = stringToIntToBytes(reponse);
    }
  }

  // 2. Obtenir la ligne et la colonne
  int ligne = obtenirPosition("Ligne ? (Entre 1 et 128)", 1, 128);
  int colonne = obtenirPosition("Colonne ? (Entre 1 et 16)", 1, 16);

  Serial.println("Écriture en cours...");
  unPara(ligne);  // Remet tous les bits de la ligne à 1

  // Placement des bits
  scBL(repByte, colonne);  // Écriture de la colonne spécifiée avec les bits donnés

  Serial.println("Écriture réussie !");
  affMenu(false);
}

// *** Lecture de la mémoire ***
void lecture() {
  // Obtenir la position de la cellule à lire
  int ligne = obtenirPosition("Ligne ? (Entre 1 et 128)", 1, 128);
  int colonne = obtenirPosition("Colonne ? (Entre 1 et 16)", 1, 16);

  Serial.println("Activer le write-back ? (1 = Oui, 0 = Non)");
  int writeBack = -1;
  while (writeBack < 0 || writeBack > 1) {
    while (!Serial.available())
      ;
    String reponse = Serial.readStringUntil('\n');
    writeBack = reponse.toInt();
  }

  //Serial.print("Lecture de la cellule en ligne ");
  //Serial.print(ligne);
  //Serial.print(", colonne ");
  //Serial.println(colonne);
  if (writeBack == 1) {
    Serial.println("Write-back activé");
  } else {
    Serial.println("Write-back désactivé.");
  }

  // Sélectionner la ligne dans la chaîne de scan
  scWLSL(ligne);

  // Configuration des signaux pour la lecture
  digitalWrite(SET_PARA, HIGH);
  clk();
  digitalWrite(PRE, HIGH);
  clk();
  digitalWrite(WL, HIGH);
  clk();
  clk();
  digitalWrite(PRE, LOW);
  clk();
  digitalWrite(SL, HIGH);
  clk();
  digitalWrite(SA, HIGH);
  clk();

  // Lecture des 8 bits de la colonne spécifiée
  int valeur = 0;
  for (int i = 0; i < 8; i++) {
    clk();
    int bitVal = digitalRead(SC_OUT);
    if (bitVal == HIGH) {
      valeur += (int)pow(2, i);
    }
  }

  // Gestion du write-back si activé
  if (writeBack == 1) {
    digitalWrite(WB, HIGH);
    clk();
    digitalWrite(WB, LOW);
  }

  // Fin de la lecture
  clk();
  digitalWrite(SL, LOW);
  digitalWrite(SA, LOW);
  clk();
  digitalWrite(PRE, HIGH);
  clk();
  clk();
  digitalWrite(WL, LOW);
  clk();
  digitalWrite(PRE, LOW);
  clk();
  digitalWrite(SET_PARA, LOW);
  clk();

  // Résultat de la lecture
  Serial.print("Valeur lue : ");
  Serial.println(valeur);

  affMenu(false);
}

// *** Fonction auxiliaire : Obtenir une position ***
int obtenirPosition(const char* message, int min, int max) {
  String reponse;
  bool repValide = false;

  Serial.println(message);
  while (!repValide) {
    while (!Serial.available())
      ;
    reponse = Serial.readStringUntil('\n');
    repValide = testRepValide(reponse, min, max);
  }

  return reponse.toInt();
}

// *** Vérification de la validité de la réponse ***
bool testRepValide(String reponse, int min, int max) {
  int repInt = reponse.toInt();
  if (repInt >= min && repInt <= max) {
    return true;
  } else {
    Serial.println("Valeur incorrecte. Réessayez.");
    return false;
  }
}

// *** Conversion d'un String en un octet ***
// Retourne un uint8_t avec les bits invertis par rapport au repInt original (si cela est souhaité)
uint8_t stringToIntToBytes(String rep) {
  int repInt = rep.toInt();
  // Selon le code initial, il semblait vouloir inverser les bits
  // mais ce n'était pas très clair. On peut conserver la logique originale:
  // repBits[i] = ~bitRead(repInt, i)
  // Ce qui revient à prendre le complément de repInt pour ce qui est stocké.
  // Simplifions : On peut simplement retourner ~repInt (inversion des bits)
  // Mais attention, ~repInt sur 16 bits n'est pas correct pour un octet.
  // On s'en tient à la logique initiale, qui faisait un bit par bit.
  uint8_t result = 0;
  for (byte i = 0; i < 8; i++) {
    // Inversion du bit
    uint8_t bitVal = bitRead(repInt, i);
    bitVal = ~bitVal & 0x01;  // Inverse le bit (0 -> 1, 1 -> 0)
    if (bitVal == 1) {
      result |= (1 << i);
    }
  }
  return result;
}

// *** Sélection des lignes ***
void scWLSL(int ligne) {
  if (ligne < 0 || ligne >= 128) {
    Serial.println("Erreur : Ligne non valide. Valeur doit être entre 0 et 127.");
    return;
  }

  // Sélection de la bonne Scan Chain
  digitalWrite(SC_SEL_ZERO, HIGH);
  digitalWrite(SC_SEL_UN, LOW);

  Serial.print("Sélection de la ligne : ");
  Serial.println(ligne);

  // Pour chaque ligne, on envoie un pulse de clock
  // Si c'est la ligne sélectionnée, on met SC_IN à HIGH pour un cycle
  for (int i = 0; i < 128; i++) {
    if (i == ligne) {
      digitalWrite(SC_IN, HIGH);
      clk();
      digitalWrite(SC_IN, LOW);
      Serial.print("Ligne ");
      Serial.print(i);
      Serial.println(" sélectionnée.");
    } else {
      digitalWrite(SC_IN, LOW);
      clk();
    }
  }
}

// *** Lecture d'une colonne ***
int scOut() {
  // Sélection de la bonne Scan Chain
  digitalWrite(SC_SEL_ZERO, LOW);
  digitalWrite(SC_SEL_UN, LOW);

  int resultat = 0;
  for (int i = 0; i < 128; i++) {
    clk();
    int bitVal = digitalRead(SC_OUT); // Lecture du bit
    if (bitVal == HIGH) {
      resultat += (int)pow(2, i);
    }
  }
  return resultat;
}

// *** Écriture d'une colonne ***
void scBL(uint8_t repByte, int colonne) {
  if (colonne < 1 || colonne > 16) {
    Serial.println("Erreur : Colonne non valide. Valeur doit être entre 1 et 16.");
    return;
  }

  // Sélection de la bonne Scan Chain
  digitalWrite(SC_SEL_ZERO, LOW);
  digitalWrite(SC_SEL_UN, HIGH);

  Serial.print("Sélection de la colonne : ");
  Serial.println(colonne);

  int startIndex = (colonne - 1) * 8;

  for (int i = 0; i < 128; i++) {
    if (i >= startIndex && i < (startIndex + 8)) {
      int bitIndex = i - startIndex;
      uint8_t bitVal = (repByte >> bitIndex) & 0x01;
      // Le code initial inversait les bits, on le laisse tel quel
      // repBits[i] était un bit inversé, on a déjà repByte inversé
      // Ici, si bitVal == 0, SC_IN = HIGH (pour écrire un '0' inverté)
      // Si bitVal == 1, SC_IN = LOW
      if (bitVal == 0) {
        digitalWrite(SC_IN, HIGH);
      } else {
        digitalWrite(SC_IN, LOW);
      }
      delayMicroseconds(1);
      clk();
    } else {
      digitalWrite(SC_IN, LOW);
      delayMicroseconds(1);
      clk();
    }
  }

  Serial.print("Colonne ");
  Serial.print(colonne);
  Serial.println(" traitée.");
}

// *** Schémas pour coder les 0 et 1 ***
void zeroPara(int ligne) {
  scWLSL(ligne);

  digitalWrite(PRE, HIGH);
  clk();
  delay(5);
  Serial.print("set high WL ");
  digitalWrite(WL, HIGH);
  Serial.print("set low WL ");
  clk();
  clk();
  digitalWrite(PRE, LOW);
  clk();
  digitalWrite(SL, HIGH);
  clk();
  clk();
  digitalWrite(SL, LOW);
  clk();
  digitalWrite(PRE, HIGH);
  clk();
  clk();
  digitalWrite(WL, LOW);
  clk();
  digitalWrite(PRE, LOW);
  clk();
}

// *** Schémas pour coder les 0 et 1 ***
void unPara(int ligne) {
  scWLSL(ligne);

  digitalWrite(PRE, HIGH);

  clk();
  Serial.print("set high WL ");
  digitalWrite(WL, HIGH);
  
  clk();

  clk();

  digitalWrite(PRE, LOW);

  digitalWrite(BL, HIGH);

  clk();

  clk();

  digitalWrite(PRE, HIGH);

  clk();

  clk();

  digitalWrite(WL, LOW);
  Serial.print("set low WL ");
  // Delay to observe WL LOW level again
  digitalWrite(PRE, LOW);
  clk();
}

// *** Schémas pour coder les 0 et 1 ***
void zeroUnitaire() {
  digitalWrite(PRE, HIGH);
  clk();
  digitalWrite(WL, HIGH);
  clk();
  clk();
  digitalWrite(PRE, LOW);
  clk();
  digitalWrite(SL, HIGH);
  digitalWrite(BL, HIGH);
  clk();
  digitalWrite(SL, LOW);
  digitalWrite(BL, LOW);
  clk();
  digitalWrite(PRE, HIGH);
  clk();
  clk();
  digitalWrite(WL, LOW);
  clk();
  digitalWrite(PRE, LOW);
  clk();
}
