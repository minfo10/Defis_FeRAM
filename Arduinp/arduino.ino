#include <math.h> // Utile pour isNaN

// Manipulation directe des ports
#define pON(port, pin) (port |= bit(pin)) // port OR bit(pin) - Passage à l'état HAUT
#define pOFF(port, pin) (port &= ~ bit(pin)) // port AND NOT bit(pin) - Passage à l'état BAS
#define lect(port, pin) (port &= bit(pin)) // port AND bit(pin) - Lecture

// Pins à brancher.
const int WB = 0;
const int SA = 1;
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
	delayMicroseconds(1);
	pOFF(PORTD, CLOCK);
}

void scWLSL(int ligne){
	// Permet la sélection de la ligne sur laquelle les opérations de lecture et d'écriture vont être effectuées.

	// Amélioration possible : usage tableaux dynamiques entrée utilisateur pour selection plusieurs lignes
	// (et donc stockage potentiel de nombres codés sur + que 128 bits)

	// Sélection de la bonne Scan Chain (cf 4.4.2.1 de la thèse de Mr Francois)
	pON(PORTB, SC_SEL_ZERO);
	pOFF(PORTB, SC_SEL_UN);


	for(int i = 0; i < 128; i++){
		if(i == ligne){ // Si la i-ième ligne est la ligne choisie
			pON(PORTB, SC_IN);
			clk();
			pOFF(PORTB, SC_IN);
		} else clk();
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

void scBL(byte rep[8], int colonne){
	// cf implémentation de l'écriture unitaire
	// A VERIFIER SUR CARTE -----------------------------------------------
	pOFF(PORTB, SC_SEL_ZERO);
	pON(PORTB, SC_SEL_UN);

	for(int i = 0; i < 120; i++){
		if(i == (colonne - 1) * 8){
			for(int j = 0; j < 8; j++){
				if(rep[j] == 0){
					pON(PORTB, SC_IN);
					clk();
					pOFF(PORTB, SC_IN);
				} else clk();
			}
		} else {
			pON(PORTB, SC_IN);
			clk();
			pOFF(PORTB, SC_IN);
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

void lectCellule(int ligne, int writeBack){
	// Lecture du contenu d'une ligne.
	// writeBack == 1 active le Write-Back. L'opération de lecture étant normalement destructive,
	// ce paramètre doit être activé si l'on souhaite réutiliser plus tard le contenu de la ligne.

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
	if(writeBack == 1){
		pON(PORTD, WB);
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
		for(int i = 0; i < 8; i++){
		lectCellule(ligne, (colonne - 1) * 8);
		if(lect(PINB, SC_OUT) != 0){
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

void setup(){
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

void loop(){
	// Ajouter vérification isNaN
	if(Serial.available() > 0){ // Attente d'une réponse de l'utilisateur
		String reponse = Serial.readStringUntil('\n');
		int repInt = reponse.toInt();

		// Switch bugué ici.
		if(repInt == 1){ // Ecriture d'un entier 8bits (pour l'instant, objectif stocker float https://en.wikipedia.org/wiki/Quadruple-precision_floating-point_format)
			// Nombre à coder.
			bool repValide = false;
			byte repBits;
			Serial.println("Entier non signé 8 bits (0 <= nb <= 255) à écrire :");
			while(not repValide){	 
				while(!Serial.available());// Attente d'une réponse
				reponse = Serial.readStringUntil('\n');
				repValide = testRepValide(reponse, 0, 255);
				repBits = stringToIntToBytes(reponse);
			}
			

			// Position.

				// Ligne
			int ligne = -1;
			repValide = false;
			Serial.println("Ligne ? (Entre 1 et 128)");
			while(not repValide){
				while(!Serial.available());// Attente d'une réponse
				reponse = Serial.readStringUntil('\n');
				repValide = testRepValide(reponse, 1, 128);
				ligne = reponse.toInt();
			}

			
				// Colonne
			int colonne = -1;
			repValide = false;
			Serial.println("Colonne ? (Entre 1 et 16)"); 
			while(not repValide){
				while(!Serial.available());// Attente d'une réponse
				reponse = Serial.readStringUntil('\n');
				repValide = testRepValide(reponse, 1, 16);
				colonne = reponse.toInt();
			}
			

			// Codage.
			// Remise à 1.
			byte* queDes1 = '11111111';
			scBL(queDes1, (colonne - 1) * 8); // Remise à 1 de l'octet.
			unPara(ligne); // scWLSL déjà dans unPara.

			// Placement des 0.
			scBL(repBits, (colonne - 1) * 8);
			zeroUnitaire();

			Serial.println("Écriture réussie !");
			affMenu(false);

		} else if(repInt == 2){
			// Position.
			int ligne = -1;
			bool repValide = false;
			while(not repValide){
				Serial.println("Ligne ? (Entre 1 et 128)"); 
				while(!Serial.available());// Attente d'une réponse
				reponse = Serial.readStringUntil('\n');
				repValide = testRepValide(reponse, 1, 128);
				ligne = reponse.toInt();
			} 
			
			int colonne = -1;
			repValide = false;
			while(not repValide){
				Serial.println("Colonne ? (Entre 1 et 16)"); 
				while(!Serial.available());// Attente d'une réponse
				reponse = Serial.readStringUntil('\n');
				repValide = testRepValide(reponse, 1, 16);
				colonne = reponse.toInt();
			}
			
			// Lecture.
			int lu = lecture(ligne, colonne);
			Serial.println(lu);

		} else if(repInt == 3){
			Serial.println("//");
		} else {
			Serial.println("Incorrect");
		}
	}
}