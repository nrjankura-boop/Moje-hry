import tkinter as tk
from tkinter import ttk


class MainFrame(ttk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        
        self['borderwidth'] = 5
        self["relief"] = "ridge"
        
        self.columnconfigure(0, weight = 10)
        self.columnconfigure(1, weight = 10)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 18)
        self.columnconfigure(4, weight = 1)
        
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 15)
        self.rowconfigure(2, weight = 15)
        
        self.grid (row = 0, column = 0, sticky = 'nswe')
        
class  SubFrameUdaje (ttk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        
        self['borderwidth'] = 5
        self["relief"] = "ridge"
        
        self.rowconfigure(0, weight = 2)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        self.rowconfigure(5, weight = 1)
        
        self.columnconfigure(0, weight = 3)
        self.columnconfigure(1, weight = 1)
        self.columnconfigure(2, weight = 1)
        self.columnconfigure(3, weight = 3)
        self.columnconfigure(4, weight = 1)
        
        self.grid (row = 0, column = 3, rowspan = 2, padx = 10, pady = 5, sticky = 'nswe')
        
class  MainFrameSprava (ttk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        
        self['borderwidth'] = 5
        self["relief"] = "ridge"
        
        self.rowconfigure(0, weight = 5)
        self.rowconfigure(1, weight = 50)
        
        self.columnconfigure(0, weight = 5)
        self.columnconfigure(1, weight = 5)
        self.columnconfigure(2, weight = 65)
        self.columnconfigure(3, weight = 1)
        self.columnconfigure(4, weight = 30)
        
        self.grid (row = 0, column = 0, sticky = 'nswe')
        
        
class  MainFrameRozdelenie (tk.Frame):
    
    def __init__(self, container):
        super().__init__(container)
        
        self['borderwidth'] = 5
        self["relief"] = "ridge"
        self["bg"] = "#ffffff"
        
        self.rowconfigure(0, weight = 3)
        self.rowconfigure(1, weight = 3)
        self.rowconfigure(2, weight = 3)
        self.rowconfigure(3, weight = 50)
        
        self.columnconfigure(0, weight = 15)
        self.columnconfigure(1, weight = 2)
        self.columnconfigure(2, weight = 2)
        self.columnconfigure(3, weight = 2)
        self.columnconfigure(4, weight = 2)
        self.columnconfigure(5, weight = 2)
        self.columnconfigure(6, weight = 2)
        self.columnconfigure(7, weight = 1)
        self.columnconfigure(8, weight = 20)
        self.columnconfigure(9, weight = 1)
        
        self.grid (row = 0, column = 0, sticky = 'nswe')