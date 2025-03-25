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

# Importation des classes
from import_export import ImportInterface
from import_export import ExportInterface


class Interface(tk.Tk):

#----------------------------------------------------------
# Initialisation de la classe Interface
#----------------------------------------------------------
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
        self.bind('<Configure>', self.on_resize)

        # Barre de menu
        self.create_menu()

        # Sections principales
        self.connection_section()
        self.write_section()
        self.read_section()
        self.information_section()

        # Bouton quitter
        Button_quitter = ttk.Button(self, text='Quitter', command=self.close)
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
        self.port_com = tk.StringVar(self, value=self.detect_arduino_port)
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
        ttk.Button(frame_connexion, text="Vérifier", command=self.check_connection).grid(row=2, column=1, padx=5, sticky="w")

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
        ttk.Button(frame_write, text="Envoyer", command=self.send_data).grid(row=3, column=0, columnspan=2, pady=10)

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
        ttk.Button(frame_read, text="Recevoir", command=self.receive_data).grid(row=3, column=0, columnspan=2, pady=10)

    # Function to close the application
    def close(self):
        self.destroy()

    # Placeholder function for reset action
    def reset(self):
        print("Reset triggered")  # Temporary action for the reset function


#----------------------------------------------------------
# Function to create the menu
#----------------------------------------------------------

    def create_menu(self):
        menuBar = tk.Menu(self)
        self.config(menu=menuBar)

        # Create "Data" menu
        self.create_data_menu(menuBar)

        # Create "Arduino" menu
        self.create_arduino_menu(menuBar)

        # Create "Help" menu
        self.create_help_menu(menuBar)

    # Function to create the "Data" menu
    def create_data_menu(self, menuBar):
        menuData = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Data', menu=menuData)
        menuData.add_command(label="Exporter en .txt", command=self.exportation)
        menuData.add_command(label="Importer en .txt", command=self.importation)

    # Function to create the "Arduino" menu
    def create_arduino_menu(self, menuBar):
        menuArduino = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Arduino', menu=menuArduino)
        menuArduino.add_command(label="Reset", command=self.reset)

    # Function to create the "Help" menu
    def create_help_menu(self, menuBar):
        menuHelp = tk.Menu(menuBar, tearoff=0)
        menuBar.add_cascade(label='Help', menu=menuHelp)
        menuHelp.add_command(label='GitHub', command=self.open_github)

    # Function to open the GitHub repository
    def open_github(self):
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
            # Check for text-based widgets
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text)):
                try:
                    # Apply the font change
                    widget.configure(font=("Arial", self.winfo_fpixels("1c") // 1.5))
                except Exception as e:
                    print(f"Error applying font to widget {widget}: {e}")
            
            # For ttk widgets, handle font separately
            elif isinstance(widget, (ttk.Label, ttk.Button, ttk.Entry)):
                try:
                    # Apply the font change for ttk widgets (may need a custom style in ttk)
                    widget.configure(style="TButton")  # This works for ttk buttons
                    widget.configure(font=("Arial", self.winfo_fpixels("1c") // 1.5))
                except Exception as e:
                    print(f"Error applying font to ttk widget {widget}: {e}")
            
            # Skip non-text widgets
            else:
                print(f"Skipping widget {widget}, as it doesn't support font changes.")


#----------------------------------------------------------
# Function to check the connection
#----------------------------------------------------------

    # Function to check the connection with the selected port
    def check_connection(self):
        # Retrieve the selected COM port and baud rate from the user interface
        port = self.port_com.get()
        baud = int(self.baud_rate.get())

        try:
            # Attempt to establish a serial connection
            with serial.Serial(port, baud, timeout=1) as ser:
                # If successful, update connection status and change the indicator to green
                self.connection_status.set("Connecté")
                self.style.configure("Voyant.TLabel", background="green")  
        except Exception as e:
            # If an error occurs, update connection status and change the indicator to red
            self.connection_status.set("Non connecté")
            self.style.configure("Voyant.TLabel", background="red")  
            print(f"Erreur de connexion: {e}")


    # Function to detect the Arduino connection port
    def detect_arduino_port(self):
        # Retrieve the list of serial ports and determine the system's OS
        ports = serial.tools.list_ports.comports()
        os_type = platform.system()

        # Iterate over the available serial ports
        for port in sorted(ports):
            print(f"Port: {port.device}, Description: {port.description}, HWID: {port.hwid}")

            # Handle different OS types to determine the correct port for Arduino
            if os_type in ['Linux', 'Darwin']:  # 'Darwin' is for macOS
                if 'ttyACM' in port.device or 'ttyUSB' in port.device:
                    return port.device  # Return the Arduino port on Linux/macOS

            elif os_type == 'Windows':
                if 'COM' in port.device:
                    return port.device  # Return the Arduino port on Windows

        # If no Arduino port is found, return None
        return None

#----------------------------------------------------------
# Function to export and import data
#----------------------------------------------------------

    # Fonctions d'exportation et d'importation
    def exportation(self):
        # Create a new window for export and start the process
        exportWindow = ExportInterface(self)
        exportWindow.grab_set()  # Make the export window modal (block interaction with parent window)

    def importation(self):
        # Create a new window for import and start the process
        importWindow = ImportInterface(self)
        importWindow.grab_set()  # Make the import window modal (block interaction with parent window)

#----------------------------------------------------------
# Receive Data Function
#----------------------------------------------------------

    # Fonction pour recevoir les données depuis l'arduino de controle
    def receive_data(self):

        port = self.port_com.get()  # Obtient le port de self.port_com
        baud = int(self.baud_rate.get())  # Convertit le baud rate en entier

        try:
            # Ouvre le port série
            ser = serial.Serial(port, baud)

            ligne = int(self.rligne.get())
            colonne = int(self.rcolonne.get())

            time.sleep(5)

            # Envoyer le nombre à l'Arduino
            ser.write("2\n".encode())
            time.sleep(1)
            ser.write((str(ligne) + "\n").encode())
            time.sleep(1)
            ser.write((str(colonne) + "\n").encode())
            time.sleep(1)

            lines = []
            while True:
                try:
                    # Lire une ligne depuis le port série
                    donnee = ser.readline().decode().strip()  # Décodage et nettoyage
                    for i in range(0,4):
                        print(f"Donnée reçue : {ser.readline().decode().strip()}")
                    
                    if donnee :
                    # Ajouter la ligne à la liste
                        lines.append(donnee)

                    # Vérifier si nous avons au moins 6 lignes
                    if len(lines) >= 1:
                        # Si oui, lire la sixième ligne
                        derniere_ligne = lines[len(lines)-1]
                        print(f"{derniere_ligne}")
                        # Vous pouvez sortir de la boucle ou faire d'autres traitements ici
                    break  # Sortir de la boucle après avoir lu la sixième ligne

                except KeyboardInterrupt:
                    print("Arrêt de la lecture des données.")
                    break  # Quitte la boucle si l'utilisateur interrompt
                # Après la lecture, afficher toutes les lignes


            print("Toutes les lignes lues :")
            for i, line in enumerate(lines):
                print(f"Ligne {i+1}: {line}")

            # Écrit les données dans le fichier texte
            with open("data/exported_data.txt", "w") as fichier:
                fichier.write(f"{donnee}\n")
                fichier.flush()

            # Lecture du contenu du fichier texte pour l'afficher
            try:
                with open("data/exported_data.txt", "r") as file:
                    contenu = file.read()
            except FileNotFoundError:
                contenu = "Fichier non trouvé"
                
            # Mise à jour de l'Entry avec le contenu
            self.read.set(contenu)

        except serial.SerialException as e:
            # Affiche une boîte de message en cas de port indisponible
            messagebox.showerror("Erreur de port", f"{e}")

        finally:
            # Ferme le port série après la lecture
            if 'ser' in locals() and ser.is_open:
                ser.close()

#----------------------------------------------------------
# Send Data Function
#----------------------------------------------------------

    # Fonction pour envoyer les données vers l'arduino de controle
    def send_data(self):
        
        port = self.port_com.get()  # Obtient le port de self.port_com
        baud = int(self.baud_rate.get())  # Convertit le baud rate en entier

        # Nombre à envoyer
        number_to_send = int(self.write.get())
        ligne = int(self.wligne.get())
        colonne = int(self.wcolonne.get())
        
        try:
            # Ouvre le port série
            ser = serial.Serial(port, baud)
            time.sleep(2)  # Attendre que la connexion s'établisse

            delay = 0.1

            # Envoyer le nombre à l'Arduino
            ser.write("1\n".encode())
            time.sleep(delay)
            ser.write((str(number_to_send) + "\n").encode())
            time.sleep(delay)
            ser.write((str(ligne) + "\n").encode())
            time.sleep(delay)
            ser.write((str(colonne) + "\n").encode())


            lines = []
            while True:
                try:
                    # Lire une ligne depuis le port série
                    donnee = ser.readline().decode().strip()  # Décodage et nettoyage
                    for i in range(0,10):
                        print(f"{ser.readline().decode().strip()}")

                    # Ajouter la ligne à la liste
                    lines.append(donnee)

                    # Vérifier si nous avons au moins 6 lignes
                    if len(lines) == 7:
                        # Si oui, lire la septième ligne
                        derniere_ligne = lines[6]
                        messagebox.showinfo("Info",f"{derniere_ligne}")
                        # Vous pouvez sortir de la boucle ou faire d'autres traitements ici
                    break  # Sortir de la boucle après avoir lu la sixième ligne
                except ValueError:
                    messagebox.showerror("Erreur de valeur", f"Veuillez entrer un nombre valide.")

        except serial.SerialException as e:
            # Affiche une boîte de message en cas de port indisponible
            messagebox.showerror("Erreur de port", f"{e}")

        finally:
            # Fermer le port série
            if 'ser' in locals() and ser.is_open:
                ser.close()