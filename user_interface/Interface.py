# Description: Interface graphique pour le défi FeRAM
# Ce programme est une interface utilisateur graphique (GUI) développée en Python avec Tkinter.
# Il permet de communiquer avec un Arduino pour lire et écrire des données sur une mémoire FeRAM.
# Les fonctionnalités incluent la détection automatique du port Arduino, l'envoi et la réception de données,
# ainsi que l'importation et l'exportation de fichiers texte. L'interface est conçue pour être intuitive
# et offre des sections dédiées pour la connexion, l'écriture, la lecture et les informations importantes.


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
from tkinter import messagebox as mb
from tkinter import filedialog as fd
from tkinter import PhotoImage


class Interface(tk.Tk):

#----------------------------------------------------------
# Initialisation de la classe Interface
#----------------------------------------------------------
    def __init__(self):
        super().__init__()
        
        # Titre et icône de la fenêtre
        self.title('Défi FeRAM')
        self.iconphoto(True, PhotoImage(os.path.abspath('icon.ico')))
        self.geometry('580x420')
        self.configure(background='light gray')

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
        
        self.grid_rowconfigure(0, weight=1, minsize=50)  # Set minimum size for row 0
        self.grid_columnconfigure(0, weight=1, minsize=150)  # Set minimum size for column 0


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

    def on_resize(self, _=None):
        self.update_font_size()
        self.update_idletasks()  # Forcer la mise à jour visuelle


    # Fonction pour mettre à jour la taille de la police et les paddings
    def update_font_size(self):
        # Appeler la fonction pour calculer la taille de la police et les paddings
        font_size, padding_factor = self.calculate_font_size_and_padding()
        # Appliquer les nouvelles tailles et paddings
        self.update_widgets_font(font_size, padding_factor)


    # Fonction pour calculer la taille de la police et les paddings
    def calculate_font_size_and_padding(self):
        # Calculer la taille de la police en fonction de la hauteur de la fenêtre
        window_height = self.winfo_height()
        font_size = max(int(window_height / 40), 8)  # Minimum font size is 8

        # Calculer les paddings en fonction de la taille de la police
        padding_factor = max(font_size // 10, 2)  # Ajuster l'espace de manière proportionnelle à la taille de la police

        # Retourner la taille de la police et le facteur de padding
        return font_size, padding_factor


    # Fonction pour mettre à jour la taille de la police et les paddings
    def update_widgets_font(self, font_size, padding_factor):
        print(f"Updating fonts to {font_size} and padding to {padding_factor}")
        for widget in self.winfo_children():
            # Ensure the widget is updated
            print(f"Updating widget: {widget}")
            if isinstance(widget, (tk.Label, tk.Button, tk.Entry, tk.Text)):
                widget.configure(font=("Arial", font_size))  # Mise à jour de la police
            elif isinstance(widget, (ttk.Label, ttk.Button, ttk.Entry)):
                style = ttk.Style(self)
                style.configure("TLabel", font=("Arial", font_size))
                style.configure("TButton", font=("Arial", font_size))
                style.configure("TEntry", font=("Arial", font_size))
            
            # Mise à jour des paddings
            widget.grid_configure(padx=padding_factor, pady=padding_factor)
            widget.update_idletasks()  # Forcer la mise à jour visuelle


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


    def close(self):
        self.destroy()

# Fonction pour détecter le port de l'Arduino
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
                    return port.device
            
            # Windows
            elif os_type == 'Windows':
                if 'COM' in port.device:
                    return port.device  # Return the Arduino port on Windows

        # Si aucun port n'est trouvé, on retourne None
        return None




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
            mb.showerror("Erreur de port", f"{e}")

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
                        mb.showinfo("Info",f"{derniere_ligne}")
                        # Vous pouvez sortir de la boucle ou faire d'autres traitements ici
                    break  # Sortir de la boucle après avoir lu la sixième ligne
                except ValueError:
                    mb.showerror("Erreur de valeur", f"Veuillez entrer un nombre valide.")

        except serial.SerialException as e:
            # Affiche une boîte de message en cas de port indisponible
            mb.showerror("Erreur de port", f"{e}")

        finally:
            # Fermer le port série
            if 'ser' in locals() and ser.is_open:
                ser.close()






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
# Importation de données
#----------------------------------------------------------

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

#----------------------------------------------------------
# Exportation de données
#----------------------------------------------------------
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