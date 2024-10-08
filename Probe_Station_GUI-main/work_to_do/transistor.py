# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 16:09:53 2021

@author: XuL
"""

import os
import pyvisa
import time
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import ttk
import matplotlib.pyplot as plt

class Carac_transistor(tk.Tk):
    def __init__(self):
        
        # Initialisation de pyvisa, on cherche la SMU
        # rm = pyvisa.ResourceManager() 
        # self.inst = rm.open_resource(rm.list_resources()[0])
        # rm.read_termination='\n'
        # rm.write_termination='\n'
        self.inst='idk'
        
        # Initialisation de l'interface
        tk.Tk.__init__(self)
        self.title('Caractérisation du transistor') # Titre
        self.iconbitmap(os.getcwd() + '\icon.ico') # Icon de l'app
        
        # Couleur et background
        self.configure(background='light yellow')
        self.option_add('*font','arial 10') # Police par defaut
        self.option_add('*foreground','black')
        self.option_add('*Label*background','light yellow')
        self.option_add('*Entry*background','white')
        self.option_add('*OptionMenu*Menu*background','pale goldenrod')
        
        """
        La structure du code de haut en bas correspond à la structure de la fenêtre de gauche à droite.
        
        Pour faire des preset il faut configurer les valeurs des tk.variable (ex: tk.DoubleVar, tk.StringVar,...)
        """
        
        # Barre de menu
        self.menuBar = tk.Menu(self)
        self.config(menu=self.menuBar)
        self.menuSave = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Sauvegarder la mesure') 
        self.menuHelp = tk.Menu(self.menuBar, tearoff=0)
        self.menuBar.add_cascade(label='Help', menu=self.menuHelp)
        self.menuHelp.add_command(label='GitHub') 
        self.menuHelp.add_command(label='Crédit') 
        
        # Schema du transistor et des positionnements des pointes
        self.img = ImageTk.PhotoImage(Image.open(os.getcwd() + '\icon_transistor.png'))
        self.panel = tk.Label(self, image = self.img)
        self.panel.grid(row=0, column=4)
        
        # Channel 1 
        self.Title1 = tk.Label(self, text='Vd', font='bold', justify='center')
        self.separator1 = ttk.Separator(self, orient='horizontal')
        self.separator1.grid(row=3, column=1, columnspan=3, pady=6, sticky='ew')
        # Légendes des valeurs à entrer par l'utilisateur
        self.Label_min1 = tk.Label(self, text='min:')
        self.Label_max1 = tk.Label(self, text='max:')
        self.Label_nbPts1 = tk.Label(self, text='Nombre de points:')
        self.Label_compliance1 = tk.Label(self, text='Compliance:')
        # Setup des variables
        self.min1 = tk.DoubleVar(self, 0)
        self.max1 = tk.DoubleVar(self, 10)
        self.nbPoint1 = tk.IntVar(self, 100)
        self.compliance1 = tk.DoubleVar(self, 1)
        # Création des champs à compléter par l'utilisateur
        self.Entry_min1 = tk.Entry(self, textvariable=self.min1, justify='center', width=15)
        self.Entry_max1 = tk.Entry(self, textvariable=self.max1, justify='center', width=15)
        self.Entry_nbPoint1 = tk.Entry(self, textvariable=self.nbPoint1, justify='center', width=15)
        self.Entry_compliance1 = tk.Entry(self, textvariable=self.compliance1, justify='center', width=15)
        # Initialisation des ranges de mesure
        self.Range_min1 = tk.StringVar(self,'V')
        self.Range_max1 = tk.StringVar(self,'V')
        self.Range_comp1 = tk.StringVar(self,'mA')
        # Création de menus déroulant pour la selection de la range de mesure
        self.Deroulant_Range_min1 = tk.OptionMenu(self, self.Range_min1, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        self.Deroulant_Range_min1.config(width=3)
        self.Deroulant_Range_max1 = tk.OptionMenu(self, self.Range_max1, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        self.Deroulant_Range_comp1 = tk.OptionMenu(self, self.Range_comp1, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        
        # Placement des éléments sur la grille
        self.Title1.grid(row=2, column=1, columnspan=3)
        self.Label_min1.grid(row=4, column=1)
        self.Entry_min1.grid(row=4, column=2)
        self.Deroulant_Range_min1.grid(row=4, column=3, sticky="ew")
        self.Label_max1.grid(row=5, column=1)
        self.Entry_max1.grid(row=5, column=2)
        self.Deroulant_Range_max1.grid(row=5, column=3, sticky="ew")
        self.Label_compliance1.grid(row=6, column=1)
        self.Entry_compliance1.grid(row=6, column=2)
        self.Deroulant_Range_comp1.grid(row=6, column=3, sticky="ew")
        self.Label_nbPts1.grid(row=7, column=1)
        self.Entry_nbPoint1.grid(row=7, column=2)
        
        # Channel 2
        self.Title2 = tk.Label(self, text='Vg', font='bold', justify='center')
        self.sep2 = ttk.Separator(self, orient='horizontal')
        self.sep2.grid(row=3, column=5, columnspan=7, pady=6, sticky='ew')
        # Légendes des valeurs à entrer par l'utilisateur
        self.Label_min2 = tk.Label(self, text='min:')
        self.Label_max2 = tk.Label(self, text='max:')
        self.Label_nbPts2 = tk.Label(self, text='Nombre de points:')
        self.Label_compliance2 = tk.Label(self, text='Compliance:')
        # Setup des variables
        self.min2 = tk.DoubleVar(self, 3)
        self.max2 = tk.DoubleVar(self, 5)
        self.nbPoint2 = tk.IntVar(self, 3)
        self.compliance2 = tk.DoubleVar(self, 1)
        # Création des champs à compléter par l'utilisateur
        self.Entry_min2 = tk.Entry(self, textvariable=self.min2, justify='center', width=15)
        self.Entry_max2 = tk.Entry(self, textvariable=self.max2, justify='center', width=15)
        self.Entry_nbPoint2 = tk.Entry(self, textvariable=self.nbPoint2, justify='center', width=15)
        self.Entry_compliance2 = tk.Entry(self, textvariable=self.compliance2, justify='center', width=15)
        # Initialisation des ranges de mesure
        self.Range_min2 = tk.StringVar(self,'V')
        self.Range_max2 = tk.StringVar(self,'V')
        self.Range_comp2 = tk.StringVar(self,'mA')
        # Création de menus déroulant pour la selection de la range de mesure
        self.Deroulant_Range_min2 = tk.OptionMenu(self, self.Range_min2, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        self.Deroulant_Range_min2.config(width=3)
        self.Deroulant_Range_max2 = tk.OptionMenu(self, self.Range_max2, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        self.Deroulant_Range_comp2 = tk.OptionMenu(self, self.Range_comp2, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        # Placement des éléments sur la grille
        self.Title2.grid(row=2, column=5, columnspan=7)
        self.Label_min2.grid(row=4, column=5)
        self.Entry_min2.grid(row=4, column=6)
        self.Deroulant_Range_min2.grid(row=4, column=7, sticky="ew")
        self.Label_max2.grid(row=5, column=5)
        self.Entry_max2.grid(row=5, column=6)
        self.Deroulant_Range_max2.grid(row=5, column=7, sticky="ew")
        self.Label_compliance2.grid(row=6, column=5)
        self.Entry_compliance2.grid(row=6, column=6)
        self.Deroulant_Range_comp2.grid(row=6, column=7, sticky="ew")
        self.Label_nbPts2.grid(row=7, column=5)
        self.Entry_nbPoint2.grid(row=7, column=6)
        
        # Ligne de séparation
        self.separator1 = ttk.Separator(self, orient='horizontal')
        self.separator1.grid(row=1, column=1, columnspan=7, pady=10, sticky='ew')
        self.separator2 = ttk.Separator(self, orient='vertical')
        self.separator2.grid(row=2, rowspan=6, column=4, sticky='ns')
        self.separator3 = ttk.Separator(self, orient='horizontal')
        self.separator3.grid(row=8, column=1, columnspan=7, pady=10, sticky='ew')
        
        # Temps de relaxation
        self.TpsRelaxation = tk.Label(self, text='Tps de relaxation (en ms):')
        self.deltaT = tk.DoubleVar(self, 10) # La SMU prend des valeurs en second il faut donc diviser par 1000 plus tard
        self.Entry_relaxation = tk.Entry(self, textvariable=self.deltaT, justify='center', width=15)
        self.TpsRelaxation.grid(row=10, column=1)
        self.Entry_relaxation.grid(row=10, column=2)
        # Bouton de lancement de mesure
        self.LETS_GO = tk.Button(self, text='Validation', bg='yellow green', width=8)
        self.LETS_GO.grid(row=9, column=4)
        # Bouton pour fermer l'interface
        self.RAGE_QUIT = tk.Button(self, text='Quitter', command=self.close, bg='firebrick1', width=8)
        self.RAGE_QUIT.grid(row=10, column=4)
            
    def close(self):
        # self.inst.write(":OUTP1 OFF")
        # self.inst.write(":OUTP2 OFF")
        self.destroy()
        
start = Carac_transistor()
start.mainloop()