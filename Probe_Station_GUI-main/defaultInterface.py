# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 15:55:46 2021

@author: XuL
"""

import os
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from FenTracer import Reglage, FenTracerVar
import ExportData

class AppWindow(tk.Tk):
    def __init__(self, inst):
        
        self.inst = inst
        self.FenVar = None
        
        # Initialisation de l'interface
        tk.Tk.__init__(self)
        self.title('Réglage channel') # Titre
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
        menuBar = tk.Menu(self)
        self.config(menu=menuBar)
        menuSave = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Sauvegarder la mesure', menu=menuSave)
        menuSave.add_command(label="Exporter en .txt", command=self.interface2export)
        menuCarac = tk.Menu(menuBar, tearoff=0) 
        menuBar.add_cascade(label='Caractérisation', menu=menuCarac) 
        menuCarac.add_command(label='Transistor') 
        menuCarac.add_command(label='Diode') 
        menuCarac.add_command(label='Résistance')
        menuCarac.add_command(label='Ionisation par impact (soon)')
        menuHelp = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Help', menu=menuHelp)
        menuHelp.add_command(label='GitHub') 
        menuHelp.add_command(label='Crédit') 
        
        # Channel 1 
        Title1 = tk.Label(self, text='CHANNEL 1', font='bold')
        self.name1 = tk.StringVar(self,'name1')
        Entry_name1 = tk.Entry(self, textvariable=self.name1, justify='center', width=15)
        # Sélection de la grandeur mesurée
        Label_grandeurImposee1 = tk.Label(self, text='Grandeur à imposer:')
        self.grandeur_imposee1 = tk.StringVar(self,'Tension')
        Deroulant_grandeurImposee1 = tk.OptionMenu(self, self.grandeur_imposee1, 'Intensité', 'Tension')
        # Légendes des valeurs à entrer par l'utilisateur
        Label_min1 = tk.Label(self, text='min:')
        Label_max1 = tk.Label(self, text='max:')
        Label_nbPts1 = tk.Label(self, text='Nombre de points:')
        Label_compliance1 = tk.Label(self, text='Compliance:')
        # Setup des variables
        self.min1 = tk.DoubleVar(self, -20)
        self.max1 = tk.DoubleVar(self, 40)
        self.nbPoint1 = tk.IntVar(self, 100)
        self.compliance1 = tk.DoubleVar(self, 100)
        # Création des champs à compléter par l'utilisateur
        Entry_min1 = tk.Entry(self, textvariable=self.min1, justify='center', width=15)
        Entry_max1 = tk.Entry(self, textvariable=self.max1, justify='center', width=15)
        Entry_nbPoint1 = tk.Entry(self, textvariable=self.nbPoint1, justify='center', width=15)
        Entry_compliance1 = tk.Entry(self, textvariable=self.compliance1, justify='center', width=15)
        # Initialisation des ranges de mesure
        self.Range_min1 = tk.StringVar(self,'V')
        self.Range_max1 = tk.StringVar(self,'V')
        self.Range_comp1 = tk.StringVar(self,'mA')
        # Création de menus déroulant pour la selection de la range de mesure
        Deroulant_Range_min1 = tk.OptionMenu(self, self.Range_min1, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        Deroulant_Range_min1.config(width=3)
        Deroulant_Range_max1 = tk.OptionMenu(self, self.Range_max1, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        Deroulant_Range_comp1 = tk.OptionMenu(self, self.Range_comp1, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        
        # Placement des éléments sur la grille
        Title1.grid(row=1, column=1)
        Entry_name1.grid(row=1, column=2)
        Label_grandeurImposee1.grid(row=2, column=1)
        Deroulant_grandeurImposee1.grid(row=2, column=2, sticky="ew")
        Label_min1.grid(row=3, column=1)
        Entry_min1.grid(row=3, column=2)
        Deroulant_Range_min1.grid(row=3, column=3, sticky="ew")
        Label_max1.grid(row=4, column=1)
        Entry_max1.grid(row=4, column=2)
        Deroulant_Range_max1.grid(row=4, column=3, sticky="ew")
        Label_compliance1.grid(row=5, column=1)
        Entry_compliance1.grid(row=5, column=2)
        Deroulant_Range_comp1.grid(row=5, column=3, sticky="ew")
        Label_nbPts1.grid(row=6, column=1)
        Entry_nbPoint1.grid(row=6, column=2)
        
        # Channel 2
        Title2 = tk.Label(self, text='CHANNEL 2', font='bold')
        self.name2 = tk.StringVar(self,'name2')
        Entry_name2 = tk.Entry(self, textvariable=self.name2, justify='center', width=15)
        # Sélection de la grandeur mesurée
        Label_grandeurImposee2 = tk.Label(self, text='Grandeur à imposer:')
        self.grandeur_imposee2 = tk.StringVar(self,'Tension')
        Deroulant_grandeurImposee2 = tk.OptionMenu(self, self.grandeur_imposee2, 'Intensité', 'Tension')
        # Légendes des valeurs à entrer par l'utilisateur
        Label_min2 = tk.Label(self, text='min:')
        Label_max2 = tk.Label(self, text='max:')
        Label_nbPts2 = tk.Label(self, text='Nombre de points:')
        Label_compliance2 = tk.Label(self, text='Compliance:')
        # Setup des variables
        self.min2 = tk.DoubleVar(self, 3)
        self.max2 = tk.DoubleVar(self, 5)
        self.nbPoint2 = tk.IntVar(self, 3)
        self.compliance2 = tk.DoubleVar(self, 1)
        # Création des champs à compléter par l'utilisateur
        Entry_min2 = tk.Entry(self, textvariable=self.min2, justify='center', width=15)
        Entry_max2 = tk.Entry(self, textvariable=self.max2, justify='center', width=15)
        Entry_nbPoint2 = tk.Entry(self, textvariable=self.nbPoint2, justify='center', width=15)
        Entry_compliance2 = tk.Entry(self, textvariable=self.compliance2, justify='center', width=15)
        # Initialisation des ranges de mesure
        self.Range_min2 = tk.StringVar(self,'V')
        self.Range_max2 = tk.StringVar(self,'V')
        self.Range_comp2 = tk.StringVar(self,'mA')
        # Création de menus déroulant pour la selection de la range de mesure
        Deroulant_Range_min2 = tk.OptionMenu(self, self.Range_min2, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        Deroulant_Range_min2.config(width=3)
        Deroulant_Range_max2 = tk.OptionMenu(self, self.Range_max2, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        Deroulant_Range_comp2 = tk.OptionMenu(self, self.Range_comp2, 'A', 'mA', '\u03BCA', 'V', 'mV', '\u03BCV')
        # Placement des éléments sur la grille
        Title2.grid(row=1, column=5)
        Entry_name2.grid(row=1, column=6)
        Label_grandeurImposee2.grid(row=2, column=5)
        Deroulant_grandeurImposee2.grid(row=2, column=6, sticky="ew",)
        Label_min2.grid(row=3, column=5)
        Entry_min2.grid(row=3, column=6)
        Deroulant_Range_min2.grid(row=3, column=7, sticky="ew")
        Label_max2.grid(row=4, column=5)
        Entry_max2.grid(row=4, column=6)
        Deroulant_Range_max2.grid(row=4, column=7, sticky="ew")
        Label_compliance2.grid(row=5, column=5)
        Entry_compliance2.grid(row=5, column=6)
        Deroulant_Range_comp2.grid(row=5, column=7, sticky="ew")
        Label_nbPts2.grid(row=6, column=5)
        Entry_nbPoint2.grid(row=6, column=6)
        
        # Ligne de séparation
        separator1 = ttk.Separator(self, orient='horizontal')
        separator1.grid(row=0, column=1, columnspan=7, pady=10, sticky='ew')
        separator2 = ttk.Separator(self, orient='vertical')
        separator2.grid(row=1, rowspan=6, column=4, sticky='ns')
        separator3 = ttk.Separator(self, orient='horizontal')
        separator3.grid(row=7, column=1, columnspan=7, pady=10, sticky='ew')
        
        # Choix des channels utilités
        Label_ch = tk.Label(self, text='Channel(s) utilisée(s):')
        self.ch_used = tk.StringVar(self, '1')
        Deroulant_ch = tk.OptionMenu(self, self.ch_used,'1','2','main-1 & 2','main-2 & 1')
        Label_ch.grid(row=8, column=1)
        Deroulant_ch.grid(row=8, column=2, sticky="ew")
        # Temps de relaxation
        TpsRelaxation = tk.Label(self, text='Tps de relaxation (en ms):')
        self.deltaT = tk.DoubleVar(self, 10) # La SMU prend des valeurs en second il faut donc diviser par 1000 plus tard
        Entry_relaxation = tk.Entry(self, textvariable=self.deltaT, justify='center', width=15)
        TpsRelaxation.grid(row=9, column=1)
        Entry_relaxation.grid(row=9, column=2)
        # Bouton de lancement de mesure
        Button_mesure = tk.Button(self, text='Mesure', command=self.interface2measure, bg='yellow green', width=8)
        Button_mesure.grid(row=8, column=4)
        # Bouton pour fermer l'interface
        Button_quitter = tk.Button(self, text='Quitter', command=self.close, bg='firebrick1', width=8)
        Button_quitter.grid(row=9, column=4)
    
    def interface2measure(self):
        print('Attempt to measure \n')
        print('step 1 : ch_used = '+self.ch_used.get()+'\n') # On definit l'object Reglage en fonction des paramètres de mesures
        if self.ch_used.get() == '1':
            if self.grandeur_imposee1.get()=='Tension':
                unite = 'VOLT'
            else:
                unite = 'CURR'
            self.reg = Reglage(self.min1.get(), self.max1.get(), unite, self.nbPoint1.get(), '1', self.compliance1.get())
        
        elif self.ch_used.get() == '2':
            if self.grandeur_imposee2.get()=='Tension':
                unite = 'VOLT'
            else:
                unite = 'CURR'
            self.reg = Reglage(self.min2.get(), self.max2.get(), unite, self.nbPoint2.get(), '2', self.compliance2.get())
            
        elif self.ch_used.get() == 'main-1 & 2' or self.ch_used.get() == 'main-2 & 1':
            if self.grandeur_imposee1.get()=='Tension':
                unite1 = 'VOLT'
            else:
                unite1 = 'CURR'
            if self.grandeur_imposee2.get()=='Tension':
                unite2 = 'VOLT'
            else:
                unite2 = 'CURR'
            reg1 = Reglage(self.min1.get(), self.max1.get(), unite1, self.nbPoint1.get(), 1, self.compliance1.get())
            reg2 = Reglage(self.min2.get(), self.max2.get(), unite2, self.nbPoint2.get(), 2, self.compliance2.get())
            self.reg = [reg1, reg2]
        else:
            print('Error 1 \n')
            
        print('step 2 \n') # On definit l'object FenTracerVar
        self.FenVar = FenTracerVar(self.inst, self.deltaT.get()/1000, self.ch_used.get(), self.reg)
        print('step 3 \n') # On lance les mesures
        self.FenVar.carac() 
        print('step 4 \n') # On trace les resultats
        if self.ch_used.get() == '1' or self.ch_used.get() == '2':
            plt.plot(self.FenVar.VarMain, self.FenVar.mesure)
        elif self.ch_used.get() == 'main-1 & 2':
            for i in range(reg2.npoint):
                plt.plot(self.FenVar.VarMain, self.FenVar.mesure[i][0])
        elif self.ch_used.get() == 'main-2 & 1':
            for i in range(reg1.npoint):
                plt.plot(self.FenVar.VarMain, self.FenVar.mesure[i][0])
        else:
            print('Error 4 \n')
        print('Mesure terminé')
            
    def interface2export(self):
        
        if self.FenVar != None:
            exportWindow = ExportData.exportInterface(self.FenVar)
            exportWindow.mainloop()
        else:
            tk.messagebox.showerror(title='Error', message="Aucune mesure n'a été réaliser")
        
    def close(self):
        self.destroy()
    