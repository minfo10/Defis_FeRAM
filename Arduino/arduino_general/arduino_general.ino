#include <math.h> // Pour isNaN et autres fonctions mathématiques

// *** Manipulation directe des ports ***
#define pON(port, pin) (port |= bit(pin))    // Mettre le pin à l'état HAUT
#define pOFF(port, pin) (port &= ~bit(pin))  // Mettre le pin à l'état BAS
#define lect(port, pin) ((port) & bit(pin))  // Lire l'état du pin

// *** Déclaration des broches ***
const int WB = A0;          // Write Back
const int SA = A1;          // Sense Amplifier
const int SL = 2;           // Source Line
const int WL = 3;           // Word Line
const int PRE = 4;          // Precharge
const int BL = 5;           // Base Line
const int SET_PARA = 6;     // Set Parallel
const int CLOCK = 7;        // Clock
const int SC_IN = 8;        // Scan Chain IN
const int SC_OUT = 9;       // Scan Chain OUT
const int SC_SEL_ZERO = 10; // Scan Chain Select 0
const int SC_SEL_UN = 11;   // Scan Chain Select 1

// *** Setup : Configuration initiale ***
void setup() {
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

    Serial.begin(9600); // Initialisation de la communication série
    affMenu(true);      // Affiche le menu
}

// *** Boucle principale : Interface utilisateur ***
void loop(){
	// Ajouter vérification isNaN
	if(Serial.available() > 0){ // Attente d'une réponse de l'utilisateur
		String reponse = Serial.readStringUntil('\n');
		int repInt = reponse.toInt();

		// Menu interactif
        switch (repInt) {
            case 1:
                ecriture(); // Fonction pour écrire dans la mémoire
                break;
            case 2:
                lecture();  // Fonction pour lire dans la mémoire
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
void clk(){
    // Simule un coup d'horloge.	
	pON(PORTD, CLOCK);
	delayMicroseconds(2);
	pOFF(PORTD, CLOCK);
}

// *** Menu interactif ***
void affMenu(bool premAff) {
    if (!premAff) {
        Serial.println("\n");
    }
    Serial.println("1. Écriture");
    Serial.println("2. Lecture");
    Serial.println("3. Export des données contenues dans la mémoire vers un fichier .txt");
}

// *** Écriture dans la mémoire ***
void ecriture() {
    bool repValide = false;
    byte repBits;
    String reponse;

    // 1. Obtenir un entier à écrire
    Serial.println("Entier non signé 8 bits (0 <= nb <= 255) à écrire :");
    while (!repValide) {
        while (!Serial.available());
        reponse = Serial.readStringUntil('\n');
        repValide = testRepValide(reponse, 0, 255);
        repBits = stringToIntToBytes(reponse);
    }

    // 2. Obtenir la ligne et la colonne
    int ligne = obtenirPosition("Ligne ? (Entre 1 et 128)", 1, 128);
    int colonne = obtenirPosition("Colonne ? (Entre 1 et 16)", 1, 16);

    // 3. Codage de l'entier

          Serial.println("Écriture en cours...");
          unPara(ligne); // Remet tous les bits de la ligne à 1

            // Placement des bits
          scBL(repBits, colonne); // Écriture de la colonne spécifiée avec les bits donnés

          Serial.println("Écriture réussie !");
          affMenu(false);

}

// *** Lecture de la mémoire ***
void lecture() {
    // Obtenir la position de la cellule à lire
    int ligne = obtenirPosition("Ligne ? (Entre 1 et 128)", 1, 128);
    int colonne = obtenirPosition("Colonne ? (Entre 1 et 16)", 1, 16);

    // Demander à l'utilisateur si le write-back doit être activé
    Serial.println("Activer le write-back ? (1 = Oui, 0 = Non)");
    int writeBack = -1;
    while (writeBack < 0 || writeBack > 1) {
        while (!Serial.available()); // Attente d'une réponse
        String reponse = Serial.readStringUntil('\n');
        writeBack = reponse.toInt();
    }

    // Initialisation pour la lecture
    Serial.print("Lecture de la cellule en ligne ");
    Serial.print(ligne);
    Serial.print(", colonne ");
    Serial.println(colonne);
    if (writeBack == 1) {
        Serial.println("Write-back activé pour cette lecture.");
    } else {
        Serial.println("Write-back désactivé.");
    }

    // Sélectionner la ligne dans la chaîne de scan
    scWLSL(ligne);

    // Configuration des signaux pour la lecture
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

    // Lecture des 8 bits de la colonne spécifiée
    int valeur = 0;
    for (int i = 0; i < 8; i++) {
        clk();
        if (lect(PINB, SC_OUT) != 0) { // Si un '1' est détecté
            valeur += pow(2, i);
        }
    }

    // Gestion du write-back si activé
    if (writeBack == 1) {
        pON(PORTD, WB);
        clk();
        pOFF(PORTD, WB);
    }

    // Fin de la lecture
    clk();
    pOFF(PORTD, SL);
    pOFF(PORTD, SA);
    clk();
    pON(PORTD, PRE);
    clk();
    clk();
    pOFF(PORTD, WL);
    clk();
    pOFF(PORTD, PRE);
    clk();
    pOFF(PORTD, SET_PARA);
    clk();

    // Résultat de la lecture
    Serial.print("Valeur lue : ");
    Serial.println(valeur);
}



// *** Fonction auxiliaire : Obtenir une position ***
int obtenirPosition(const char* message, int min, int max) {
    String reponse;
    bool repValide = false;

    Serial.println(message);
    while (!repValide) {
        while (!Serial.available());
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

// *** Conversion d'un String en tableau de bits ***
byte stringToIntToBytes(String rep){
	int repInt = rep.toInt();
	byte repBits[8];
	for(byte i = 0; i < 8; i++){
		repBits[i] = ~ bitRead(repInt, i); // NOT bit --> Il est préférable de tout placer à 1 puis placer les 0 (cf fonction scBL)
	}
	return repBits;
}



// *** Sélection des lignes et colonnes ***
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

    for (int i = 0; i < 128; i++) {
        if (i >= startIndex && i < startIndex + 8) {
            int bitIndex = i - startIndex; // Index dans le tableau rep[8]

            if (rep[bitIndex] == 0) {
                pON(PORTB, SC_IN);
            } else {
                pOFF(PORTB, SC_IN);
            }

            // Ajout d'un délai avant l'impulsion du clock pour stabilisation
            delayMicroseconds(1);
            clk(); // Une seule impulsion d'horloge après avoir placé SC_IN

        } else {
            pOFF(PORTB, SC_IN);  // Assure que SC_IN est toujours en état bas lorsqu'on n'écrit pas de valeur
            delayMicroseconds(1);
            clk();
        }
    }

    Serial.print("Colonne ");
    Serial.print(colonne);
    Serial.println(" traitée.");
}



// *** Schémas pour coder les 0 et 1 ***
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
