#include <math.h> // Utile pour isNaN

// Manipulation directe des ports
#define pON(port, pin) (port |= bit(pin)) // Passage à l'état HAUT
#define pOFF(port, pin) (port &= ~ bit(pin)) // Passage à l'état BAS
#define lect(port, pin) ((port) & bit(pin)) // Lecture sans modifier le port

// Pins à brancher.
const int WB = A0; // Remplace la broche 0
const int SA = A1; // Remplace la broche 1

const int SL = 2;
const int WL = 3;
const int PRE = 4;
const int BL = 5;
const int SET_PARA = 6;
const int CLOCK = 7;
const int SC_IN = 8;
const int SC_OUT = 9;
const int SC_SEL_ZERO = 10;
const int SC_SEL_UN = 11;

// Définition des fonctions de base du programme (cf chronogrammes)
void clk(){
	// Simule un coup de clock.
	// Il est important de noter ici que la carte à pointe prend en compte le changement d'état de ses entrée..
	// uniquement quand elle reçoit un front montant sur le pin CLOCK.
	// Le rapport cyclique du signal créneau envoyé n'a donc aucune importance.
	pON(PORTD, CLOCK);
	delayMicroseconds(2);
	pOFF(PORTD, CLOCK);
}
void scWLSL(int ligne) {
    // Vérifie si la ligne est dans la plage valide
    if (ligne < 0 || ligne >= 128) {
        Serial.println("Erreur : Ligne non valide. Valeur doit être entre 0 et 127.");
        return;
    }

    // Sélection de la bonne Scan Chain
    pON(PORTB, SC_SEL_ZERO);
    pOFF(PORTB, SC_SEL_UN);

    Serial.print("Sélection de la ligne : ");
    Serial.println(ligne);

    for (int i = 0; i < 128; i++) {
        if (i == ligne) { // Si la i-ième ligne est la ligne choisie
            pON(PORTB, SC_IN);
            clk();  // Une seule impulsion est suffisante pour indiquer la sélection
            pOFF(PORTB, SC_IN);
            Serial.print("Ligne ");
            Serial.print(i);
            Serial.println(" sélectionnée.");
        } else {
            clk(); // Impulsion de clock pour les autres lignes
        }
    }
}


int scOut(){
	// Permet de lire la valeur stockée dans la ligne préalablement choisie par l'appel de la fonction scWLSL.

	// Sélection de la bonne Scan Chain (cf 4.4.2.1 de la thèse de Mr Francois)
	pOFF(PORTB, SC_SEL_ZERO);
	pOFF(PORTB, SC_SEL_UN);

	int resultat = 0; // Valeur stockée dans la ligne choisie

	for(int i = 0; i < 128; i++){ // Lecture des 128 blocs d'une ligne
		clk();

		// A VERIFIER SUR CARTE -----------------------------------------------
		if (lect(PORTB, SC_OUT) != 0){ // la i-ième cellule contient un 1
			resultat += pow(2, i);
		}
	}

	return resultat;
}

void scBL(byte rep[8], int colonne) {
    // Vérifie si la colonne est dans la plage valide
    if (colonne < 1 || colonne > 16) {
        Serial.println("Erreur : Colonne non valide. Valeur doit être entre 1 et 16.");
        return;
    }

    // Sélection de la bonne Scan Chain
    pOFF(PORTB, SC_SEL_ZERO);
    pON(PORTB, SC_SEL_UN);

    Serial.print("Sélection de la colonne : ");
    Serial.println(colonne);

    int startIndex = (colonne - 1) * 8;  // Calcul de l'index de début pour la colonne

    for (int i = 0; i < 120; i++) {
        if (i == startIndex) {
            for (int j = 0; j < 8; j++) {
                if (rep[j] == 0) {
                    pON(PORTB, SC_IN);
                    clk();
                    pOFF(PORTB, SC_IN);
                } else {
                    clk();
                }
            }
            Serial.print("Colonne ");
            Serial.print(colonne);
            Serial.println(" traitée.");
        } else {
            clk();  // Impulsions pour les autres colonnes
        }
    }
}


void zeroPara(int ligne){
	// Programmation parallèle d'un 0 sur toute la ligne en argument.

	// Sélection de la ligne
	scWLSL(ligne);

	// Copie du chronogramme (cf 4.4.1.1 de la thèse de mr Francois)
	pON(PORTD, PRE);
	clk();
	pON(PORTD, WL);
	clk();
	clk();
	pOFF(PORTD, PRE);
	clk();
	pON(PORTD, SL);
	clk();
	clk();
	pOFF(PORTD, SL);
	clk();
	pON(PORTD, PRE);
	clk();
	clk();
	pOFF(PORTD, WL);
	clk();
	pOFF(PORTD, PRE);
	clk();
}

void unPara(int ligne){
	// Programmation parallèle d'un 1 sur toute la ligne en argument.

	// Sélection de la ligne
	scWLSL(ligne);

	// Copie du chronogramme (cf 4.4.1.1 de la thèse de mr Francois)
	pON(PORTD, PRE);
	clk();
	pON(PORTD, WL);
	clk();
	clk();
	pOFF(PORTD, PRE);
	clk();
	pON(PORTD, BL);
	clk();
	clk();
	pON(PORTD, PRE);
	clk();
	clk();
	pOFF(PORTD, WL);
	clk();
	pOFF(PORTD, PRE);
	clk();
}

void lectCellule(int ligne, int writeBack) {
    Serial.print("Lecture de la cellule sur la ligne : ");
    Serial.println(ligne);
    if (writeBack == 1) {
        Serial.println("Write-back activé pour cette lecture.");
    } else {
        Serial.println("Write-back non activé pour cette lecture.");
    }

    // Sélection de la ligne
    scWLSL(ligne);

    // Copie du chronogramme (cf 4.4.1.1 de la thèse de mr Francois)
    pON(PORTD, SET_PARA);
    clk();
    pON(PORTD, PRE);
    clk();
    pON(PORTD, WL);
    clk();
    clk();
    pOFF(PORTD, PRE);
    clk();
    pON(PORTD, SL);
    clk();
    pON(PORTD, SA);
    clk();
    clk();
    clk();
    clk();
    pOFF(PORTD, SL);
    pOFF(PORTD, SA);
    if (writeBack == 1) {
        pON(PORTD, WB);
        Serial.println("Signal WB activé.");
    }
    clk();
    pON(PORTD, PRE);
    pOFF(PORTD, WB);
    clk();
    clk();
    pOFF(PORTD, WL);
    clk();
    pOFF(PORTD, PRE);
    clk();
    pOFF(PORTD, SET_PARA);
    clk();
}



int lecture(int ligne, int colonne){
	int lu = 0;
		for (int i = 0; i < 8; i++) {
    lectCellule(ligne, 1);  // Utilisation de `1` pour activer le write-back après lecture
    if (lect(PINB, SC_OUT) != 0) {
        lu += pow(2, i);
    }
}

	return lu;
}

void zeroUnitaire(){
	pON(PORTD, PRE);
	clk();
	pON(PORTD, WL);
	clk();
	clk();
	pOFF(PORTD, PRE);
	clk();
	pON(PORTD, SL);
	pON(PORTD, BL);
	clk();
	pOFF(PORTD, SL);
	pOFF(PORTD, BL);
	clk();
	pON(PORTD, PRE);
	clk();
	clk();
	pOFF(PORTD, WL);
	clk();
	pOFF(PORTD, PRE);
	clk();
}

byte stringToIntToBytes(String rep){
	// Transforme la chaîne de caractère donnée par l'utilisateur en tableau contenant sa décomposition en base 2.
	int repInt = rep.toInt();
	byte repBits[8];
	for(byte i = 0; i < 8; i++){
		repBits[i] = ~ bitRead(repInt, i); // NOT bit --> Il est préférable de tout placer à 1 puis placer les 0 (cf fonction scBL)
	}
	return repBits;
}

bool testRepValide(String reponse, int min, int max){
	// Vérifie si une réponse entrée par l'utilisateur est valide. Fonction utile pour l'interface.
	int repInt = reponse.toInt();
	if(repInt >= min && repInt <= max){
		return true;
	} else {
		Serial.println("Incorrect");
		return false;
	}
}

void affMenu(bool premAff){
	if(not premAff){
		Serial.println("\n");
	}
	Serial.println("1. Ecriture");
	Serial.println("2. Lecture");
	Serial.println("3. Export des données contenues dans la mémoire vers un txt.");
}

void setup() {
  // Configuration des pins
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

    // Interface homme-machine par le moniteur série
  Serial.begin(9600);
  affMenu(true);
}

void loop() {
    if (Serial.available() > 0) { // Attente d'une réponse de l'utilisateur
        String reponse = Serial.readStringUntil('\n');
        int repInt = reponse.toInt();

        if (repInt == 1) { // Écriture d'un entier 8 bits
            // Nombre à coder
            bool repValide = false;
            byte repBits[8];  // Note : correction pour créer un tableau de 8 bits
            Serial.println("Entier non signé 8 bits (0 <= nb <= 255) à écrire :");

            while (!repValide) {
                while (!Serial.available()); // Attente d'une réponse
                reponse = Serial.readStringUntil('\n');
                repValide = testRepValide(reponse, 0, 255);
                if (repValide) {
                    // Transformation de la réponse en tableau de bits
                    byte* repBitsTemp = stringToIntToBytes(reponse);
                    for (int i = 0; i < 8; i++) {
                        repBits[i] = repBitsTemp[i];
                    }
                } else {
                    Serial.println("Valeur incorrecte, veuillez entrer un nombre entre 0 et 255.");
                }
            }

            // Position Ligne
            int ligne = -1;
            repValide = false;
            Serial.println("Ligne ? (Entre 1 et 128)");

            while (!repValide) {
                while (!Serial.available()); // Attente d'une réponse
                reponse = Serial.readStringUntil('\n');
                repValide = testRepValide(reponse, 1, 128);
                if (repValide) {
                    ligne = reponse.toInt();
                } else {
                    Serial.println("Valeur de ligne incorrecte, veuillez entrer un nombre entre 1 et 128.");
                }
            }

            // Position Colonne
            int colonne = -1;
            repValide = false;
            Serial.println("Colonne ? (Entre 1 et 16)");

            while (!repValide) {
                while (!Serial.available()); // Attente d'une réponse
                reponse = Serial.readStringUntil('\n');
                repValide = testRepValide(reponse, 1, 16);
                if (repValide) {
                    colonne = reponse.toInt();
                } else {
                    Serial.println("Valeur de colonne incorrecte, veuillez entrer un nombre entre 1 et 16.");
                }
            }

            // Codage
            Serial.println("Écriture en cours...");
            unPara(ligne); // Remet tous les bits de la ligne à 1

            // Placement des bits
            scBL(repBits, colonne); // Écriture de la colonne spécifiée avec les bits donnés

            Serial.println("Écriture réussie !");
            affMenu(false);

        } else if (repInt == 2) { // Lecture
            // Position Ligne
            int ligne = -1;
            bool repValide = false;
            Serial.println("Ligne ? (Entre 1 et 128)");

            while (!repValide) {
                while (!Serial.available()); // Attente d'une réponse
                reponse = Serial.readStringUntil('\n');
                repValide = testRepValide(reponse, 1, 128);
                if (repValide) {
                    ligne = reponse.toInt();
                } else {
                    Serial.println("Valeur de ligne incorrecte, veuillez entrer un nombre entre 1 et 128.");
                }
            }

            // Position Colonne
            int colonne = -1;
            repValide = false;
            Serial.println("Colonne ? (Entre 1 et 16)");

            while (!repValide) {
                while (!Serial.available()); // Attente d'une réponse
                reponse = Serial.readStringUntil('\n');
                repValide = testRepValide(reponse, 1, 16);
                if (repValide) {
                    colonne = reponse.toInt();
                } else {
                    Serial.println("Valeur de colonne incorrecte, veuillez entrer un nombre entre 1 et 16.");
                }
            }

            // Lecture
            int lu = lecture(ligne, colonne);
            Serial.print("Valeur lue : ");
            Serial.println(lu);

        } else if (repInt == 3) {
            Serial.println("Export des données (pas encore implémenté)...");
        } else {
            Serial.println("Option incorrecte, veuillez entrer un nombre entre 1 et 3.");
        }
    }
}
