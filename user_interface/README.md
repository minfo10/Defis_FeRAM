# Défi FeRAM - Interface graphique Python avec Tkinter

## Description
Dans notre **Défi FeRAM**, nous utilisons une interface graphique (GUI) développée en **Python** utilisant le module **Tkinter**. Elle permet de communiquer avec un **Arduino** pour lire et écrire des données sur une mémoire **FeRAM**. Cette interface offre les fonctionnalités suivantes :

- **Détection automatique du port Arduino**
- **Envoi et réception de données vers/depuis l'Arduino**
- **Importation et exportation de fichiers texte**
- **Interface intuitive et facile à utiliser**

L'application est conçue pour être utilisée par des utilisateurs qui souhaitent interagir avec un Arduino en utilisant un port série pour lire et écrire des données.

## Fonctionnalités

### 1. **Connexion à Arduino**
   - Détection automatique du port Arduino connecté au système.
   - Configuration du baud rate pour la communication.
   - Vérification de la connexion avec l'Arduino.
   
### 2. **Lecture et Écriture sur FeRAM**
   - Permet d'écrire un nombre sur une cellule de mémoire FeRAM spécifique (définie par la ligne et la colonne).
   - Permet de lire la donnée stockée à une position spécifique sur la FeRAM.

### 3. **Exportation et Importation des Données**
   - Exportation des données depuis l'Arduino vers un fichier `.txt`.
   - Importation de données depuis un fichier `.txt` pour les afficher ou les utiliser dans l'application.

### 4. **Aide et Support**
   - Menu d'aide avec un lien vers le dépôt GitHub pour plus d'informations.

## Menu

L'application dispose d'un menu avec plusieurs options :
   - Data : Pour importer ou exporter des fichiers .txt.
   - Arduino : Pour réinitialiser l'Arduino (en cas de besoin).
   - Help : Pour obtenir de l'aide et accéder à la documentation sur GitHub.

## Code et Conception

Le code est structuré autour de la classe principale Interface qui gère l'interface graphique et la communication avec l'Arduino via le port série.

Les principales fonctionnalités de l'application sont organisées en sections :
   - Connection Section : Gère la connexion à l'Arduino.
   - Write Section : Permet d'écrire des données dans la mémoire FeRAM.
   - Read Section : Permet de lire les données stockées dans la mémoire FeRAM.
   - Information Section : Affiche des informations sur la connexion et les étapes à suivre.
