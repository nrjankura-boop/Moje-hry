import tkinter as tk
from tkinter import ttk


class OknoPrePrvokDiety(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.geometry('400x200')
        self.title('Pridajte prvok diety')
        self.resizable(0, 0)
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        
        font_label = ('Verdana', 12)
        font_nazov_potraviny_label = ('Verdana', 12, 'bold')
        font_entry = ('Verdana', 12)
        
        ttk.Label(self, text = 'Názov diety: ', font = font_label).grid(row = 0, column = 0)
        
        self.nazov_diety_entry = ttk.Entry(self, font = font_entry)
        self.nazov_diety_entry.grid(row = 0, column = 1)
        
        ttk.Label(self, 
            text = 'Chcete pridať túto potravinu do diety?',
            font = font_label
        ).grid(row = 1, column = 0, columnspan = 2, padx = 10, sticky = 'w')
       
        ttk.Label(self, 
            text = 'Potravina:',
            font = font_label
        ).grid(row = 2, column = 0, padx = 10, sticky = 'w')
        
        self.nazov_potraviny_label = ttk.Label(self, 
            text = 'Nazov potraviny',
            wraplength = 280,
            font = font_nazov_potraviny_label
        )
        self.nazov_potraviny_label.grid(row = 2, column = 1, sticky = 'w')
        
        self.button_ano = ttk.Button(self, text = 'Áno')
        self.button_ano.grid(row = 3, column = 0)
        
        self.button_nie = ttk.Button(self, text = 'Nie')
        self.button_nie.grid(row = 3, column = 1)
        
        self.grab_set()

class OknoPreVytvorenieDiety(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.geometry('400x200')
        self.title('Vytvorenie diety')
        self.resizable(0, 0)
        
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 5)
        self.rowconfigure(2, weight = 1)
        
        font = ('Verdana', 12)
        
        ttk.Label(self, text = 'Vytvorenie diety: ', font = font).grid(row = 0, column = 0, columnspan = 2)
        ttk.Label(self, text = 'Názov diety: ', font = font).grid(row = 1, column = 0)
        
        self.nazov_diety_entry = ttk.Entry(self, font = font)
        self.nazov_diety_entry.grid(row = 1, column = 1)
        
        self.button_uloz = ttk.Button(self, text = 'Ulož')
        self.button_uloz.grid(row = 2, column = 0)
        
        self.button_zrus = ttk.Button(self, text = 'Zruš', command = self.destroy)
        self.button_zrus.grid(row = 2, column = 1)
        
        self.grab_set()
       
class OknoPreCredits(tk.Toplevel):

    def __init__(self, parent):
        super().__init__(parent)
        
        self.geometry('400x200')
        self.title('Credits')
        self.resizable(0, 0)
        
        self.columnconfigure(0, weight = 1)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        self.rowconfigure(2, weight = 1)
        self.rowconfigure(3, weight = 1)
        self.rowconfigure(4, weight = 1)
        
        ttk.Label(self, 
            text = 'Energia ver 1.0.0',
            font = ('Verdana, 12'),
            background = "#ffffff"
        ).grid(row = 1, column = 0, padx = 10, sticky = 'w')
        
        ttk.Label(self, 
            text = 'Autor: Ing. Norbert Jankura, PhD.',
            font = ('Verdana, 12'),
            background = "#ffffff"
        ).grid(row = 2, column = 0, padx = 10, sticky = 'w')
        
        ttk.Label(self, 
            text = 'E-mail: nr.jankura@gmail.com',
            font = ('Verdana, 12'),
            background = "#ffffff"
        ).grid(row = 3, column = 0, padx = 10, sticky = 'w')
        
        self.button_ok = ttk.Button(self, text = 'Ok', command = self.destroy)
        self.button_ok.grid(row = 4, column = 0)
        
        self.grab_set()
        
class OknoPreVyberDiety(tk.Toplevel):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.geometry('900x500')
        
        self.resizable(0, 0)
        
        self.rowconfigure(0, weight = 40)
        self.rowconfigure(1, weight = 40)
        self.rowconfigure(2, weight = 100)
        self.rowconfigure(3, weight = 10)
        
        self.columnconfigure(0, weight = 100)
        self.columnconfigure(1, weight = 1)
        
        self.nadpis = ttk.Label(self,
            font = ('Verdana 14 bold')
        )
        self.nadpis.grid(row = 0, column = 0, columnspan = 2)
        
        self.grab_set()
        
class OknoDialogPotvrdenia(tk.Toplevel):
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.geometry('400x200')
        
        self.title("Potvrdenie")
        
        self.resizable(0, 0)
        self.columnconfigure(0, weight = 1)
        self.columnconfigure(1, weight = 1)
        
        self.rowconfigure(0, weight = 1)
        self.rowconfigure(1, weight = 1)
        
        self.nadpis = ttk.Label(self,
                font = ('Verdana, 12'),
                wraplength = 350,
                background = "#ffffff"
            )
        self.nadpis.grid(row = 0, column = 0, columnspan = 2, padx = 10)
        
        self.button_ano = ttk.Button(self, text = 'Áno')
        self.button_ano.grid(row = 1, column = 0)
        
        self.button_nie = ttk.Button(self, text = 'Nie', command = self.destroy)
        self.button_nie.grid(row = 1, column = 1)
        
        self.grab_set()