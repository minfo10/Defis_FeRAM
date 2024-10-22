import datetime as dt
import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

class exportInterface(tk.Tk):
    def __init__(self, FenVar):
        super().__init__()
        
        self.FenVar = FenVar
        self.Dossier = "/download"
        DefaultName = dt.datetime.now().strftime("Exported_Data_from_%d-%m-%Y_at_%H-%M-%S")
        self.file_name_var = tk.StringVar(value=DefaultName)
        
        self.title("Exportation des données")
        label_text1 = tk.Label(self, text="Destination:")
        label_text2 = tk.Label(self, text="Nom du fichier:")
        label_destination = tk.Label(self, text=self.Dossier, width=50)
        
        ligne_text1 = tk.Entry(self, textvariable=self.file_name_var, width=50)
        bouton_choisir = tk.Button(self, text="Choisir", width=8, command=self.ChooseFolder)
        bouton_valider = tk.Button(self, text="Exporter", width=8, command=self.ExportIntoTxt)
        bouton_quitter = tk.Button(self, text="Quitter", width=8, command=self.destroy)
        
        label_text1.grid(row=1, column=1)
        label_destination.grid(row=1, column=2)
        bouton_choisir.grid(row=1, column=3)
        label_text2.grid(row=2, column=1)
        ligne_text1.grid(row=2, column=2)
        bouton_valider.grid(row=3, column=3)
        bouton_quitter.grid(row=3, column=4)

    def ChooseFolder(self):
        self.Dossier = fd.askdirectory(initialdir=self.Dossier, title="Select a Folder")

    def ExportIntoTxt(self):
        file_path = fd.asksaveasfilename(
            title="Exporting data",
            initialfile=self.file_name_var.get(),
            defaultextension=".txt",
            filetypes=(("Fichier texte", "*.txt"), ("Autres types", "*.*"))
        )
        
        if file_path:  # Check if the user did not cancel
            with open(file_path, "w") as file:
                if self.FenVar.ch_used in ['1', '2']:
                    file.write("Reglage: \n")
                    file.write("Mini = " + str(self.FenVar.reglage.mini) + "\n")
                    file.write("Maxi = " + str(self.FenVar.reglage.maxi) + "\n")
                    file.write("unite = " + str(self.FenVar.reglage.unite) + "\n")
                    file.write("npoint = " + str(self.FenVar.reglage.npoint) + "\n")
                    file.write("nom = " + str(self.FenVar.ch_used) + "\n")
                    file.write("mes = " + str(self.FenVar.reglage.mes) + "\n")
                    file.write("comp = " + str(self.FenVar.reglage.comp) + "\n")
                    file.write("\n")
                    
                    file.write("Input 1 \t Output 1 \n")
                    for i in range(self.FenVar.reglage.npoint):
                        file.write(str(self.FenVar.VarMain[i]) + "\t" + str(self.FenVar.mesure[i]) + "\n")
                
                    mb.showinfo(title="Exporting data", message="Completed")
                else:
                    print('Ca marche pas encore mdr')

        self.destroy()
