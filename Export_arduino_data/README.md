
# Instructions

Ce dossier contient deux programmes python :
- memory.py
- get-pip.py

Le programme memory.py est le code principal avec lequel nous allons travailler. Le but de ce programme est d'écrire les données du terminal Arduino dans un fichier .txt

Ce programme utilise cependant la librarie serial, il faudra donc l'importer et installer au préalable get-pip.py.
Il faudra ensuite ouvrir le terminal, se rendre dans le dossier ou est get-pip.py, et installer pyserial :
    ```bash
    pip install pyserial
    ```
Sur Windows 11, il sera peut être nécessaire d'ajouter python3 :
    ```bash
    pythin3 pip install pyserial 
    ```
Votre programme sera ensuite prêt à être utilisé, penser bien à vérifier le port sur lequel votre Arduino est branchée, et vous voilà avec une interface de communication simple entre votre Arduino et python. 
