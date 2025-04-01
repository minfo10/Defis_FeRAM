# Défis d'IPhy - Mémoires du futur

## Sommaire

- [Arduino](#Arduino)
- [Interface utilisateur](#Interface-utilisateur)

## Pré-requis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Python 3.x** : Assurez-vous d'avoir une version récente de Python. Vous pouvez le télécharger depuis [python.org](https://www.python.org/downloads/).
- **get-pip** : Utilisez `get-pip.py` pour installer `pip`, le gestionnaire de packages Python.
- **Arduino IDE** : Téléchargez et installez l'[IDE Arduino](https://www.arduino.cc/en/software).

Nous allons utiliser ces bibliothèques Python :
- **PyQt5** : Bibliothèque pour la création d'interfaces graphiques.
- **Numpy** : Pour le calcul numérique et la gestion de tableaux.
- **PySerial** : Pour la communication série avec des appareils.
- **tkinter** : Bibliothèque standard pour créer des interfaces graphiques.
- **zeroconf** : Pour la découverte automatique de services sur un réseau local. 
- **pyvisa** : Pour contrôler des instruments de mesure via des interfaces VISA.

## Installation et Utilisation

1. **Cloner le dépôt** :
   ```bash
   git clone https://github.com/minfo10/Defis_FeRAM.git
   cd Defis_FeRAM
   ```
   
2. **Téléverser le programme Arduino sur la carte moniteur** :
   - Pour Windows :
   ```bash
   cd Arduino/arduino_general
   explorer .
   ```
   - Pour GNOME (Ubuntu, Fedora...) :
   ```bash
   cd Arduino/arduino_general
   nautilus .
   ```
   - Pour MacOS :
   ```bash
   cd Arduino/arduino_general
   open .
   ```
   - Lancer l'IDE Arduino en ouvrant le fichier `.ino`.
   - Regarder le `baudrate` et le `port`.
   - Compiler et téléverser sur votre carte Arduino.

3. **Créer et activer un environnement virtuel Python**

   La création d'un environnement virtuel Python peut prendre un peu de temps. Si jamais cela dépasse 2mins, il se peut que vous ayez déjà un environnement fonctionnel donc faites CRTL+C et passez à la suite.
   - Pour Windows :
   ```bash
   cd ..
   cd ..
   python -m venv env #Créez un environnement virtuel Python
   .\env\Scripts\activate #Activez l'environnement virtuel
   ```
   - Pour Linux/MacOS :
   ```bash
   cd ..
   cd ..
   python3 -m venv env #Créez un environnement virtuel Python
   source env/bin/activate #Activez l'environnement virtuel
   ```
   
5. **Installer les dépendances Python** :
   ```bash
   pip install -r requirements.txt
   ```
   Si vous avez une erreur avec `tkinter`, il se peut que vous deviez installer Python avec `tkinter` inclus. Vous pouvez vérifier si `tkinter` est installé avec cette commande :
   ```bash
   python -m tkinter
   ```
   Si cela ouvre une fenêtre avec le message "This is Tk", vous avez `tkinter` installé. Sinon, vous devrez peut-être installer ou réinstaller Python en vous assurant que `tkinter` est inclus.
   
6. **Exécutez le programme `main.py` avec Python** :
   ```bash
   cd user_interface
   python main.py
   ```
---
## Arduino

### Objectif du Programme

Ce programme permet d'effectuer des opérations de lecture et d'écriture sur une mémoire FeRAM, en utilisant une carte Arduino.
Le code est optimisé pour manipuler directement les registres matériels des ports afin de réduire le temps de calcul et d'améliorer les performances.

#### Manipulation directe des ports Arduino
Pour garantir une meilleure efficacité, le programme n'utilise pas les fonctions standard digitalRead et digitalWrite pour accéder aux pins. À la place, il manipule directement les ports du microcontrôleur intégré, en interagissant avec leurs registres internes.
    
### Théorie : Ports et registres du microcontrôleur
Le microcontrôleur d'une carte Arduino est divisé en ports, chacun responsable d'un groupe de pins.
Les cartes de type Arduino UNO disposent de trois principaux ports numériques :

- `Port D` : Contrôle les pins numériques 0 à 7.
- `Port B` : Contrôle les pins numériques 8 à 13.
- `Port C` : Contrôle les pins analogiques (`A0` à `A5`).

Chaque port est constitué de trois registres binaires (8 bits chacun) :

- `PORTx` : Utilisé pour écrire (changer l'état) sur les pins.
- `PINx` : Utilisé pour lire l'état des pins.
- `DDRx` : Définit si les pins sont en entrée ou en sortie (Data Direction Register).

*Exemple* : État des pins d'un port
Si les pins numériques 1 et 3 sont à l'état haut (`HIGH`) et les autres pins du port D sont à l'état bas (`LOW`), la valeur du registre PORTD sera : `0101 0000` (en binaire).

**Remarque** : L'ordre des bits est inversé. Le bit de poids faible (le dernier à droite) correspond au pin 0, tandis que le bit de poids fort (le premier à gauche) correspond au pin 7.

### Opérations binaires pour manipuler les pins

- **Passage à l'état haut (`HIGH`)**

   Pour mettre un pin à l'état haut, on utilise une opération OU inclusif (`OR`) sur le registre correspondant :
   ```bash
              0101 0000  (valeur actuelle du registre `PORTD`)
          OU  0000 0100  (bit correspondant au pin 5)
          =   0101 0100  (le pin 5 est maintenant à l'état haut)
   ```

- **Passage à l'état bas (`LOW`)**

   Pour mettre un pin à l'état bas, on utilise une opération ET NON (`AND NOT`) :
   ```bash
                 0101 0100  (valeur actuelle du registre `PORTD`)
          ET NON 0000 0100  (bit correspondant au pin 5)
          =      0101 0000  (le pin 5 est maintenant à l'état bas)
   ```

- **Lecture de l'état d'un pin**

   Pour lire l'état d'un pin, on effectue une opération ET (`AND`) sur le registre correspondant, puis on interprète le résultat :
   ```bash
              0101 0000  (valeur actuelle du registre `PIND`)
          ET  0100 0000  (bit correspondant au pin 6)
          =   0100 0000  (résultat non nul : le pin 6 est à l'état haut)
   ```


### Implémentation

Fonctions utilitaires
Pour simplifier la manipulation des ports, trois fonctions de base ont été définies :

- `pON(pin)` : Passe le pin spécifié à l'état haut.
- `pOFF(pin)` : Passe le pin spécifié à l'état bas.
- `lect(pin)` : Lit l'état d'un pin et retourne 1 (haut) ou 0 (bas).

Ces fonctions permettent d'encapsuler les opérations binaires tout en offrant une interface claire pour l'utilisateur.

### Programmes Arduino disponibles
Le projet inclut plusieurs programmes spécialisés :

- `arduino_read` : Programme dédié à la lecture d'une ligne complète dans la mémoire.
- `arduino_write` : Programme dédié à l'écriture d'une ligne complète.
- `arduino_simul` : Programme simulant le comportement d'une mémoire FeRAM.
- `arduino_general` : Programme principal combinant les fonctionnalités de lecture et d'écriture.


---

## Interface-Utilisateur

L'interface graphique (GUI) est conçue pour pour caractériser des dispositifs FeRAM. La GUI permet aux utilisateurs d'envoyer et recevoir les données que l'on souhaite au travers de la mémoire FeRAM.

### Structure

- `main.py` : Script principal pour lancer l'interface graphique.
- `Interface.py` : Contient la classe principale pour l'interface utilisateur, avec gestion de la connexion série à l'Arduino, l'envoi et la réception de données, et l'affichage des résultats et gère aussi la fonctionnalité d'importation et d'exportation des données. Vous pouvez importer des fichiers `.txt` contenant des données pour les afficher ou exporter des données sous forme de fichiers texte.

### Détails sur l'interface graphique
L'interface graphique se compose des sections suivantes :

1. **Connexions série avec Arduino** : Configurez les paramètres de communication (`port` et `baud rate`) et vérifiez la connexion avec l'Arduino. Un voyant de connexion indique si la connexion est établie ou non.
2. **Écriture de données vers l'Arduino** : Envoyez des données numériques vers l'Arduino. Vous pouvez spécifier une ligne et une colonne à écrire.
3. **Lecture des données depuis l'Arduino** : Lisez les données envoyées par l'Arduino après avoir spécifié la ligne et la colonne de lecture.
4. **Importation et exportation des données** : Utilisez les menus pour importer ou exporter des fichiers `.txt` contenant des données. L'importation affichera les données dans une fenêtre pop-up, tandis que l'exportation enregistrera les données actuelles dans un fichier `.txt`.

---
## Contribution

N'hésitez pas à contribuer en soumettant des demandes de modification pour améliorer la fonctionnalité ou ajouter de nouvelles caractéristiques au Probe Station GUI.

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.



