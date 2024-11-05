// Arduino : ATmega8 et ATmega168
// -> 3 pins B (digital pin 8 to 13), C (analog input pins), D (digital pins 0 to 7)
// DDR = INPUT/OUTPUT, PORT = HIGH/LOW, PIN = Lecture
// https://docs.arduino.cc/hacking/software/PortManipulation

#define pON(port, pin) (port |= bit(pin)) // port OR bit(pin) -> changement que sur pin souhaité.
#define pOFF(port, pin) (port &= ~ bit(pin)) // port AND NOT bit(pin)

const int CLOCK = 7; // Définit la broche pour l'horloge
const int SC_OUT = 9; // Définit la broche de sortie de signal de contrôle

// Vérifiez que cette valeur correspond au bit correct de la broche SC_OUT sur PORTB
const int SC_OUTport = (1 << 1); // 0000 0010 pour le bit 1 de PORTB, selon le câblage physique

int checkDebug = 1;
int sRead = 0;

void clk() {
  // Génère une impulsion d'horloge
  pON(PORTD, CLOCK);
  delayMicroseconds(2); // Durée de l'impulsion
  pOFF(PORTD, CLOCK);
  delayMicroseconds(2);
}

void setup() {
  pinMode(CLOCK, OUTPUT); // Définit l'horloge comme sortie
  pinMode(SC_OUT, INPUT); // Définit la broche SC_OUT comme entrée
  Serial.begin(9600); // Initialise la communication série
}

void loop() {
  if (checkDebug == 1) {
    // Mode débugage, attend l'entrée de l'utilisateur via le port série
    sRead = 0;
    while (Serial.available() == 0) {
      // Attend une commande utilisateur
    }
    sRead = Serial.read() - '0'; // Conversion du caractère en nombre entier

    Serial.print("Received: "); 
    Serial.println(sRead); // Affiche la valeur reçue pour débogage
    
    checkDebug = 0;
  } else {
    if (sRead == 1) {
      Serial.println("ok"); // Affiche "ok" lorsque '1' est reçu
      // Trois impulsions d'horloge pour l'initialisation
      clk();
      clk();
      clk();
      checkDebug = 0;
      sRead = 2;
    } else if (sRead == 2) {
      // Lit la valeur de PORTB
      int lect = PINB; // Correction: utilisation correcte de PINB pour lire le port

      // Vérifie si le bit SC_OUTport est élevé
      if ((lect & SC_OUTport) == SC_OUTport) {
        Serial.println("Wooooo");
        checkDebug = 1;
      }
    }
  }
}
