# connection.py

import serial
import serial.tools.list_ports
import platform
import tkinter as tk
from tkinter import ttk


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
