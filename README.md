# Défis d'IPhy - Mémoires du futur

## Sommaire

- [Arduino](#Arduino)

- [Interface utilisateur](user_interface)

## Pré-requis

Avant de commencer, assurez-vous d'avoir les éléments suivants installés sur votre machine :

- **Python 3.x** : Assurez-vous d'avoir une version récente de Python. Vous pouvez le télécharger depuis [python.org](https://www.python.org/downloads/).
- **get-pip** : Utilisez `get-pip.py` pour installer `pip`, le gestionnaire de packages Python.

Nous allons utiliser ces librairies :
- **PyQt5** : Bibliothèque pour la création d'interfaces graphiques.
- **Numpy** : Pour le calcul numérique et la gestion de tableaux.
- **PySerial** : Pour la communication série avec des appareils.
- **tkinter** : Bibliothèque standard pour créer des interfaces graphiques.
- **zeroconf** : Pour la découverte automatique de services sur un réseau local. 
- **pyvisa** : Pour contrôler des instruments de mesure via des interfaces VISA.


## Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/minfo10/Defis_FeRAM.git
   ```

2. Installer les dépendances requises :
   ```bash
   pip install -r requirements.txt
   ```

## Arduino

Ce programme permet d'écrire et de lire une ligne complète de la carte mémoire.

### Changement de l'état d'un pin - Manipulation directe des ports de la carte Arduino
Afin de gagner en efficacité et en temps de calcul, ce programme n'utilise pas les fonctions de base pour changer l'état des pins de la carte (digitalRead et digitalWrite) mais manipule directement ses ports.

#### Ports et registres
Les microcontrolleurs intégrés aux cartes arduinos sont composés de 3 ports :
- le port **D** est responsable des **pins numériques 0 à 7**;
- le port **B** est responsable des **pins numériques 8 à 13**;
- le port **B** est responsable des **pins analogiques**.

Chaque port est lui-même composé de 3 registres à décalages (concrètement 3 variables bianaires appelées dans le code).
- Le registre **PORT*** permet le changement de l'état d'un pin;
- Le registre **PIN*** permet la lecture de l'état d'un pin.

##### Exemple
Si les pins numériques **1** et **3** sont à l'état haut et les pins **0**, **2**, **4**, **5**, **6** et **7** sont à l'état bas, on aura :
```
PIND = 0101 0000 = PORTD
```
Attention à l'ordre de lecture ! Le bit de poids faible code ici l'état du pin 7 et non celui du pin 0.

Pour plus d'informations, cf https://docs.arduino.cc/retired/hacking/software/PortManipulation/.


#### Passage à l'état haut
Il est donc possible de passer l'état d'un pin de l'état bas à l'état haut en appliquant l'opération arithmétique binaire **OU inclusif** à la variable **PORT***.

##### Exemple
On reprend l'exemple précédent. On souhaite passer le pin 5 à l'état haut.

```
    0101 0000 
OU  0000 0100
=   0101 0100
```

#### Passage à l'état bas
De la même façon, il est possible de passer l'état d'un pin de l'état haut à l'état bas en appliquant l'opération arithmétique binaire **ET NON** à la variable **PORT***.

##### Exemple
On reprend l'exemple précédent. On souhaite passer le pin 5 à l'état bas.

```
        0101 0100 
ET NON  0000 0100 
=       0101 0000
```
#### Lecture d'un pin
Pour lire l'état d'un pin, il suffit d'isoler sa valeur en appliquant l'opération arithmétique binaire **ET** à la variable **PIN*** puis d'interpréter le résultat (nul ou non).

##### Exemple
Lecture du pin 1.

```
    0101 0000 
ET  0100 0000
=   0100 0000
=   64
=/= 0
```

#### Implémentation
Ainsi, pour lire ou écrire l'état d'un pin, le programe appelle les fonctions **pON** (passage à l'état haut), **pOFF** (passage à l'état bas) et **lect** définies en entête du code.

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



