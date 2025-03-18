# import_export.py

import tkinter as tk
from tkinter import filedialog as fd
from tkinter import messagebox as mb

# Fonctions d'exportation et d'importation
def exportation(self):
    # Create a new window for export and start the process
    exportWindow = ExportInterface(self)
    exportWindow.grab_set()  # Make the export window modal (block interaction with parent window)

def importation(self):
    # Create a new window for import and start the process
    importWindow = ImportInterface(self)
    importWindow.grab_set()  # Make the import window modal (block interaction with parent window)


# Importation de données
class ImportInterface(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Import Data")
        self.parent = parent  # Reference to the parent window
        
        # Ask for the file to import
        file_path = fd.askopenfilename(
            title="Select a file to import",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:  # Check if the user did not cancel
            try:
                # Try reading the file content
                with open(file_path, "r") as file:
                    data = file.read()
                    # Display imported data in a message box
                    mb.showinfo("Imported Data", data)
                    self.destroy()  # Close the import window after showing data
            except Exception as e:
                # Handle any errors during file reading
                mb.showerror("Error", f"Failed to import data: {e}")
                self.destroy()  # Close


# Exportation de données
class ExportInterface(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        
        self.title("Export Data")
        self.parent = parent  # Reference to the parent window
        
        # Ask for the file to save the data
        file_path = fd.asksaveasfilename(
            initialfile="exported_data.txt",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:  # Check if the user did not cancel
            try:
                # Sample data to export (you can change this as needed)
                with open(file_path, "w") as file:
                    file.write("Sample data\n")
                # Show a success message
                mb.showinfo("Success", "Data exported successfully!")
                self.destroy()  # Close the export window after success
            except Exception as e:
                # Handle any errors during file writing
                mb.showerror("Error", f"Failed to export data: {e}")
                self.destroy()  # Close