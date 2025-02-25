# Projet Arduino

## Fonctionnement Général
L'objectif principal est de gérer l'écriture et la lecture sur les PINs de l'Arduino en utilisant un signal d'horloge (**CLOCK - clk()**) pour synchroniser les opérations. La carte ne prend en compte les changements d'état de ses entrées qu'à la réception d'un front montant sur le PIN CLOCK, rendant le rapport cyclique du signal créneau envoyé sans importance.

## Développement des Programmes

Durant ce projet, nous avons dû séparer les tâches et fonctionner suivant plusieurs étapes :

### 1. Premiers Programmes
- **arduino_read** : Gestion de la lecture des données.
- **arduino_write** : Gestion de l'écriture des données.

Ces programmes étaient issus des travaux de l'ancienne équipe.

### 2. Fusion et Optimisation
- **arduino_general** : Fusion des programmes **arduino_read** et **arduino_write**.
  - Création d'un menu interactif dans le Serial Monitor permettant de choisir entre lecture et écriture.
  - Prise en compte des coordonnées (**line** et **column**).
  - Introduction de la **value** à écrire, convertie en byte puis en séquence binaire envoyée sur les différents PINs grâce aux chronogrammes créés par l'ancienne équipe.

### 3. Tests et Simulations
- **arduino_simul** : Programme test pour comprendre l'écriture des données sur la carte Arduino.
- **acquisition_unit** : Programme permettant de tester combien de cycles d'horloge (**clk()**) peuvent être observés sur une opération de lecture/écriture.

### 4. Optimisation de la Lecture
L'ancienne approche lisait les signaux **PIN par PIN**, ce qui était inefficace. Une lecture par **PORTs simultanés** a été implémentée, permettant d'augmenter le nombre de **clk()** observés de 4-5 à 49 sur 128 envoyés.
- **arduino_simul2** : Programme testant la capacité de lecture simultanée des informations reçues.

Cette version avec la lecture des ports en simultané avait été proposée l'année passée mais dont l'implémentation était assez étrange. Cette année, on a réussi à stabiliser cette méthode, ce qui a représenté une grosse avancée dans la fluidité du processus de lecture.

### 5. Implémentation de Matrice Conditionnelle
Il est maintenant question de voir si on peut aller plus loin avec une potentielle **matrice conditionnelle**. L'idée ici, c'est de restreindre l'accès à certains points de la matrice en fonction des entrées détectées. 

- **mat_condition** : Expérimentation d'une matrice conditionnelle avec des signaux continus 0V - 5V pour tester si on peut autoriser ou non l'accès à l'écriture sous certaines conditions.

On utilise toujours la lecture séquentielle, ce qui n'est pas optimal. Pour l'instant, c'est un prototype, car il nous manque une bonne compréhension du stockage des données. Mais les premiers tests sont prometteurs.

### 6. Utilisation de la Fonction *buffer[N]*
Dernière découverte qui change un peu tout : la fonction *buffer[N]*. Grâce à elle, on peut stocker **les N derniers signaux lus** dans un **buffer circulaire**, ce qui permet d’effacer les anciennes données et de garder les plus récentes sans ralentir la lecture.

- **arduino_simul3** : Première version du programme qui exploite cette nouvelle fonctionnalité. 

C’est une avancée énorme : on a maintenant une lecture dynamique et rapide tout en optimisant le stockage des signaux. On continue d’expérimenter pour voir jusqu’où on peut pousser cette méthode.
