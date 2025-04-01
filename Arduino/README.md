# Arduino Memory Scan Chain Project

This project consists of two Arduino sketches that work together to control a memory device using a scan chain protocol. One sketch provides the main user interface for reading and writing memory cells, and the other simulates the acquisition process to aid in testing and debugging.

---

## File Overview

### 1. `arduino_general.ino`
**Purpose:**  
This sketch implements the core functionality for interfacing with a memory system via a scan chain. It manages user interactions through the Serial Monitor, allowing the user to write data to and read data from specific memory locations.

**Key Functions and Their Roles:**

- **`setup()`**
  - **Role:**  
    - Initializes all designated pins as inputs or outputs.
    - Sets all output pins to LOW.
    - Starts serial communication at 2,000,000 baud.
    - Displays the main menu via `affMenu()`.
  - **Considerations:**  
    - Verify that all hardware connections (pins for WB, SA, SL, WL, PRE, BL, etc.) correspond to your actual wiring.

- **`loop()`**
  - **Role:**  
    - Listens for user input via the Serial Monitor.
    - Depending on the user’s selection, it calls:
      - `ecriture()` for writing data.
      - `lecture()` for reading data.
      - (A placeholder for exporting data, not yet implemented.)
  - **Considerations:**  
    - Ensure that user inputs are correctly formatted and that the system remains responsive.

- **`affMenu(bool premAff)`**
  - **Role:**  
    - Displays a menu of options (Write, Read, Export) to guide the user.
  - **Considerations:**  
    - Called from both `setup()` and after completing an operation to keep the user informed.

- **`ecriture()`**
  - **Role:**  
    - Manages the writing process:
      - Prompts the user to input an 8-bit unsigned integer (0–255).
      - Requests the row (1–128) and column (1–16) where the data should be written.
      - Prepares the memory cell using `unPara()` (which sets the line to all 1’s).
      - Writes the data to the specified column with `scBL()`.
  - **Considerations:**  
    - Validates user inputs using `testRepValide()` and converts the string input to an 8-bit value via `stringToIntToBytes()`.

- **`lecture()`**
  - **Role:**  
    - Handles the reading process:
      - Prompts the user for the row and column to read.
      - Asks whether to activate the write-back function.
      - Configures the scan chain for reading (using `scWLSL()` and a series of pin toggles).
      - Reads the 8-bit value by iterating over clock pulses and accumulating bits.
      - Optionally performs a write-back operation if requested.
  - **Considerations:**  
    - Ensures proper synchronization with clock pulses via the `clk()` function.

- **`clk()`**
  - **Role:**  
    - Generates a clock pulse (HIGH → delay → LOW → delay) essential for timing in scan chain operations.
  - **Considerations:**  
    - The delays (200 µs) are critical; adjust them only if needed for your hardware.

- **Scan Chain Functions:**
  - **`scWLSL(int ligne)`**  
    - Selects a memory row by pulsing the scan chain input (`SC_IN`) when the target row is reached.
  - **`scOut()`**  
    - Reads a full 128-bit scan chain and assembles an integer value.
  - **`scBL(uint8_t repByte, int colonne)`**  
    - Writes a specified 8-bit value to a given column by pulsing `SC_IN` appropriately.
  - **`zeroPara(int ligne)`, `unPara(int ligne)`, `zeroUnitaire()`**  
    - Execute specific timing sequences (waveforms) for setting memory bits to 0 or 1.
    
- **Input Validation and Conversion:**
  - **`obtenirPosition(const char* message, int min, int max)`**  
    - Repeatedly prompts the user until a valid numeric position within the specified range is provided.
  - **`testRepValide(String reponse, int min, int max)`**  
    - Checks if the received input is within the acceptable bounds.
  - **`stringToIntToBytes(String rep)`**  
    - Converts the user’s string input to an 8-bit integer, applying a bit inversion for each bit (as per the original design).

---

### 2. `Simulation_AquisitionV1.ino`
**Purpose:**  
This sketch simulates the scan chain acquisition process, allowing you to test the memory read/write logic without needing the physical memory hardware. It is particularly useful for debugging and for early-stage development when hardware is unavailable.

**Key Functions and Their Roles:**

- **Interrupt Service Routines (ISRs):**
  - **`selUnISR()`**
    - **Role:**  
      - Triggered by a rising edge on `SIM_SEL_UN_PIN` to initiate a write capture cycle.
    - **Considerations:**  
      - Sets flags to indicate that a write scan is starting.
      
  - **`clockISR()`**
    - **Role:**  
      - Triggered by the rising edge on `SIM_CLOCK_PIN`.
      - In write mode, it captures the bit from `SIM_SC_IN_PIN` into the `scanData` buffer.
      - In read mode (when `readActive` is true), it outputs bits (LSB first) on `SIM_SC_OUT_PIN`.
    - **Considerations:**  
      - Manages both capturing and outputting data depending on the current cycle.
      
  - **`readTriggerISR()`**
    - **Role:**  
      - Triggered by a rising edge on `SIM_SA_PIN` to start a read cycle.
      - Computes the 8-bit value for a fixed column (by default, column 1) from the stored scan chain data.
    - **Considerations:**  
      - Sets debug flags to report the read operation.

- **`decodeScanData()`**
  - **Role:**  
    - Processes the 128-bit raw scan chain data and decodes it into 16 separate 8-bit column values.
  - **Considerations:**  
    - The decoded data is stored in the `storedColumns` array for further processing or debugging.

- **`setup()`**
  - **Role:**  
    - Initializes serial communication.
    - Sets pin modes for simulation (input for signals from the controller, output for simulation response).
    - Attaches the ISRs to the appropriate pins.
  - **Considerations:**  
    - Make sure the pin assignments match your simulation wiring, especially when using an Arduino Mega.

- **`loop()`**
  - **Role:**  
    - Monitors flags to detect when a complete write scan cycle (`scanDone`) or a read trigger occurs.
    - Decodes the scan data and prints the current state of each column for debugging.
    - Prints additional debug information (e.g., when a write or read trigger is detected).
  - **Considerations:**  
    - Contains a small delay to prevent serial output flooding.

---

## How to Use the Project

### For the Main Controller (`arduino_general.ino`)
1. **Wiring and Setup:**  
   - Connect your hardware according to the pin assignments (WB, SA, SL, WL, PRE, BL, etc.). Verify each connection corresponds to the expected function.
   - Upload the sketch to your Arduino (compatible with Arduino UNO-like boards).

2. **Operation:**  
   - Open the Serial Monitor set at 2,000,000 baud.
   - Choose an operation from the menu:
     - **1. Écriture (Write):** Input an 8-bit number (0–255), specify the row (1–128) and column (1–16), then watch as the data is written using the scan chain.
     - **2. Lecture (Read):** Select a row and column to read the stored 8-bit value. Optionally, activate write-back if desired.
     - **3. Export:** (Not yet implemented) Intended for exporting memory data to a text file.

### For the Simulation (`Simulation_AquisitionV1.ino`)
1. **Wiring and Setup:**  
   - Wire your simulation board (e.g., Arduino Mega) using the designated simulation pins:
     - `SIM_CLOCK_PIN`, `SIM_SEL_UN_PIN`, `SIM_SC_IN_PIN`, `SIM_SC_OUT_PIN`, and `SIM_SA_PIN`.
   - Upload the sketch to your simulation board.

2. **Operation:**  
   - The simulation will capture scan chain operations (triggered by interrupts) and decode them.
   - Debug messages will be printed on the Serial Monitor to indicate:
     - When a write scan is initiated and completed.
     - The decoded 8-bit values for each of the 16 columns.
     - When a read trigger occurs, including the raw and computed values.
   - Use these messages to validate the functionality of your scan chain operations.

---

## Project Sustainability (Pérénisation du Projet)

To ensure that this project remains maintainable and extendable over time, consider the following best practices:

- **Comprehensive Documentation:**  
  - Continue updating inline comments and this README as new features or modifications are implemented.
  - Maintain a changelog and version history using a version control system (e.g., Git).

- **Modular Code Design:**  
  - Consider refactoring the code to separate concerns (e.g., hardware control, user interface, simulation logic) into distinct modules or files.
  - This makes it easier to update parts of the code without affecting other modules.

- **Testing and Simulation:**  
  - Leverage the simulation sketch to test new functionality before deploying on actual hardware.
  - Implement unit tests for critical functions when feasible.

- **Hardware Abstraction:**  
  - Introduce abstraction layers for hardware interactions. This can simplify porting the project to other microcontroller platforms in the future.

- **Community and Support:**  
  - Engage with Arduino and embedded systems communities for feedback and to stay updated on best practices.
  - Consider open-sourcing the project to allow collaboration and contributions from other developers.

---

## Sources and References

- **Arduino Official Documentation:**  
  - [Arduino Reference](https://www.arduino.cc/reference/en/) for functions such as `digitalWrite()`, `digitalRead()`, `pinMode()`, and `delayMicroseconds()`.

- **Interrupts in Arduino:**  
  - [attachInterrupt() Documentation](https://www.arduino.cc/reference/en/language/functions/external-interrupts/attachinterrupt/) for guidance on using interrupts.

- **Digital I/O and Timing Considerations:**  
  - Consult the Arduino forums and tutorials for tips on achieving precise timing in embedded systems.

---

This README serves as both a user guide and a technical reference for anyone working with or maintaining this project. Adjust the documentation as needed to reflect any future modifications or specific hardware configurations.

Happy coding!
