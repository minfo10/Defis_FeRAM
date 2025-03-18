# arduino/receive_data.py

import time
import serial
from tkinter import messagebox

# Fonction pour recevoir les données depuis l'arduino de controle
def receive_data(self):

        port = self.port_com.get()  # Obtient le port de self.port_com
        baud = int(self.baud_rate.get())  # Convertit le baud rate en entier

        try:
            # Ouvre le port série
            ser = serial.Serial(port, baud)

            ligne = int(self.rligne.get())
            colonne = int(self.rcolonne.get())

            time.sleep(5)

            # Envoyer le nombre à l'Arduino
            ser.write("2\n".encode())
            time.sleep(1)
            ser.write((str(ligne) + "\n").encode())
            time.sleep(1)
            ser.write((str(colonne) + "\n").encode())
            time.sleep(1)

            lines = []
            while True:
                try:
                    # Lire une ligne depuis le port série
                    donnee = ser.readline().decode().strip()  # Décodage et nettoyage
                    for i in range(0,4):
                        print(f"Donnée reçue : {ser.readline().decode().strip()}")
                    
                    if donnee :
                    # Ajouter la ligne à la liste
                        lines.append(donnee)

                    # Vérifier si nous avons au moins 6 lignes
                    if len(lines) >= 1:
                        # Si oui, lire la sixième ligne
                        derniere_ligne = lines[len(lines)-1]
                        print(f"{derniere_ligne}")
                        # Vous pouvez sortir de la boucle ou faire d'autres traitements ici
                    break  # Sortir de la boucle après avoir lu la sixième ligne

                except KeyboardInterrupt:
                    print("Arrêt de la lecture des données.")
                    break  # Quitte la boucle si l'utilisateur interrompt
                # Après la lecture, afficher toutes les lignes


            print("Toutes les lignes lues :")
            for i, line in enumerate(lines):
                print(f"Ligne {i+1}: {line}")

            # Écrit les données dans le fichier texte
            with open("data/exported_data.txt", "w") as fichier:
                fichier.write(f"{donnee}\n")
                fichier.flush()

            # Lecture du contenu du fichier texte pour l'afficher
            try:
                with open("data/exported_data.txt", "r") as file:
                    contenu = file.read()
            except FileNotFoundError:
                contenu = "Fichier non trouvé"
                
            # Mise à jour de l'Entry avec le contenu
            self.read.set(contenu)

        except serial.SerialException as e:
            # Affiche une boîte de message en cas de port indisponible
            messagebox.showerror("Erreur de port", f"{e}")

        finally:
            # Ferme le port série après la lecture
            if 'ser' in locals() and ser.is_open:
                ser.close()