Durant ce projet assez complexe en terme d'Arduino, nous avons dû séparer les tâches et fonctionner suivant plusieurs étapes :

La première étant l'écriture et la lecture de PIN. Nous avons récupéré les programmes de l'ancienne équipe qui étaient basé sur les chronogrammes des thèses en bibliographie.
La notion importante ici était le CLOCK - clk() : Elle permet de faire la différence entre un signal long ou court et savoir quand la détection de signal sur les autres ports se fait pour pouvoir retirer des informations.

clock : Simule un coup de clock. Il est important de noter ici que la carte à pointe prend en compte le changement d état de ses entrée uniquement quand elle reçoit un front montant sur le pin CLOCK. Le rapport cyclique du signal créneau envoyé n a donc aucune importance.


Les deux premiers programmes créés sont donc : 
- **arduino_read**
- **arduino_write**

L'équipe de cette année a commencé par créer **arduino_general** qui est la fusion de **arduino_read** et **arduino_write** avec les chronogrammes de l'ancienne équipe.
Ce travail de fusion a permi de faire plusieurs chose :
- un menu interractif dans le serial monitor pour savoir si on veut écrire ou lire
- précision de la **line** et de la **column**
- introduction de la **value** à écrire

Ensuite, le programme va transformer cette **value** en byte puis en séquence de 0 et de 1 sur les différents PIN des PORTS.

Il est maintenant question de savoir si notre programme marche vraiment ou non !
Première tentative : **arduino_simul**
C'est surtout un programme test qui nous a permi de mieux comprendre comment les opérations d'écriture étaient effectuées au sein de la carte Arduino.

Les signaux qui peuvent être envoyé depuis la carte Arduino sont très rapides mais ceux lu par la carte sont lent à cause des fonctions internes de la carte Arduino.
Il faut passer par une lecture suivant les PORTs et non PIN par PIN (on prend toute une série de PIN qu'on lit simultanément). Ceci nous a permi de lire jusq'à 49 clocks sur les 128 envoyés (ce qui est une grosse évolution par rapport aux 4 ou 5 clock reçu en mode séquentiel.
Cette version avec la lecture des ports en simultané avait été proposée l'année passée mais dont l'implémentation était assez étrange.
- **acquisition_unit** est un programme qui permet de tester combien de **clk()** on peut observer sur une opération de lecture / écriture
- **arduino_simul2** est un programme qui essaie de lire les informations reçu par la carte arduino de lecture / écriture

Nous avons récement découvert la fonction *captures[N]* qui permet de stocker les N différents signaux lus par la carte Arduino, avec un *Buffer circulaire*, on peut effacer les anciennes données lues pour mettre les plus récentes. Cette version permet une lecture dynamique et rapide tout en permettant le stockage des signaux. C'est le programme **arduino_simul3**.
