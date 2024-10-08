# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 21:27:00 2021

@author: XuL
"""

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import random

class App_Window(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        
        self.mesure = [1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5]
        self.nbPoint = len(self.mesure[0])
        
        self.leftFrame = frame1(self)
        self.leftFrame.grid(row=0, column=0)
        
        self.rightFrame = frame2(self)
        self.rightFrame.grid(row=0, column=1)
        
    def increment(self):
        for i in range(1):
            for j in range(self.nbPoint):
                self.mesure[i][j] = random.randint(0,10)
        self.rightFrame.a.clear()
        self.rightFrame.a.plot(self.mesure[0], self.mesure[1])
        self.rightFrame.canvas.draw()
        
class frame1(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.leftSeparator1 = ttk.Separator(self, orient='horizontal')
        self.leftSeparator1.grid(row=0, column=0, columnspan=3, pady=10, sticky='ew')
        
        self.leftSeparator2 = ttk.Separator(self, orient='vertical')
        self.leftSeparator2.grid(row=0, rowspan=3, column=2, padx=10, sticky='ns')
        
        self.leftSeparator3 = ttk.Separator(self, orient='horizontal')
        self.leftSeparator3.grid(row=2, column=0, columnspan=3, pady=10, sticky='ew')
        
        self.leftSeparator4 = ttk.Separator(self, orient='vertical')
        self.leftSeparator4.grid(row=0, rowspan=3, column=0,  padx=10, sticky='ns')
        
        self.leftButton = tk.Button(self, text='+1', command=parent.increment, font='arial 15')
        self.leftButton.grid(row=1, column=1)        
        
class frame2(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        
        f = Figure(figsize=(5,5), dpi=100)
        self.a = f.add_subplot(111)
        self.a.plot(parent.mesure[0], parent.mesure[1])
        
        self.canvas = FigureCanvasTkAgg(f, self)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        self.toolbar = NavigationToolbar2Tk(self.canvas, self)
        self.toolbar.update()
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
main = App_Window()
main.mainloop()
        
        