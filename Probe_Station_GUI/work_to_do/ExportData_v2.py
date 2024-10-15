# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 18:23:52 2020

@author: XuL
"""

import tkinter as tk
from tkinter import filedialog 
import datetime as dt

def ExportInterface():
    #Nom par défaut du fichier
    CurrentTime = dt.datetime.now()
    File_Name = CurrentTime.strftime("Exported_Data_from_%d-%m-%Y_at_%H-%M-%S")
    
    global Dossier
    Dossier = "/download"
    
    #Fenetre d'exportation, changement de nom du fichier possible
    fenetre = tk.Tk()
    fenetre.title("Exportation des données")
    
    label_text1 = tk.Label(fenetre, text="Destination:")
    label_text2 = tk.Label(fenetre, text="Nom du fichier:")
    label_destination = tk.Label(fenetre, text="None", width=50)
    ligne_text1 = tk.Entry(fenetre, textvariable=File_Name,width = 50)
    ligne_text1.insert(0, File_Name)
    bouton_choisir = tk.Button(fenetre, text="Choisir", command=ChoisirDossier )
    bouton_valider = tk.Button(fenetre, text="Exporter", command=lambda:ExportIntoTxt(File_Name + ".txt"))
    bouton_quitter = tk.Button(fenetre, text="Quitter", command=fenetre.destroy)
    
    label_text1.grid(row=1, column=1)
    label_destination.grid(row=1, column=2)
    bouton_choisir.grid(row=1, column=3)
    label_text2.grid(row=2, column=1)
    ligne_text1.grid(row=2, column=2)
    bouton_valider.grid(row=3, column = 3)
    bouton_quitter.grid(row=3, column = 4)
    
    fenetre.mainloop()  
    
def ChoisirDossier(): 

    Dossier = filedialog.askdirectory(initialdir = "/", title = "Select a File", filetypes = ("all files","*.*"))
    
def ExportIntoTxt(File_Name):
    
    File = open(File_Name, "w")
    File.write("Settings \n")
    File.write("Output 1 \t Input 1 \t Output 2 \t Input 2")
    
    for i in range (0, get_nb_pts=100):
        File.write("Output et input pour i = %d", i)
        
    
    
    
    
    
    File.close()
    
    Flavor = tk.Tk()
    FlavorLabel = tk.Label(Flavor, text="Exportation terminer")
    FlavorButton = tk.Button(Flavor, text="Ok", command=Flavor.destroy)
    FlavorLabel.grid(row=1, column=1)
    FlavorButton.grid(row=2, column=1)
    Flavor.mainloop()
    

def CheckFileName(File_Name):
    return True

ExportInterface()