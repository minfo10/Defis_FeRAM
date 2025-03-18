# arduino/send_data.py

import time
import serial
from tkinter import messagebox

# Fonction pour envoyer les données vers l'arduino de controle
def send_data(self):
        
        port = self.port_com.get()  # Obtient le port de self.port_com
        baud = int(self.baud_rate.get())  # Convertit le baud rate en entier

        # Nombre à envoyer
        number_to_send = int(self.write.get())
        ligne = int(self.wligne.get())
        colonne = int(self.wcolonne.get())
        
        try:
            # Ouvre le port série
            ser = serial.Serial(port, baud)
            time.sleep(2)  # Attendre que la connexion s'établisse

            delay = 0.1

            # Envoyer le nombre à l'Arduino
            ser.write("1\n".encode())
            time.sleep(delay)
            ser.write((str(number_to_send) + "\n").encode())
            time.sleep(delay)
            ser.write((str(ligne) + "\n").encode())
            time.sleep(delay)
            ser.write((str(colonne) + "\n").encode())


            lines = []
            while True:
                try:
                    # Lire une ligne depuis le port série
                    donnee = ser.readline().decode().strip()  # Décodage et nettoyage
                    for i in range(0,10):
                        print(f"{ser.readline().decode().strip()}")

                    # Ajouter la ligne à la liste
                    lines.append(donnee)

                    # Vérifier si nous avons au moins 6 lignes
                    if len(lines) == 7:
                        # Si oui, lire la septième ligne
                        derniere_ligne = lines[6]
                        messagebox.showinfo("Info",f"{derniere_ligne}")
                        # Vous pouvez sortir de la boucle ou faire d'autres traitements ici
                    break  # Sortir de la boucle après avoir lu la sixième ligne
                except ValueError:
                    messagebox.showerror("Erreur de valeur", f"Veuillez entrer un nombre valide.")

        except serial.SerialException as e:
            # Affiche une boîte de message en cas de port indisponible
            messagebox.showerror("Erreur de port", f"{e}")

        finally:
            # Fermer le port série
            if 'ser' in locals() and ser.is_open:
                ser.close()