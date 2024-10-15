# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 21:34:37 2020

@author: XuL
"""

import datetime as dt
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb
import FenTracer

def Export(NombreDeVariable, FenTracer):
    
    # Nom par defaut du fichier
    DefaultName = dt.datetime.now().strftime("Exported_Data_from_%d-%m-%Y_at_%H-%M-%S")
    
    # Explorateur de fichier pour choisir ou sauvegarder
    file = fd.asksaveasfile(mode="w", title="Exporting data", initialfile=DefaultName, defaultextension=".txt", filetypes=(("Fichier texte", "*.txt"), ("Autres types", "*.*")))
    
    # Si FenTracer1var alors
    if (NombreDeVariable == 1):
        file.write("Reglage: \n") # On ecrit toute les reglages et parametrage
        file.write("Mini = " + str(FenTracer.Reglage.mini) + "\n")
        file.write("Maxi = " + str(FenTracer.Reglage.maxi) + "\n")
        file.write("unite = " + str(FenTracer.Reglage.unite) + "\n")
        file.write("npoint = " + str(FenTracer.Reglage.npoint) + "\n")
        file.write("nom = " + str(FenTracer.Reglage.nom) + "\n")
        file.write("mes = " + str(FenTracer.Reglage.mes) + "\n")
        file.write("comp = " + str(FenTracer.Reglage.comp) + "\n")
        file.write("\n")
        file.write("Temps de mesure: " + str(FenTracer.tps) + "\n")
        file.write("\n")
        
        # On ecrit les donnees
        file.write("Input 1 \t Output 1 \n")
        for i in range (0, FenTracer.npoint):
            file.write(str(FenTracer.mesure[0][i]) + "\t" + str(FenTracer.mesure[1][i]) + "\n")
    
    # Signaler la fin de l'exportation
    mb.showinfo(title="Exporting data", message="Completed")
    
# Interface de test
main = tk.Tk()
label = tk.Label(main, text="idk")
truc = tk.Button(main, text="Export", command=Export(1, FenTracer.FenTracer1var)) # Pas encore tester
end = tk.Button(main, text="Quitter", command = main.destroy)
label.grid(row=1, column=1)
truc.grid(row=2, column=1)
end.grid(row=3, column=1)
main.mainloop()