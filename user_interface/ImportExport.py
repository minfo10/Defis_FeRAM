import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

class ImportInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Import Data")
        self.file_name_var = tk.StringVar(value="imported_data.txt")
        file_path = fd.askopenfilename(
            title="Select a file to import",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:  # Check if the user did not cancel
            try:
                with open(file_path, "r") as file:
                    data = file.read()
                    mb.showinfo("Imported Data", data)
                    self.destroy()  # Ferme la fenêtre après l'importation réussie
            except Exception as e:
                mb.showerror("Error", f"Failed to import data: {e}")

class ExportInterface(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Export Data")
        self.file_name_var = tk.StringVar(value="exported_data.txt")
        file_path = fd.asksaveasfilename(
            initialfile=self.file_name_var.get(),
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:  # Check if the user did not cancel
            with open(file_path, "w") as file:
                # Sample data to export
                file.write("Sample data\n")
                self.destroy()  # Ferme la fenêtre après l'importation réussie

            mb.showinfo("Success", "Data exported successfully!")