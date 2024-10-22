// Arduino : ATmega8 et ATmega168
// -> 3 pins B (digital pin 8 to 13), C (analog input pins), D (digital pins 0 to 7)
// DDR = INPUT/OUTPUT, PORT = HIGH/LOW, PIN = Lecture
// https://docs.arduino.cc/hacking/software/PortManipulation

#define pON(port, pin) (port |= bit(pin)) // port OR bit(pin) -> changement que sur pin souhaitÃ©.
#define pOFF(port, pin) (port &= ~ bit(pin)) // port AND NOT bit(pin)

// digitalWrite Tmin > 4us

const int CLOCK = 7;
const int SC_OUT = 9; // 0100 0000 -> 2d

const int SC_OUTport = 2;

int checkDebug = 1;

int sRead = 0;

void clk(){
	pON(PORTD, CLOCK);
	delayMicroseconds(2);
	pOFF(PORTD, CLOCK);
	delayMicroseconds(2);
}

void setup(){
	pinMode(CLOCK, OUTPUT);
	pinMode(SC_OUT, INPUT);
	Serial.begin(9600);
}

void loop() {
	if(checkDebug == 1){
		sRead = 0;
		while(Serial.available() == 0){
			// Mode débuggage.
		}
		sRead = Serial.read();
		checkDebug = 0;
	} else {
		if (sRead == 1) {
			clk();
			clk();
			clk();
			checkDebug = 0; // Rentre directement dans le switch
			sRead = 2;}
		else if(sRead == 2){
			int lect = PORTB;
				if((lect & SC_OUTport) == SC_OUTport){
					Serial.write("Wooooo");
					checkDebug = 1;
			}
		}
		}
	}
