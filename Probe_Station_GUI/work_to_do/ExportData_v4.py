# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 22:30:58 2020

@author: XuL
"""

import tkinter as tk
from tkinter import filedialog 
import datetime as dt
import os.path


def ExportInterface():

    #Nom du fichier par défaut
    File_Name = dt.datetime.now().strftime("Exported_Data_from_%d-%m-%Y_at_%H-%M-%S")
    
    #Dossier de destination par défaut
    global Dossier
    Dossier = "/download"
    
    #Fenetre d'exportation
    fenetre = tk.Tk()
    fenetre.title("Exportation des données")
    label_text1 = tk.Label(fenetre, text="Destination:")
    label_text2 = tk.Label(fenetre, text="Nom du fichier:")
    label_destination = tk.Label(fenetre, text=Dossier, width=50)
    ligne_text1 = tk.Entry(fenetre, textvariable=File_Name,width = 50)
    ligne_text1.insert(0, File_Name)
    bouton_choisir = tk.Button(fenetre, text="Choisir", width=8, command=ChooseFolder)
    bouton_valider = tk.Button(fenetre, text="Exporter", width=8, command=lambda:ExportIntoTxt(File_Name + ".txt", Dossier))
    bouton_quitter = tk.Button(fenetre, text="Quitter", width=8, command=fenetre.destroy)

    label_text1.grid(row=1, column=1)
    label_destination.grid(row=1, column=2)
    bouton_choisir.grid(row=1, column=3)
    label_text2.grid(row=2, column=1)
    ligne_text1.grid(row=2, column=2)
    bouton_valider.grid(row=3, column = 3)
    bouton_quitter.grid(row=3, column = 4)
    
    fenetre.mainloop()
    
def ChooseFolder():
    global Dossier
    Dossier = filedialog.askdirectory(initialdir = Dossier, title = "Select a Folder")
    
def CheckFileName(File_Name, Dossier):
    
    
    return True
    
def ExportIntoTxt(File_Name):
    
    # File = open(File_Name, "w")
    # File.write("Settings \n")
    # File.write("Output 1 \t Input 1 \t Output 2 \t Input 2")
    
    # for i in range (0, get_nb_pts=100):
    #     File.write("Output et input pour i = %d", i)
        
    # File.close()
    
    Flavor = tk.Tk()
    FlavorLabel = tk.Label(Flavor, text="Exportation terminer")
    FlavorButton = tk.Button(Flavor, text="Ok", command=Flavor.destroy)
    FlavorLabel.grid(row=1, column=1)
    FlavorButton.grid(row=2, column=1)
    Flavor.mainloop()
    
ExportInterface()