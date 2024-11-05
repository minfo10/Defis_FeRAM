# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 15:55:46 2021

@author: XuL
"""

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
        self.port_com = tk.StringVar(self, value="COM3")   # Port série
        self.baud_rate = tk.StringVar(self, value="9600")  # Vitesse de transmission
        # Champ d'entrée pour le baud rate
        Label_baud = tk.Label(self, text="Vitesse (baud rate)")
        Label_baud.grid(row=3, column=1)
        Outpout_baud = tk.Entry(self, textvariable=self.baud_rate, justify='center', width=10)
        Outpout_baud.grid(row=3, column=2)
        # Champ d'entrée pour le port COM
        Label_port = tk.Label(self, text="Port où l'Arduino est branchée")
        Label_port.grid(row=2, column=1)
        Outpout_port = tk.Entry(self, textvariable=self.port_com, justify='center', width=10)
        Outpout_port.grid(row=2, column=2)

        # Bouton quitter
        Button_quitter = tk.Button(self, text='Quitter', command=self.close, bg='firebrick1', width=8)
        Button_quitter.grid(row=13, column=4)


        # Write
        Title_write = tk.Label(self, text='Écriture', font='bold')
        Title_write.grid(row=5, column=2)
        Label_write = tk.Label(self, text='Texte à écrire:')
        Label_write.grid(row=6, column=1)

        self.write = tk.StringVar(self,'6')
        Entry = tk.Entry(self, textvariable=self.write, justify='center', width=20)
        Entry.grid(row=6, column=2)
        

        # Read
        Title_read = tk.Label(self, text='Lecture', font='bold')
        Title_read.grid(row=5, column=6)
        Label_read = tk.Label(self, text='Texte lu:')
        Label_read.grid(row=6, column=5)

        self.read = tk.StringVar(self, '')
        Outpout_txt2 = tk.Entry(self, textvariable=self.read, justify='center', width=20, state='readonly')
        Outpout_txt2.grid(row=6, column=6)
        

        # Ligne de séparation
        separator1 = ttk.Separator(self, orient='horizontal')
        separator1.grid(row=4, column=1, columnspan=8, pady=12, sticky='ew')
        separator2 = ttk.Separator(self, orient='vertical')
        separator2.grid(row=5, rowspan=6, column=4, sticky='ns')
        separator3 = ttk.Separator(self, orient='horizontal')
        separator3.grid(row=11, column=1, columnspan=8, pady=12, sticky='ew')
        
        # Bouton de lancement de lecture / écriture
        Button_write = tk.Button(self, text='Envoyer', bg='light blue', width=8)
        Button_write.grid(row=12, column=2)
        Button_read = tk.Button(self, text='Recevoir', bg='light green', width=8, command=self.update_text_loop)
        Button_read.grid(row=12, column=6)            


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

    def update_text_loop(self):

        port = self.port_com.get()  # Obtient le port de self.port_com
        baud = int(self.baud_rate.get())  # Convertit le baud rate en entier

        try:
            # Ouvre le port série
            ser = serial.Serial(port, baud)

            # Lit une ligne de données depuis le port série
            donnee = ser.readline().decode().strip()
            print(f"Donnée reçue depuis l'Arduino : {donnee}")

            # Écrit les données dans le fichier texte
            with open("data/exported_data.txt", "a") as fichier:
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