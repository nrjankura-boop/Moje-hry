import tkinter
import math
import random

class Utvar:

    def __init__(self):
        self.farba = f'#{random.randrange(256**3):06x}'
        self.d = 10
        self.id = []
        self.y = 20
        self.x = 250
        
        self.rotacia = random.randint(0, 3)
        
        self.lava_hranica_x = 100
        self.prava_hranica_x = 400
        
    def zobraz(self, suradnice):
        for x, y in suradnice:
            id = canvas.create_rectangle(x + self.d, 
                                          y + self.d,
                                          x - self.d, 
                                          y - self.d, 
                                          width = 2, 
                                          fill = self.farba)
            self.id.append(id)
    
class Elko(Utvar):
    
    def __init__(self):
        super().__init__()
        
    def vykresli(self):
        if self.rotacia == 0:
            if self.x - 2*self.d < 100:
                self.x += 2*self.d
            if self.x + 2*self.d > 400:
                self.x -= 2*self.d
            if self.y + 2*self.d > 700:
                self.y = 700 - 2*self.d
            self.suradnice = [(self.x - 2*self.d, self.y), (self.x, self.y), 
                                (self.x + 2*self.d, self.y), (self.x - 2*self.d, 
                                self.y + 2*self.d)]
            
            self.hranica_min_x = 2*self.d
            self.hranica_max_x = 2*self.d
            self.hranica_max_y = 2*self.d
        elif self.rotacia == 1:
            if self.x + 2*self.d < 100:
                self.x -= 2*self.d
            if self.y > 700:
                self.y = 700
            self.suradnice = [(self.x, self.y - 2*self.d),(self.x, self.y - 4*self.d),
                                (self.x, self.y), (self.x + 2*self.d, self.y)]
            
            self.hranica_min_x = 0
            self.hranica_max_x = 2*self.d
            self.hranica_max_y = 0
        elif self.rotacia == 2:
            if self.x - 2*self.d < 100:
                self.x += 2*self.d
            if self.x + 2*self.d > 400:
                self.x -= 2*self.d
            if self.y + 2*self.d > 700:
                self.y = 700 - 2*self.d
            self.suradnice = [(self.x - 2*self.d, self.y),(self.x + 2*self.d, self.y),
                                (self.x, self.y), (self.x + 2*self.d, self.y + 2*self.d)]
                                
            self.hranica_min_x = 2*self.d
            self.hranica_max_x = 2*self.d
            self.hranica_max_y = 2*self.d                  
        elif self.rotacia == 3:
            if self.x - 2*self.d < 100:
                self.x += 2*self.d
            if self.y + 2*self.d > 700:
                self.y = 700 - 2*self.d
            self.suradnice = [(self.x, self.y - 2*self.d),(self.x, self.y + 2*self.d),
                                (self.x, self.y), (self.x - 2*self.d, self.y - 2*self.d)]
            
            self.hranica_min_x = 2*self.d
            self.hranica_max_x = 0
            self.hranica_max_y = 2*self.d  
            
        super().zobraz(self.suradnice)
        
            
class Sliz(Utvar):
    
    def __init__(self): 
        super().__init__()
    
    def vykresli(self):
        if self.rotacia == 0 or self.rotacia == 2:
            if self.x - 2*self.d < 100:
                self.x += 2*self.d
            if self.x + 2*self.d > 400:
                self.x -= 2*self.d
            if self.y  > 700:
                self.y = 700 
            self.suradnice = [(self.x - 2*self.d, self.y), (self.x, self.y), 
                            (self.x + 2*self.d, self.y)]
            
            self.hranica_min_x = 2*self.d
            self.hranica_max_x = 2*self.d
            self.hranica_max_y = 0 
            
        elif self.rotacia == 1 or self.rotacia == 3:
            if self.y + 2*self.d > 700:
                self.y = 700 - 2*self.d
            self.suradnice = [(self.x, self.y + 2*self.d), (self.x, self.y), 
                            (self.x, self.y - 2*self.d)]
                            
            self.hranica_min_x = 0
            self.hranica_max_x = 0
            self.hranica_max_y = 2*self.d
            
        super().zobraz(self.suradnice)


class Plusko(Utvar):

    def __init__(self):
        super().__init__()
        
    def vykresli(self):
        self.suradnice = [(self.x - 2*self.d, self.y), (self.x, self.y), 
                            (self.x + 2*self.d, self.y),
                            (self.x, self.y-2 * self.d),
                            (self.x, self.y + 2 * self.d)]
                            
        self.hranica_min_x = 2*self.d
        self.hranica_max_x = 2*self.d
        self.hranica_max_y = 2*self.d
        
        super().zobraz(self.suradnice)
        
class Trojuholnik(Utvar):

    def __init__(self):
        super().__init__()
        
    def vykresli(self):
        if self.rotacia == 0:
            if self.x - 2*self.d < 100:
                self.x += 2*self.d
            if self.x + 2*self.d > 400:
                self.x -= 2*self.d
            
            if self.x == self.prava_hranica_x:
                self.x += 2*self.d
                
            if self.x == self.lava_hranica_x:
                self.x -= 2*self.d
                
            if self.y > 700:
                self.y = 700 
            
            self.suradnice = [(self.x - 2*self.d, self.y), (self.x, self.y), 
                                (self.x + 2*self.d, self.y),
                                (self.x, self.y - 2 * self.d)]
                                
            self.hranica_min_x = 2*self.d
            self.hranica_max_x = 2*self.d
            self.hranica_max_y = 0                    
                                
        elif self.rotacia == 1:
            if self.x - 2*self.d < 100:
                self.x += 2*self.d
            
            if self.y + 2*self.d > 700:
                self.y = 700 - 2*self.d
                
            if self.x == self.prava_hranica_x:
                self.x += 2*self.d
                
            if self.x == self.lava_hranica_x:
                self.x -= 2*self.d 
                
            self.suradnice = [(self.x - 2*self.d, self.y), (self.x, self.y), 
                                (self.x, self.y + 2*self.d),
                                (self.x, self.y - 2*self.d)]
                                
            self.hranica_min_x = 2*self.d 
            self.hranica_max_x = 0
            self.hranica_max_y = 2*self.d                    
                                
        elif self.rotacia == 2:
            if self.x - 2*self.d < 100:
                self.x += 2*self.d
            if self.x + 2*self.d > 400:
                self.x -= 2*self.d
            
            if self.x == self.prava_hranica_x:
                self.x += 2*self.d
                
            if self.x == self.lava_hranica_x:
                self.x -= 2*self.d
            
            if self.y + 2*self.d > 700:
                self.y = 700 - 2*self.d
                
            self.suradnice = [(self.x - 2*self.d, self.y), (self.x, self.y), 
                                (self.x + 2*self.d, self.y),
                                (self.x, self.y + 2*self.d)]
                                
            self.hranica_min_x = 2*self.d 
            self.hranica_max_x = 2*self.d 
            self.hranica_max_y = 2*self.d                     
                                
        elif self.rotacia == 3:
            if self.x + 2*self.d > 400:
                self.x -= 2*self.d
                
            if self.x == self.prava_hranica_x:
                self.x += 2*self.d
                
            if self.x == self.lava_hranica_x:
                self.x -= 2*self.d
            
            if self.y + 2*self.d > 700:
                self.y = 700 - 2*self.d
                
            self.suradnice = [(self.x + 2*self.d, self.y), (self.x, self.y), 
                                (self.x, self.y + 2*self.d),
                                (self.x, self.y - 2*self.d)]
                                
            self.hranica_min_x = 0
            self.hranica_max_x = 2*self.d 
            self.hranica_max_y = 2*self.d
            
        super().zobraz(self.suradnice)
        
class Tetris:
    
    def __init__(self):
        canvas.create_line(100, 0, 100, 710, width=4)
        canvas.create_line(400, 0, 400, 710, width=4)
        canvas.create_line(100, 710, 400, 710, width=4)
        
        self.plochy_idcka = []
        
        self.idem_dolava = False
        self.idem_doprava = False
        
        self.lava_hranica_x = False
        self.prava_hranica_x = False
        self.hranica_y = False
        self.hranica_y_hod = 700
        
        #self.utvar = [Elko, Sliz, Plusko, Trojuholnik] 
        self.utvar = [Trojuholnik] 
        self.entita = random.choice(self.utvar)()
        
        canvas.bind_all('<Left>', self.dolava)
        canvas.bind_all('<Right>', self.doprava)
        canvas.bind_all('<Down>', self.dole)
        canvas.bind_all('<Up>', self.rotuj)
        
        self.pohyb()
        
    def pohyb(self):
        if not self.idem_dolava or not self.idem_doprava:
            self.entita.y += 20
        
        if self.idem_dolava:
            if hasattr(self.entita, 'hranica_min_x'):
                if (self.entita.x - self.entita.hranica_min_x - 20 > 100 and 
                    not self.lava_hranica_x):
                    self.entita.x -= 20
            self.idem_dolava = False
            
        if self.idem_doprava:
            if hasattr(self.entita, 'hranica_max_x'):
                if (self.entita.x + self.entita.hranica_max_x + 20 < 400 and
                    not self.prava_hranica_x):
                    self.entita.x += 20
            self.idem_doprava = False
            
        self.kresli_entitu() 
         
        self.nastav_hranice()
        
        if self.entita.y + self.entita.hranica_max_y == 700 or self.hranica_y:
            for id in self.entita.id:
                self.plochy_idcka.append(id)
            
            self.skontroluj_a_zmaz_rady()
            
            self.entita = random.choice(self.utvar)()
        if self.hranica_y_hod > 50:
            job = canvas.after(250, self.pohyb)
            return job
        else:
            canvas.unbind_all('<Left>')
            canvas.unbind_all('<Right>')
            canvas.unbind_all('<Down>')
            canvas.unbind_all('<Up>')
    
    def skontroluj_a_zmaz_rady(self):
        rad_sa_zmazal = 0
        id_y = self.vrat_id_y()
        
        idcka_na_zmazanie = []
        sur_y_zmazanych = [0]
        for ypsilon, pole_id in id_y.items():
            if len(pole_id) == 15:
                for id in pole_id:
                    canvas.delete(id)
                    idcka_na_zmazanie.append(id)
                    sur_y_zmazanych.append(ypsilon)
                rad_sa_zmazal += 1
                
        max_y_zmazanych = max(sur_y_zmazanych)
        
        if rad_sa_zmazal:        
            for id in idcka_na_zmazanie:
                self.plochy_idcka.remove(id)
            
            id_y = self.vrat_id_y()
            for _ in range(rad_sa_zmazal):
                for ypsilon, pole_id in id_y.items():
                    if ypsilon < max_y_zmazanych:
                        for id in pole_id:
                            canvas.move(id, 0, 2*self.entita.d)
        
    def vrat_id_y(self):
        id_y = {}
        for id in self.plochy_idcka:
            p_x1, p_y1, p_x2, p_y2 = canvas.coords(id)
            x = int(p_x1 + (p_x2 - p_x1)/2)
            y = int(p_y1 + (p_y2 - p_y1)/2)
            if y in id_y:
                id_y[y].append(id)
            else:
                id_y[y] = [id]
        return id_y
    
    def kresli_entitu(self):
        idcka = []
        for element in self.entita.id:
            canvas.delete(element)
            idcka.append(element)
            
        for element in idcka:
            self.entita.id.remove(element)
            
        self.entita.vykresli()
    
    def nastav_hranice(self):
        entita_coords = []
        plocha_coords = []
        
        self.lava_hranica_x = False
        self.prava_hranica_x = False
        self.hranica_y = False
        
        for id in self.entita.id:
            e_x1, e_y1, e_x2, e_y2 = canvas.coords(id)
            x = int(e_x1 + (e_x2 - e_x1)/2)
            y = int(e_y1 + (e_y2 - e_y1)/2)
            entita_coords.append((x, y))
            
        for id in self.plochy_idcka:
            p_x1, p_y1, p_x2, p_y2 = canvas.coords(id)
            x = int(p_x1 + (p_x2 - p_x1)/2)
            y = int(p_y1 + (p_y2 - p_y1)/2)
            plocha_coords.append((x, y))
        
        for ex, ey in entita_coords:
            for px, py in plocha_coords:
                if ex == px:
                    if ey + 2*self.entita.d == py:
                        self.hranica_y = True
                        self.hranica_y_hod = py
                self.entita.lava_hranica_x = 400
                self.entita.prava_hranica_x = 100                
                if ey == py:
                    if ex - 2*self.entita.d == px:
                        self.lava_hranica_x = True
                        self.entita.lava_hranica_x = min(px, self.entita.lava_hranica_x)
                    if ex + 2*self.entita.d == px:
                        self.prava_hranica_x = True
                        self.entita.prava_hranica_x = max(px, self.entita.prava_hranica_x)
   
    def dolava(self, event):
        self.idem_dolava = True
        self.entita.y -= 20
        try:
            job = self.pohyb()
            canvas.after_cancel(job)
        except ValueError:
            pass
   
    def doprava(self, event):
        self.idem_doprava = True
        self.entita.y -= 20
        try:
            job = self.pohyb()
            canvas.after_cancel(job)
        except ValueError:
            pass
    
    def dole(self, event):
        try:
            job = self.pohyb()
            canvas.after_cancel(job)
        except ValueError:
            pass

    def rotuj(self, event):
        self.entita.rotacia = (self.entita.rotacia + 1) % 4
        
        
win = tkinter.Tk()
canvas = tkinter.Canvas(width=500, height=800)
canvas.pack()

Tetris()

tkinter.mainloop()        