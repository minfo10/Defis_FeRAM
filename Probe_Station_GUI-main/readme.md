
# Probe Station GUI

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

### Pré-requis

- **Python 3.x**
- **PyQt5** : Pour la création de l'interface graphique.
- **Matplotlib** : Pour la visualisation et le tracé des données.
- **Numpy** : Pour la gestion des données numériques.
- **PySerial** : Pour la communication avec la station de sondage via des interfaces série.

### Installation

1. Cloner le dépôt :
   ```bash
   git clone https://github.com/minfo10/Defis_FeRAM.git
   ```

2. Naviguer vers le répertoire du Probe Station GUI :
   ```bash
   cd Defis_FeRAM/Probe_Station_GUI-main
   ```

3. Installer les dépendances requises :
   ```bash
   pip install -r requirements.txt
   pip install pyvisa-py
   pip install zeroconf
   ```

### Utilisation

1. Exécuter le script `main.py` pour lancer la GUI :
   ```bash
   python main.py
   ```

2. Configurer les paramètres de la sonde en utilisant la GUI et surveiller le processus en temps réel grâce aux outils de traçage intégrés.

3. Exporter les données des tests à l'aide du script `ExportData.py` ou de l'une de ses versions disponibles pour une fonctionnalité personnalisée.

## Contribution

N'hésitez pas à contribuer en soumettant des demandes de modification pour améliorer la fonctionnalité ou ajouter de nouvelles caractéristiques au Probe Station GUI.

## Licence

Ce projet est sous licence MIT - voir le fichier LICENSE pour plus de détails.

