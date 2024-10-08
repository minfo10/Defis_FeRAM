# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 15:54:00 2021

@author: Laurent XU
"""

##################
# MAIN PROGRAMME #
##################

import connectScreen as cS
import defaultInterface

# Ecran de connection a la SMU, on ouvre l'interface de mesure que si on arrive a se connecter a la SMU
pre_main = cS.connectScreen()
pre_main.mainloop()

# On lance l'interface de mesure
# Le modeTest ne sert pas a faire des mesures, justes pour voir l'interface en cas de changement d'aesthetic
if pre_main.connected == True:
    print(pre_main.inst)
    main = defaultInterface.AppWindow(pre_main.inst)
    main.mainloop()
else:
    print('Failed to connect bis')