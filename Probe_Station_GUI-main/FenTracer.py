# -*- coding: utf-8 -*-
"""
Created on Tue Mar  2 15:21:00 2021

@author: XuL
"""

import pyvisa
import matplotlib.pyplot as plt
import time

class Reglage:
    def __init__(self, mini, maxi, unite, npoint, numero, comp):
        self.mini = mini
        self.maxi = maxi
        self.unite = unite      # ce qu'on impose
        self.npoint = npoint    
        self.num = numero       # channel utiliser
        self.comp = comp        # compliance
        
        if unite == "CURR":
            self.mes = "VOLT"   
        elif unite == "VOLT":
            self.mes = "CURR"
        
    # def PrintReglage(self):
    #     print('nom = nom de la channel = {} \n'.format(self.nom))
    #     print('unite = grandeur à imposer = {} \n'.format(self.unite))
    #     print('mes = grandeur à mesurer = {} \n'.format(self.mes))

    #     print('npoint = {} \n'.format(self.npoint))
    #     print('mini = {} \n'.format(self.mini))
    #     print('maxi = {} \n'.format(self.maxi))

    #     print('comp = compliance du SMU = {} \n'.format(self.comp))
        
class FenTracerVar:
    def __init__(self, nomInstrument, deltaT, ch_used, reglage): 
        self.inst = nomInstrument
        self.deltaT = deltaT        # Temps de relaxation
        self.ch_used = ch_used    # Les channels used
        self.reglage = reglage
        
    def carac(self):
        
        self.mesure = []
        
        if self.ch_used == '1' or self.ch_used == '2': # Mesure 2 pointes
            
            debMes = self.reglage.mini
            finMes = self.reglage.maxi
            npoint = self.reglage.npoint
            num = self.reglage.num
            
            self.VarMain = [debMes + (finMes-debMes)*i/npoint for i in range(npoint)]
            
            self.inst.write(":OUTP"+num+" ON")             
            self.inst.write('SENS{}:{}:PROT {}'.format(self.reglage.num, self.reglage.mes, self.reglage.comp))
            self.inst.write(":SOUR"+num+":FUNC:MODE "+self.reglage.unite)
            
            for i in range(npoint):
                self.inst.write("SOUR{}:{} {}".format(num, self.reglage.unite, self.VarMain[i]))
                time.sleep(self.deltaT)
                
                self.mesure.append(float(self.inst.query(":MEAS:{}? (@{})".format(self.reglage.mes, num))))
            
            self.inst.write(":SOUR{}:{} 0".format(num, self.reglage.unite))

            self.inst.write(":OUTP"+num+" OFF")

        elif self.ch_used == 'main-1 & 2' or self.ch_used == 'main-2 & 1':
            
            if self.ch_used == 'main-1 & 2':
                reg1 = self.reglage[0]
                reg2 = self.reglage[1]
            elif self.ch_used == 'main-2 & 1':
                reg1 = self.reglage[1]
                reg2 = self.reglage[0]
            
            self.VarMain = [reg1.mini + (reg1.maxi-reg1.mini)*i/reg1.npoint for i in range(reg1.npoint)]
            self.VarNonMain = [reg2.mini + (reg2.maxi-reg2.mini)*i/reg2.npoint for i in range(reg2.npoint)]
            
            self.inst.write(':OUTP1 ON')
            self.inst.write(':OUTP2 ON')
            
            self.inst.write(':SENS1:'+reg1.mes+':PROT '+str(reg1.comp))
            self.inst.write(':SENS2:'+reg2.mes+':PROT '+str(reg2.comp))
            
            self.inst.write(':SOUR{}:FUNC:MODE {}'.format(reg1.num, reg1.unite))
            self.inst.write(':SOUR{}:FUNC:MODE {}'.format(reg2.num, reg2.unite))
            
            for i in range(reg2.npoint):
                self.inst.write('SOUR{}:{} {}'.format(reg2.num, reg2.unite, self.VarNonMain[i]))
                time.sleep(self.deltaT)

                Y1 = []
                Y2 = []
                for j in range(reg1.npoint):
                    self.inst.write("SOUR{}:{} {}".format(reg1.num, reg1.unite, self.VarMain[j]))
                    time.sleep(self.deltaT)
                    Y1.append(float(self.inst.query(":MEAS:{}? (@{})".format(reg1.mes, reg1.num))))
                    Y2.append(float(self.inst.query(":MEAS:{}? (@{})".format(reg2.mes, reg2.num))))
                self.mesure.append([Y1,Y2])

            self.inst.write(":SOUR{}:{} 0".format(reg1.num, reg1.unite))
            self.inst.write(":SOUR{}:{} 0".format(reg2.num, reg2.unite))
            self.inst.write(":OUTP1 OFF")
            self.inst.write(":OUTP2 OFF")
            
        else:
            print("wtf")
                
# rm = pyvisa.ResourceManager()
# SMU = rm.open_resource(rm.list_resources()[0])

# # Reglage(min, max, unite, npoint, channel, compliance)

# # Test: Résistance
# reg = Reglage(-5, 5, 'VOLT', 50, "2", 1)
# idk = FenTracerVar(SMU, 0.01, "1", reg) 
# idk.carac()
# plt.plot(idk.VarMain, idk.mesure)
# plt.xlabel("Vd")
# plt.ylabel("Id")

# # Test: Transistor
# reg1 = Reglage(0, 10, "VOLT", 50, "1", 1) # Vds
# reg2 = Reglage(3, 5, "VOLT", 3, "2", 1) # Vgs
# idk = FenTracerVar(SMU, 0.01, '1 Main & 2 Step', [reg1,reg2])
# idk.carac()
# for j in range(3):
#     Id = [idk.mesure[j][0][i] for i in range(50)]
#     plt.plot(idk.VarMain, Id)
# mesure = idk.mesure
# plt.xlabel("Vd")
# plt.ylabel("Id")

# SMU.close()