#include <iostream>
#include <SerialStream.h> // Nécessite la bibliothèque SerialStream

int main() {
    LibSerial::SerialStream serial_port;
    serial_port.Open("/dev/ttyUSB0"); // Remplace par le port approprié
    serial_port.SetBaudRate(LibSerial::SerialStreamBuf::BAUD_9600);
    serial_port.SetCharSize(LibSerial::SerialStreamBuf::CHAR_SIZE_8);
    serial_port.SetFlowControl(LibSerial::SerialStreamBuf::FLOW_CONTROL_NONE);
    serial_port.SetParity(LibSerial::SerialStreamBuf::PARITY_NONE);
    serial_port.SetNumOfStopBits(1);

    if (!serial_port.IsOpen()) {
        std::cerr << "Erreur lors de l'ouverture du port série." << std::endl;
        return 1;
    }

    std::string data_to_send;
    while (true) {
        std::cout << "Entrez les données à envoyer (ou 'exit' pour quitter) : ";
        std::getline(std::cin, data_to_send);
        if (data_to_send == "exit") {
            break;
        }
        serial_port << data_to_send << std::endl; // Envoyer les données
    }

    serial_port.Close();
    return 0;
}