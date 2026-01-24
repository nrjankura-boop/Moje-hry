import tkinter as tk
from tkinter import ttk
import Controller
import View
import Model


class Main(tk.Tk):
    
    def __init__(self):
        super().__init__()
        
        self.geometry("1650x800+50+50")
        self.title('Energia')
        self.resizable(0, 0)
        
        self.denna_spotreba_energie = '11700'
        
        view = View.View(self)
        
        model = Model.Model(host = 'localhost', user = 'root', password = 'slniecko', database = 'energia')
        
        controller = Controller.Controller(model ,view)
        
if __name__ == '__main__':
    main = Main()
    main.mainloop()