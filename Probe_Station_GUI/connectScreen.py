# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 15:54:49 2021

@author: XuL
"""

import os
import pyvisa
import tkinter as tk

class connectScreen(tk.Tk):
    def __init__(self):
        
        self.connected = False
        
        tk.Tk.__init__(self)
        self.geometry('320x180')
        self.title('Réglage channel') # Titre
        self.iconbitmap(os.getcwd() + '\icon.ico') # Icon de l'app
        self.config(background='light yellow')
        self.option_add('*font','arial 15')
        self.option_add('*foreground','black')
        connectButton = tk.Button(self, text='Connection SMU', command=self.checkSMU, relief='raised')
        connectButton.place(bordermode='inside', width=160, height=90, x=80, y=45)
        testButton = tk.Button(self, text='Mode test', command=self.modeTest, relief='raised')
        testButton.place(bordermode='inside', width=160, height=30, x=80, y=150)

    def checkSMU(self):
        rm = pyvisa.ResourceManager()
        if len(rm.list_resources())==1:
            self.connected = True
            self.inst = rm.open_resource(rm.list_resources()[0])
            rm.read_termination='\n'
            rm.write_termination='\n'
            self.destroy()
        else:
            
            tk.messagebox.showerror(title='Error', message='Failed to connect')
            print('Failed to connect')
    
    def modeTest(self):
        self.connected = True
        self.inst = 'Mode test'
        self.destroy()   