// Arduino : ATmega8 et ATmega168
// -> 3 pins B (digital pin 8 to 13), C (analog input pins), D (digital pins 0 to 7)
// DDR = INPUT/OUTPUT, PORT = HIGH/LOW, PIN = Lecture
// https://docs.arduino.cc/hacking/software/PortManipulation

// OBJECTIF : Répondre un front montant après 3 impulsions de clk reçues.
#define pON(port, pin) (port |= bit(pin)) // port OR bit(pin) -> changement que sur pin souhaitÃ©.
#define pOFF(port, pin) (port &= ~ bit(pin)) // port AND NOT bit(pin)

const int IN = 3;
const int OUT = 4;
const int INport = 8; // 0001 0000

int cpt = 0;
int check = 0; // Retour à 0 après 3 fronts montants.

void setup(){
	pinMode(IN, INPUT);
	pinMode(OUT, OUTPUT);
}

void loop(){
	int lect = PORTD;
	if ((lect & INport) == 8){
		if(check == 0){
			cpt += 1;
			check = 1;
			if(cpt == 3){
				pON(PORTD, OUT);
				delay(3);
				pOFF(PORTD, OUT);
				cpt = 0;
			}
		}
		
	} else {
		check == 0;
	}

}