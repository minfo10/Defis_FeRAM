# Description: Interface graphique pour le défi FeRAM

# Importation des modules
import platform
import os
import webbrowser
import time
import serial
import serial.tools.list_ports

# Importation des modules tkinter
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import PhotoImage
from tkinter import filedialog as fd
from tkinter import messagebox as mb

# Importation des modules locaux
from connection import check_connection, detect_arduino_port
from import_export import exportation, importation
from receive_data import receive_data
from send_data import send_data


class Interface(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Titre et icône de la fenêtre
        self.title('Défi FeRAM')
        self.iconphoto(True, PhotoImage(os.path.abspath('icon.ico')))
        
        # Obtenir la résolution de l'écran
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Définir la taille de la fenêtre en fonction de la résolution
        window_width = int(screen_width * 0.7)  # 70% de la largeur de l'écran
        window_height = int(screen_height * 0.7)  # 70% de la hauteur de l'écran
        self.geometry(f'{window_width}x{window_height}')

        # Police et couleurs par défaut
        # self.option_add('*font', 'Arial 10')
        self.option_add('*foreground', 'black')
        self.configure(background='light gray')
    
        # Ajouter des configurations pour le redimensionnement
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Ajouter un binding pour ajuster la taille de la police lorsque la fenêtre est redimensionnée
        self.bind('<Configure>', on_resize())

        # Barre de menu
        self.create_menu()

        # Sections principales
        self.connection_section()
        self.write_section()
        self.read_section()
        self.information_section()

        # Bouton quitter
        Button_quitter = ttk.Button(self, text='Quitter', command=close)()
        Button_quitter.grid(row=4, column=1, pady=10, sticky='w')

        # Initialiser la taille de la police
        self.update_font_size()


#----------------------------------------------------------
# Fonctions de la classe Interface
#----------------------------------------------------------

    def connection_section(self):
        # Cadre principal pour la connexion et informations
        frame_connexion = ttk.LabelFrame(self, text="Information de connexion", padding=(10, 10))
        frame_connexion.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # Variables
        self.port_com = tk.StringVar(self, value=detect_arduino_port())
        self.baud_rate = tk.StringVar(self, value="2000000")
        self.connection_status = tk.StringVar(self, value="Non connecté")

        # Information de connexion
        ttk.Label(frame_connexion, text="Port de l'Arduino :").grid(row=0, column=0, sticky="w", pady=5)
        ttk.Entry(frame_connexion, textvariable=self.port_com, justify='center', width=12).grid(row=0, column=1, padx=5)

        ttk.Label(frame_connexion, text="Baud rate :").grid(row=1, column=0, sticky="w", pady=5)
        ttk.Entry(frame_connexion, textvariable=self.baud_rate, justify='center', width=12).grid(row=1, column=1, padx=5)

        # Voyant de connexion       
        voyant_frame = ttk.Frame(frame_connexion)  # Cadre pour aligner le voyant et le statut
        voyant_frame.grid(row=2, column=0, padx=5, sticky="w")
        self.voyant = ttk.Label(voyant_frame, text=" ", width=2, style="Voyant.TLabel", relief="solid")
        self.voyant.pack(side="left", padx=5)

        self.style = ttk.Style()
        self.style.configure("Voyant.TLabel", background="red")  # Initial state

        ttk.Label(voyant_frame, textvariable=self.connection_status).pack(side="left", padx=5)

        # Bouton pour vérifier la connexion
        ttk.Button(frame_connexion, text="Vérifier", command=check_connection()).grid(row=2, column=1, padx=5, sticky="w")

    def information_section(self):
        frame_information = ttk.LabelFrame(self, text="Informations importantes", padding=(10, 10))
        frame_information.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        info_text = tk.Text(frame_information, height=6, width=40, wrap="word", bg="white", state="normal", relief="flat")
        info_text.insert("1.0", "1. Vérifiez que le port COM et le baud rate soient bons.\n")
        info_text.insert("2.0", "2. Assurez-vous que ArduinoIDE est fermé (une console ouverte).\n")
        info_text.insert("3.0", "3. Cliquez sur 'Vérifier' pour confirmer la connexion Arduino.\n")
        info_text.config(state="disabled")  # Désactiver la modification par l'utilisateur
        info_text.pack(fill="both", expand=True)

    def write_section(self):
        # Section Écriture
        frame_write = ttk.LabelFrame(self, text="Écriture", padding=(10, 10))
        frame_write.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

        # Variables
        self.write = tk.StringVar(self, value="0")
        self.wligne = tk.StringVar(self, value="1")
        self.wcolonne = tk.StringVar(self, value="1")

        # Widgets
        ttk.Label(frame_write, text="Entier non signé (0-255)").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(frame_write, textvariable=self.write, justify='center', width=12).grid(row=0, column=1, padx=5)

        ttk.Label(frame_write, text="Ligne ? (1-128)").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Entry(frame_write, textvariable=self.wligne, justify='center', width=12).grid(row=1, column=1, padx=5)

        ttk.Label(frame_write, text="Colonne ? (1-16)").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Entry(frame_write, textvariable=self.wcolonne, justify='center', width=12).grid(row=2, column=1, padx=5)

        # Bouton Envoyer
        ttk.Button(frame_write, text="Envoyer", command=send_data()).grid(row=3, column=0, columnspan=2, pady=10)

    def read_section(self):
        # Section Lecture
        frame_read = ttk.LabelFrame(self, text="Lecture", padding=(10, 10))
        frame_read.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Variables
        self.rligne = tk.StringVar(self, value="1")
        self.rcolonne = tk.StringVar(self, value="1")
        self.read = tk.StringVar(self, value="")

        # Widgets
        ttk.Label(frame_read, text="Ligne ? (1-128)").grid(row=0, column=0, sticky='w', pady=5)
        ttk.Entry(frame_read, textvariable=self.rligne, justify='center', width=12).grid(row=0, column=1, padx=5)

        ttk.Label(frame_read, text="Colonne ? (1-16)").grid(row=1, column=0, sticky='w', pady=5)
        ttk.Entry(frame_read, textvariable=self.rcolonne, justify='center', width=12).grid(row=1, column=1, padx=5)

        ttk.Label(frame_read, text="Entier lu").grid(row=2, column=0, sticky='w', pady=5)
        ttk.Entry(frame_read, textvariable=self.read, justify='center', width=12, state='readonly').grid(row=2, column=1, padx=5)

        # Bouton Recevoir
        ttk.Button(frame_read, text="Recevoir", command=receive_data()).grid(row=3, column=0, columnspan=2, pady=10)

    # Function to close the application
    def close(self):
        self.destroy()

    # Placeholder function for reset action
    def reset(self):
        print("Reset triggered")  # Temporary action for the reset function


#----------------------------------------------------------
# Function to create the menu
#----------------------------------------------------------

def create_menu(app):
    menuBar = tk.Menu(app)
    app.config(menu=menuBar)

    # Create "Data" menu
    create_data_menu(menuBar)

    # Create "Arduino" menu
    create_arduino_menu(menuBar)

    # Create "Help" menu
    create_help_menu(menuBar)

# Function to create the "Data" menu
def create_data_menu(menuBar):
    menuData = tk.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label='Data', menu=menuData)
    menuData.add_command(label="Exporter en .txt", command=exportation)
    menuData.add_command(label="Importer en .txt", command=importation)

# Function to create the "Arduino" menu
def create_arduino_menu(menuBar):
    menuArduino = tk.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label='Arduino', menu=menuArduino)
    menuArduino.add_command(label="Reset", command=reset)

# Function to create the "Help" menu
def create_help_menu(menuBar):
    menuHelp = tk.Menu(menuBar, tearoff=0)
    menuBar.add_cascade(label='Help', menu=menuHelp)
    menuHelp.add_command(label='GitHub', command=open_github)

# Function to open the GitHub repository
def open_github():
    webbrowser.open("https://github.com/minfo10/Defis_FeRAM")

#----------------------------------------------------------
# Function to resize
#----------------------------------------------------------

# Function to handle window resizing
def on_resize(self, event):
    # Update font size when the window is resized
    self.update_font_size()

# Function to update font size dynamically
def update_font_size(self):
    # Calculate the font size based on the window's height
    window_width, window_height = self.winfo_width(), self.winfo_height()
    font_size = max(int(window_height / 40), 8)  # Minimum font size is 8

    # Apply the new font size to all widgets
    self.option_add('*font', f'Arial {font_size}')
    self.update_widgets_font_size()

# Function to update font size for all widgets
def update_widgets_font_size(self):
    # Update the font size of all existing widgets
    for widget in self.winfo_children():
        if isinstance(widget, ttk.Widget):
            widget.configure(font=("Arial", self.winfo_fpixels("1c") // 1.5))
