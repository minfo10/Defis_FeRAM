import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import webbrowser
import Importation
import Exportation
import serial
import time

class AppWindow(tk.Tk):
    def __init__(self, inst):
        
        self.inst = inst
        
        # Initialisation de l'interface
        tk.Tk.__init__(self)
        self.title('Défi FeRAM') # Titre
        self.iconbitmap(os.getcwd() + '\icon.ico') # Icon de l'app
        self.geometry('700x300')
        
        # Couleur et background
        self.configure(background='light gray')
        self.option_add('*font','arial 10') # Police par defaut
        self.option_add('*foreground','black')
        self.option_add('*Label*background','light gray')
        self.option_add('*Entry*background','white')
        self.option_add('*OptionMenu*Menu*background','pale goldenrod')
        
        """
        La structure du code de haut en bas correspond à la structure de la fenêtre de gauche à droite.
        
        Pour faire des preset il faut configurer les valeurs des tk.variable (ex: tk.DoubleVar, tk.StringVar,...)
        """
        
        # Barre de menu
        menuBar = tk.Menu(self)
        self.config(menu=menuBar)

        menuData = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Data', menu=menuData)
        menuData.add_command(label="Exporter en .txt", command=self.exportation)
        menuData.add_command(label="Importer en .txt", command=self.importation)

        menuReset = tk.Menu(menuBar, tearoff=0) 
        menuBar.add_cascade(label='Arduino', menu=menuReset)
        menuData.add_command(label="Reset")

        menuHelp = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Help', menu=menuHelp)
        menuHelp.add_command(label='GitHub', command=self.open_github)
        
        # First line
        Label_info_connection = tk.Label(self, text='Information de connection')
        Label_info_connection.grid(row=0, column=1)
        # Variables pour le port et le baud rate
        self.port_com = tk.StringVar(self, value="COM6")   # Port série
        self.baud_rate = tk.StringVar(self, value="9600")  # Vitesse de transmission
        # Champ d'entrée pour le baud rate
        Label_baud = tk.Label(self, text="Vitesse (baud rate)")
        Label_baud.grid(row=3, column=1)
        Outpout_baud = tk.Entry(self, textvariable=self.baud_rate, justify='center', width=10)
        Outpout_baud.grid(row=3, column=2)
        # Champ d'entrée pour le port COM
        Label_port = tk.Label(self, text="Port de l'Arduino")
        Label_port.grid(row=2, column=1)
        Outpout_port = tk.Entry(self, textvariable=self.port_com, justify='center', width=10)
        Outpout_port.grid(row=2, column=2)

        # Bouton quitter
        Button_quitter = tk.Button(self, text='Quitter', command=self.close, bg='firebrick1', width=8)
        Button_quitter.grid(row=15, column=4)


        # Write
        Title_write = tk.Label(self, text='Écriture', font='bold')
        Title_write.grid(row=5, column=2)
        Label_write = tk.Label(self, text='Entier non signé 8 bits (0 <= nb <= 255)')
        Label_write.grid(row=6, column=1)
        self.write = tk.StringVar(self,'12')
        Entry = tk.Entry(self, textvariable=self.write, justify='center', width=10)
        Entry.grid(row=6, column=2)
        #ligne
        Label_wligne = tk.Label(self, text='Ligne ? (Entre 1 et 128)')
        Label_wligne.grid(row=7, column=1)
        self.wligne = tk.StringVar(self,'1')
        Ligne = tk.Entry(self, textvariable=self.wligne, justify='center', width=10)
        Ligne.grid(row=7, column=2)
        #colonne
        Label_wcolonne = tk.Label(self, text='Colonne ? (Entre 1 et 16)')
        Label_wcolonne.grid(row=8, column=1)
        self.wcolonne = tk.StringVar(self,'1')
        Colonne = tk.Entry(self, textvariable=self.wcolonne, justify='center', width=10)
        Colonne.grid(row=8, column=2)
        

        # Read
        Title_read = tk.Label(self, text='Lecture', font='bold')
        Title_read.grid(row=5, column=6)
        Label_read = tk.Label(self, text='Texte lu:')
        Label_read.grid(row=8, column=5)
        self.read = tk.StringVar(self, '')
        Outpout_txt2 = tk.Entry(self, textvariable=self.read, justify='center', width=10, state='readonly')
        Outpout_txt2.grid(row=8, column=6)        
        #ligne
        Label_rligne = tk.Label(self, text='Ligne ? (Entre 1 et 128)')
        Label_rligne.grid(row=6, column=5)
        self.rligne = tk.StringVar(self,'1')
        Ligne = tk.Entry(self, textvariable=self.rligne, justify='center', width=10)
        Ligne.grid(row=6, column=6)
        #colonne
        Label_rcolonne = tk.Label(self, text='Colonne ? (Entre 1 et 16)')
        Label_rcolonne.grid(row=7, column=5)
        self.rcolonne = tk.StringVar(self,'1')
        Colonne = tk.Entry(self, textvariable=self.rcolonne, justify='center', width=10)
        Colonne.grid(row=7, column=6)
        

        # Ligne de séparation
        separator1 = ttk.Separator(self, orient='horizontal')
        separator1.grid(row=4, column=1, columnspan=8, pady=12, sticky='ew')
        separator2 = ttk.Separator(self, orient='vertical')
        separator2.grid(row=5, rowspan=8, column=4, sticky='ns')
        separator3 = ttk.Separator(self, orient='horizontal')
        separator3.grid(row=13, column=1, columnspan=8, pady=12, sticky='ew')
        
        # Bouton de lancement de lecture / écriture
        Button_write = tk.Button(self, text='Envoyer', bg='light blue', width=8, command=self.send_data)
        Button_write.grid(row=14, column=2)
        Button_read = tk.Button(self, text='Recevoir', bg='light green', width=8, command=self.receive_data)
        Button_read.grid(row=14, column=6)            


    # Différentes fonctions
    def exportation(self):
            exportWindow = Exportation.ExportInterface()    
            exportWindow.mainloop()

    def importation(self):
            exportWindow = Importation.ImportInterface()
            exportWindow.mainloop()

    def open_github(self):
    # Ouvre le lien GitHub dans le navigateur par défaut
        webbrowser.open("https://github.com/minfo10/Defis_FeRAM")

    def close(self):
        self.destroy()


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
            ser.write(f"{2}\n".encode())
            time.sleep(1)
            ser.write(f"{ligne}\n".encode())
            time.sleep(1)
            ser.write(f"{colonne}\n".encode())
            time.sleep(1)

            lines = []
            while True:
                try:
                    # Lire une ligne depuis le port série
                    donnee = ser.readline().decode().strip()  # Décodage et nettoyage
                    print(f"Donnée reçue : {donnee}")
                    
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

            # Envoyer le nombre à l'Arduino
            ser.write(f"{1}\n".encode())
            time.sleep(1)
            ser.write(f"{number_to_send}\n".encode())
            time.sleep(1)
            ser.write(f"{ligne}\n".encode())
            time.sleep(1)
            ser.write(f"{colonne}\n".encode())


            lines = []
            while True:
                try:
                    # Lire une ligne depuis le port série
                    donnee = ser.readline().decode().strip()  # Décodage et nettoyage
                    print(f"Donnée reçue : {donnee}")
                    
                    # Ajouter la ligne à la liste
                    lines.append(donnee)

                    # Vérifier si nous avons au moins 6 lignes
                    if len(lines) == 7:
                        # Si oui, lire la septième ligne
                        derniere_ligne = lines[6]
                        messagebox.showinfo("Info",f"{derniere_ligne}")
                        # Vous pouvez sortir de la boucle ou faire d'autres traitements ici
                    break  # Sortir de la boucle après avoir lu la sixième ligne
        

                except serial.SerialException as e:
                    messagebox.showerror("Erreur de port", f"{e}")

                except ValueError:
                    messagebox.showerror("Erreur de valeur", f"Veuillez entrer un nombre valide.")

        finally:
            # Fermer le port série
            ser.close()


            #I have an issue, my arduino cannot read the data i sent it and when i try to get serial data, it only shows me the first line. Can you help me and maybe do a clean