# Défis d'IPhy - Mémoires du futur

## Sommaire

- [Arduino](##Arduino)
- [Interface utilisateur](##Interface-utilisateur)

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

## Installation

1. **Cloner le dépôt** :
   Clonez le projet localement en utilisant la commande suivante :
   ```bash
   git clone https://github.com/minfo10/Defis_FeRAM.git
   cd Defis_FeRAM
   ```
2. **Installer les dépendances Python** : Assurez-vous d'utiliser un environnement virtuel (optionnel mais recommandé) pour isoler les dépendances :
   ```bash
   python -m venv env
   source env/bin/activate   # Sous Windows : env\Scripts\activate
   pip install -r requirements.txt
   ```

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

| Exemple : État des pins d'un port
| Si les pins numériques 1 et 3 sont à l'état haut (`HIGH`) et les autres pins du port D sont à l'état bas (`LOW`), la valeur du registre PORTD sera :
| `0101 0000` (en binaire).
| 
| Remarque : L'ordre des bits est inversé. Le bit de poids faible (le dernier à droite) correspond au pin 0, tandis que le bit de poids fort (le premier à gauche) correspond au pin 7.

### Opérations binaires pour manipuler les pins


Passage à l'état haut (`HIGH`)
Pour mettre un pin à l'état haut, on utilise une opération OU inclusif (`OR`) sur le registre correspondant :
|     0101 0000  (valeur actuelle du registre `PORTD`)
| OU  0000 0100  (bit correspondant au pin 5)
| =   0101 0100  (le pin 5 est maintenant à l'état haut)


Passage à l'état bas (`LOW`)
Pour mettre un pin à l'état bas, on utilise une opération ET NON (`AND NOT`) :
|        0101 0100  (valeur actuelle du registre `PORTD`)
| ET NON 0000 0100  (bit correspondant au pin 5)
| =      0101 0000  (le pin 5 est maintenant à l'état bas)


Lecture de l'état d'un pin
Pour lire l'état d'un pin, on effectue une opération ET (`AND`) sur le registre correspondant, puis on interprète le résultat :
|     0101 0000  (valeur actuelle du registre `PIND`)
| ET  0100 0000  (bit correspondant au pin 6)
| =   0100 0000  (résultat non nul : le pin 6 est à l'état haut)

### Implémentation
Fonctions utilitaires
Pour simplifier la manipulation des ports, trois fonctions de base ont été définies :

- `pON(pin)` : Passe le pin spécifié à l'état haut.
- `pOFF(pin)` : Passe le pin spécifié à l'état bas.
- `lect(pin)` : Lit l'état d'un pin et retourne 1 (haut) ou 0 (bas).
Ces fonctions permettent d'encapsuler les opérations binaires tout en offrant une interface claire pour l'utilisateur.


### Programmes Arduino disponibles
Le projet inclut plusieurs programmes spécialisés :

`arduino_read` : Programme dédié à la lecture d'une ligne complète dans la mémoire.
`arduino_write` : Programme dédié à l'écriture d'une ligne complète.
`arduino_simul` : Programme simulant le comportement d'une mémoire FeRAM.
`arduino_general` : Programme principal combinant les fonctionnalités de lecture et d'écriture.


---

## user_interface

Ce dépôt contient une interface graphique (GUI) conçue pour contrôler et collecter des données d'une station de sondage, spécifiquement pour la caractérisation des dispositifs FeRAM (Mémoire vive ferroélectrique). La GUI permet aux utilisateurs d'automatiser les séquences de sondage, de visualiser les données en temps réel et d'exporter les résultats pour des analyses supplémentaires.

### Fonctionnalités

- **Contrôle automatisé de la station de sondage** : Gérez les mouvements des sondes avec des configurations précises.
- **Visualisation des données en temps réel** : Tracez et affichez les données des tests.
- **Fonction d'exportation de données** : Exportez les données pour des analyses supplémentaires, avec plusieurs versions de scripts disponibles.
- **Conception modulaire** : La structure du code permet une modification et une extension faciles.

### Structure du projet

- `main.py` : Script principal pour lancer l'interface graphique.
- `ExportData.py` : Gère la fonctionnalité d'exportation des données, avec plusieurs versions (`v1` à `v4`) disponibles dans le répertoire `work_to_do` pour différentes implémentations.
- `FenTracer.py` : Gère le traçage et la visualisation des données.
- `test_plt_and_frame/` : Contient des scripts de test pour les tracés et la combinaison des cadres graphiques.
  - `frame_side_by_side.py`, `update_graph.py` : Implémente et teste les tracés de données avec les interfaces de cadre.
- `work_to_do/` : Contient des scripts en cours, tels que `transistor.py` et des fichiers icônes comme `icon_transistor.png`.
- `Manuel_programmation_Keysight.pdf` : Un manuel de programmation pour le matériel Keysight utilisé dans le projet.


### Utilisation

1. Exécuter le script `main.py` pour lancer la GUI :
   ```bash
   python main.py
   ```

2. Configurer les paramètres de la sonde en utilisant la GUI et surveiller le processus en temps réel grâce aux outils de traçage intégrés.

3. Exporter les données des tests à l'aide du script `ExportData.py` ou de l'une de ses versions disponibles pour une fonctionnalité personnalisée.

### Contribution

N'hésitez pas à contribuer en soumettant des demandes de modification pour améliorer la fonctionnalité ou ajouter de nouvelles caractéristiques au Probe Station GUI.

### Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.



