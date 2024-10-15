# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 13:56:07 2020

@author: XuL
"""

import tkinter as tk
import datetime as dt
import settings as st

def ExportInterface(reg):
    #Nom par défaut du fichier
    CurrentTime = dt.datetime.now()
    File_Name = CurrentTime.strftime("Exported_Data_%d-%m-%Y_at_%H-%M-%S")
    
    #Fenetre d'exportation, changement de nom du fichier possible
    fenetre = tk.Tk()
    fenetre.title("Exportation des données")
    
    champ_label1 = tk.Label(fenetre, text="Nom du fichier")
    champ_label2 = tk.Label(fenetre, text=".txt")
    champ_label3 = tk.Label(fenetre, text="")
    ligne_texte1 = tk.Entry(fenetre, textvariable=File_Name, width = 50)
    ligne_texte1.insert(0, File_Name)
    bouton_valider = tk.Button(fenetre, text="Valider", command=lambda:ExportIntoTxt(File_Name + ".txt", reg))
    bouton_quitter = tk.Button(fenetre, text="Quitter", command=fenetre.destroy)
    
    champ_label1.grid(row=1, column=1)
    ligne_texte1.grid(row=1, column=2)
    champ_label2.grid(row=1, column=3)
    champ_label3.grid(row=2, column=1)
    bouton_valider.grid(row=3, column = 3)
    bouton_quitter.grid(row=3, column = 4)
    
    fenetre.mainloop()  

def ExportIntoTxt(File_Name, reg):
    
    File = open(File_Name, "w")
    File.write("Settings \n")
    File.write("Output 1 \t Input 1 \t Output 2 \t Input 2")
    
    for i in range (0, reg.get_nb_pts
    
    
    
    
    
    File.close()
    
    Flavor = tk.Tk()
    FlavorLabel = tk.Label(Flavor, text="Exportation terminer")
    FlavorButton = tk.Button(Flavor, text="Ok", command=Flavor.destroy)
    FlavorLabel.grid(row=1, column=1)
    FlavorButton.grid(row=2, column=1)
    Flavor.mainloop()
    

def CheckFileName(File_Name):
    return True


    
    
    