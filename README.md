# IPhy Challenges – Memories of the Future

**Authors**: Melahoui Aymane, Nicolas Rabreau (2024–2025)
**Partnership**: CEA Leti, as part of a year-long project at Grenoble-INP Phelma

---

## 📖 Table of Contents

* [⚙️ Prerequisites](#️-prerequisites)
* [🚀 Installation & Usage](#-installation--usage)
* [🔌 Arduino](#-arduino)
* [🖥️ User Interface](#️-user-interface)

---

## ⚙️ Prerequisites

Before starting, make sure the following are installed:

* [Python 3.x](https://www.python.org/downloads/)
* `pip` (via `get-pip.py` if needed)
* [Arduino IDE](https://www.arduino.cc/en/software)

**Required Python libraries**:

* `PyQt5` – Graphical user interfaces
* `numpy` – Numerical computations
* `pyserial` – Serial communication
* `tkinter` – Standard GUI library
* `zeroconf` – Automatic network discovery
* `pyvisa` – Instrument control through VISA

---

## 🚀 Installation & Usage

1. **Clone the repository**

   ```bash
   git clone https://github.com/minfo10/Defis_FeRAM.git
   cd Defis_FeRAM
   ```

2. **Upload the Arduino program**

   * Open the folder `Arduino/arduino_general` with your file explorer:

     * Windows: `explorer .`
     * Linux (GNOME): `nautilus .`
     * macOS: `open .`
   * Open the `.ino` file in the Arduino IDE
   * Check the `baudrate` and `port`
   * Compile and upload to your Arduino

3. **Create a Python virtual environment**

   * Windows:

     ```bash
     python -m venv env
     .\env\Scripts\activate
     ```
   * Linux/macOS:

     ```bash
     python3 -m venv env
     source env/bin/activate
     ```

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   ⚠️ If you encounter issues with `tkinter`:

   ```bash
   python -m tkinter
   ```

   → If a window "This is Tk" opens, it is installed. Otherwise, reinstall Python with `tkinter` included.

5. **Run the user interface**

   ```bash
   cd user_interface
   python main.py
   ```

---

## 🔌 Arduino

### 🎯 Purpose

The Arduino program allows **read and write operations** on a **FeRAM memory**, optimized through **direct register manipulation** for improved performance.

### ⚡ Register manipulation

Instead of using `digitalRead` and `digitalWrite`, the code interacts directly with the microcontroller registers.

* **Arduino UNO ports**:

  * `Port D` → pins 0–7
  * `Port B` → pins 8–13
  * `Port C` → A0–A5

Each port has 3 registers:

* `PORTx` → write output
* `PINx` → read input
* `DDRx` → set pin direction (in/out)

### 🛠️ Utility functions

* `pON(pin)` → set pin HIGH
* `pOFF(pin)` → set pin LOW
* `lect(pin)` → read pin state (0/1)

### 📂 Included Arduino programs

* `arduino_read` → read a full memory row
* `arduino_write` → write a full memory row
* `arduino_simul` → simulate FeRAM memory behavior
* `arduino_general` → combined read & write operations

---

## 🖥️ User Interface

The graphical interface (GUI) allows **characterization of the FeRAM device** and easy data exchange with the Arduino.

### 📌 File structure

* `main.py` → launches the GUI
* `Interface.py` → main class: serial connection, send/receive, import/export `.txt`

### 🖼️ Features

1. **Serial connection**: configure `port` & `baudrate`, connection indicator
2. **Write operations**: send numerical data to Arduino (row + column)
3. **Read operations**: retrieve data from Arduino (row + column)
4. **Import/Export**: handle `.txt` files (popup display, save current data)
