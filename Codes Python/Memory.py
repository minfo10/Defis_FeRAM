# -*- coding: utf-8 -*-

import serial
import time

# Configuration du port série 
port = "COM3"  #Vérifier que c'est le port ou l'arduino est branchée
baudrate = 9600

# Ouvre le port série
ser = serial.Serial(port, baudrate)

# Crée un fichier texte pour enregistrer les données
with open("donnees_arduino.txt", "w") as fichier:
    while True:
        try:
            # Lecture des données depuis le port série
            donnee = ser.readline().decode().strip()  # Convertit les octets en chaîne de caractères
            print(f"Donnée reçue depuis l'Arduino : {donnee}")

            # Écriture dans le fichier texte
            fichier.write(f"{donnee}\n")
            fichier.flush()  # Force l'écriture immédiate dans le fichier

            # Attente avant la prochaine lecture
            time.sleep(1)  # Délai ajustable 
        except KeyboardInterrupt:
            print("Arrêt de la lecture.")
            break

# Ferme le port série
ser.close()
