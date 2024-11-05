// Arduino : ATmega8 et ATmega168
// -> 3 pins B (digital pin 8 to 13), C (analog input pins), D (digital pins 0 to 7)
// DDR = INPUT/OUTPUT, PORT = HIGH/LOW, PIN = Lecture
// https://docs.arduino.cc/hacking/software/PortManipulation

// OBJECTIF : Répondre un front montant après 3 impulsions de clk reçues.
#define pON(port, pin) (port |= bit(pin)) // port OR bit(pin) -> changement que sur pin souhaité.
#define pOFF(port, pin) (port &= ~ bit(pin)) // port AND NOT bit(pin)

const int IN = 3; // Définit la broche pour l'entrée de l'impulsion
const int OUT = 4; // Définit la broche pour la sortie de l'impulsion

// Correction: vérifiez que cette valeur correspond au bit correct de la broche IN sur PORTD
const int INport = (1 << IN); // 0000 1000 pour le bit correspondant à la broche 3 sur PORTD

int cpt = 0;
int check = 0; // Retour à 0 après 3 fronts montants.

void setup() {
  pinMode(IN, INPUT); // Définit la broche IN comme entrée
  pinMode(OUT, OUTPUT); // Définit la broche OUT comme sortie
}

void loop() {
  // Lecture de l'état de PORTD
  int lect = PIND; // Correction: utilisation de PIND pour lire l'état actuel du port

  // Vérifie si la broche IN est élevée (front montant)
  if ((lect & INport) == INport) {
    if (check == 0) {
      cpt += 1; // Incrémente le compteur sur un front montant détecté
      check = 1;
      if (cpt == 3) {
        // Après 3 fronts montants, active la broche OUT
        pON(PORTD, OUT);
        delay(3); // Délai de 3 ms (ajustable selon les besoins)
        pOFF(PORTD, OUT);
        cpt = 0; // Réinitialise le compteur
      }
    }
  } else {
    // Réinitialise l'indicateur pour détecter le prochain front montant
    check = 0;
  }
}
