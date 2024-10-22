# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 15:55:46 2021

@author: XuL
"""

import os
import tkinter as tk
from tkinter import ttk
import webbrowser
import Importation
import Exportation

class AppWindow(tk.Tk):
    def __init__(self, inst):
        
        self.inst = inst
        
        # Initialisation de l'interface
        tk.Tk.__init__(self)
        self.title('Défi FeRAM') # Titre
        self.iconbitmap(os.getcwd() + '\icon.ico') # Icon de l'app
        self.geometry('600x300')
        
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
        Label_txt1 = tk.Label(self, text='Information de connection')
        Label_txt1.grid(row=0, column=1)

        # Bouton quitter
        Button_quitter = tk.Button(self, text='Quitter', command=self.close, bg='firebrick1', width=8)
        Button_quitter.grid(row=10, column=4)


        # Write
        Title1 = tk.Label(self, text='Écriture', font='bold')
        Title1.grid(row=2, column=2)
        Label_txt1 = tk.Label(self, text='Texte à écrire:')
        Label_txt1.grid(row=3, column=1)
        self.txt1 = tk.StringVar(self,'6')
        Entry_txt1 = tk.Entry(self, textvariable=self.txt1, justify='center', width=30)
        Entry_txt1.grid(row=3, column=2)
        
        # Read
        Title2 = tk.Label(self, text='Lecture', font='bold')
        Title2.grid(row=2, column=6)
        self.txt2 = tk.StringVar(self,'')
        Outpout_txt2 = tk.Entry(self, textvariable=self.txt2, justify='center', width=30)
        Outpout_txt2.grid(row=3, column=6)
        Label_txt2 = tk.Label(self, text='Texte lu:')
        Label_txt2.grid(row=3, column=5)
        
        # Ligne de séparation
        separator1 = ttk.Separator(self, orient='horizontal')
        separator1.grid(row=1, column=1, columnspan=7, pady=10, sticky='ew')
        separator2 = ttk.Separator(self, orient='vertical')
        separator2.grid(row=2, rowspan=6, column=4, sticky='ns')
        separator3 = ttk.Separator(self, orient='horizontal')
        separator3.grid(row=8, column=1, columnspan=7, pady=10, sticky='ew')
        
        # Bouton de lancement de lecture / écriture
        Button_write = tk.Button(self, text='Envoyer', bg='light blue', width=8)
        Button_write.grid(row=9, column=2)
        Button_read = tk.Button(self, text='Recevoir', bg='light green', width=8)
        Button_read.grid(row=9, column=6)
            


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


    