# -*- coding: utf-8 -*-
"""
Created on Fri Oct  8 10:25:25 2021

@author: XuL
"""

import tkinter as tk
from tkinter import ttk

import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure

main = tk.Tk()

leftFrame = tk.Frame(main)
leftFrame.grid(row=0, column=0)

leftSeparator1 = ttk.Separator(leftFrame, orient='horizontal')
leftSeparator1.grid(row=0, column=0, columnspan=3, pady=10, sticky='ew')

leftSeparator2 = ttk.Separator(leftFrame, orient='vertical')
leftSeparator2.grid(row=0, rowspan=3, column=2, padx=10, sticky='ns')

leftSeparator3 = ttk.Separator(leftFrame, orient='horizontal')
leftSeparator3.grid(row=2, column=0, columnspan=3, pady=10, sticky='ew')

leftSeparator4 = ttk.Separator(leftFrame, orient='vertical')
leftSeparator4.grid(row=0, rowspan=3, column=0,  padx=10, sticky='ns')

leftLabel = tk.Label(leftFrame, text='RIGHT FRAME', font='arial 15')
leftLabel.grid(row=1, column=1)

rightFrame = tk.Frame(main)
rightFrame.grid(row=0,column=1)

f = Figure(figsize=(5,5), dpi=100)
a = f.add_subplot(111)
a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])

canvas = FigureCanvasTkAgg(f, rightFrame)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
toolbar = NavigationToolbar2Tk(canvas, rightFrame)
toolbar.update()
canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# tk.Frame.__init__(self, parent)
#         label = tk.Label(self, text="Graph Page!", font=LARGE_FONT)
#         label.pack(pady=10,padx=10)

#         button1 = ttk.Button(self, text="Back to Home", command=lambda: controller.show_frame(StartPage))
#         button1.pack()



        

#         canvas = FigureCanvasTkAgg(f, self)
#         canvas.draw()
#         canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

#         toolbar = NavigationToolbar2Tk(canvas, self)
#         toolbar.update()
#         canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

main.mainloop()