import tkinter
import math
import random

class Utvar:

    def __init__(self):
        #self.farba = f'#{random.randrange(256**3):06x}'
        red = random.randint(0, 200)
        green = random.randint(0, 200)
        blue = random.randint(0, 200)
        self.farba = f'#{red:02x}{green:02x}{blue:02x}'
        self._suradnice = []
        
class Elko(Utvar):
    
    def __init__(self):
        super().__init__()
        self.max_rotacii = 4
        
    def suradnice(self, rotacia=5):    
        self._suradnice.append([(0, 0), (-1, -1), (0, -1), (0, 1)])
        self._suradnice.append([(0, 0), (-1, 0), (1, -1), (1, 0)])
        self._suradnice.append([(0, 0), (0, -1), (0, 1), (1, 1)])
        self._suradnice.append([(0, 0), (-1, 0), (-1, 1), (1, 0)])
        
        nahodna_rotacia = random.randint(0, self.max_rotacii - 1)
        
        if rotacia == 5: return self._suradnice[nahodna_rotacia], nahodna_rotacia 
        else: return self._suradnice[rotacia]

class Elko2(Utvar):
    
    def __init__(self):
        super().__init__()
        self.max_rotacii = 4
        
    def suradnice(self, rotacia=5):    
        self._suradnice.append([(0, 0), (0, -1), (0, 1), (1, -1)])
        self._suradnice.append([(0, 0), (-1, 0), (1, 0), (1, 1)])
        self._suradnice.append([(0, 0), (-1, 1), (0, -1), (0, 1)])
        self._suradnice.append([(0, 0), (-1, -1), (-1, 0), (1, 0)])
        
        nahodna_rotacia = random.randint(0, self.max_rotacii - 1)
        
        if rotacia == 5: return self._suradnice[nahodna_rotacia], nahodna_rotacia 
        else: return self._suradnice[rotacia]
       
class Sliz(Utvar):
    
    def __init__(self): 
        super().__init__()
        self.max_rotacii = 2
        
    def suradnice(self, rotacia = 5):    
        self._suradnice.append([(0, 0), (0, -1), (0, 1)])
        self._suradnice.append([(0, 0), (-1, 0), (1, 0)])
        
        nahodna_rotacia = random.randint(0, self.max_rotacii - 1)
        
        if rotacia == 5: return self._suradnice[nahodna_rotacia], nahodna_rotacia 
        else: return self._suradnice[rotacia]
        
class Plusko(Utvar):

    def __init__(self):
        super().__init__()
        self.max_rotacii = 1
        
    def suradnice(self, rotacia=5):    
        self._suradnice.append([(0, 0), (1, -1), (1, 0), (1, 1), (2, 0)])
        
        if rotacia == 5: return self._suradnice[0], 0 
        else: return self._suradnice[0]
    
class Trojuholnik(Utvar):

    def __init__(self):
        super().__init__()
        self.max_rotacii = 4
        
    def suradnice(self, rotacia=5):    
        self._suradnice.append([(0, 0), (-1, 0), (0, -1), (0, 1)])
        self._suradnice.append([(0, 0), (-1, 0), (0, -1), (1, 0)])
        self._suradnice.append([(0, 0), (0, -1), (0, 1), (1, 0)])
        self._suradnice.append([(0, 0), (-1, 0), (0, 1), (1, 0)])
        
        nahodna_rotacia = random.randint(0, self.max_rotacii - 1)
        
        if rotacia == 5: return self._suradnice[nahodna_rotacia], nahodna_rotacia 
        else: return self._suradnice[rotacia]

class Esko(Utvar):

    def __init__(self):
        super().__init__()
        self.max_rotacii = 4
        
    def suradnice(self, rotacia=5):    
        self._suradnice.append([(0, 0), (-1, -1), (0, -1), (1, 0)])
        self._suradnice.append([(0, 0), (0, 1), (1, -1), (1, 0)])
        self._suradnice.append([(0, 0), (-1, 0), (0, 1), (1, 1)])
        self._suradnice.append([(0, 0), (-1, 0), (-1, 1), (0, -1)])
        
        nahodna_rotacia = random.randint(0, self.max_rotacii - 1)
        
        if rotacia == 5: return self._suradnice[nahodna_rotacia], nahodna_rotacia 
        else: return self._suradnice[rotacia]

class Esko2(Utvar):

    def __init__(self):
        super().__init__()
        self.max_rotacii = 4
        
    def suradnice(self, rotacia=5):    
        self._suradnice.append([(0, 0), (-1, 0), (0, -1), (1, -1)])
        self._suradnice.append([(0, 0), (0, -1), (1, 0), (1, 1)])
        self._suradnice.append([(0, 0), (-1, 1), (0, 1), (1, 0)])
        self._suradnice.append([(0, 0), (-1, -1), (-1, 0), (0, 1)])
        
        nahodna_rotacia = random.randint(0, self.max_rotacii - 1)
        
        if rotacia == 5: return self._suradnice[nahodna_rotacia], nahodna_rotacia 
        else: return self._suradnice[rotacia]
        
class Tetris:
    
    def __init__(self):
        
        self.test = False # sluzi pre ucely testovania
        
        self.d = 20 # velkost stvorceka utvaru na ploche
        
        self.x0, self.y0 = 50, 100 # suradnice pociatku plochy
        
        self.pocet_r, self.pocet_s = 30, 15 # maximalny pocet stlpcov a riadkov
        
        self.min_rychlost = 500 # rychlost klesania utvarov
        
        self.max_rychlost = 50 # rychlost klesania utvarov ak stlacim sipku dole
        
        self.score = 0 # pociatocne skore
        
        self.prekazky = {}
        self.entita_idcka = []
        self.nasledovna_entita_idcka = []
        self.entita = None
        self.prva_inicializacia = True
        self.koniec = False
        
        self.rychlost = self.min_rychlost
        
        if self.pocet_s % 2 == 0:
            self.stred_s = self.pocet_s / 2 - 1
        else:
            self.stred_s = self.pocet_s // 2
        
        canvas.create_rectangle(self.x0, self.y0, self.x0 + self.pocet_s * self.d, self.y0 + self.pocet_r * self.d, width=4) 
        
        canvas.bind_all('<KeyPress-Down>', self.zrychli)
        canvas.bind_all('<KeyRelease-Down>', self.spomal)
        canvas.bind_all('<Left>', self.dolava)
        canvas.bind_all('<Right>', self.doprava)
        canvas.bind_all('<Up>', self.rotuj)
        
        self.vypis_score_a_copy()
        self.pohyb()
        
    ##########################################################
    ############### Vytvorenie noveho utvaru #################
    ############### a zaroven vytvorenie     #################
    ############### nasledovneho utvaru      #################
    ##########################################################
    
    def init_entity(self):
        self.utvar = [Elko, Elko2, Sliz, Plusko, Trojuholnik, Esko, Esko2] 
        #self.entita = random.choice(self.utvar)()
        if self.test:
            self.entita = Sliz()
            suradnice, self.rotacia = self.entita.suradnice()
        else:
            if self.prva_inicializacia:
                self.entita = random.choice(self.utvar)()
                self.nasledovna_entita = random.choice(self.utvar)()
                suradnice, self.rotacia = self.entita.suradnice()
                self.prva_inicializacia = False
            else:
                self.entita = self.nasledovna_entita
                self.nasledovna_entita = random.choice(self.utvar)()
                suradnice, self.rotacia = self.suradnice_nasledovnej_entity[:], self.rotacia_nasledovnej_entity
                
            self.zobraz_nasledovnu_entitu()
            
        self.suradnice_entity = []
        
        for r, s in suradnice:
            if r < 0:
                posun = 1
                break
            else:
                posun = 0
                
        for r, s in suradnice:        
            self.suradnice_entity.append((r + posun, s + self.stred_s))
    
    ############### Koniec Vytvorenie noveho utvaru #################
    
    ##########################################################
    ########### Automaticky pohyb utvaru nadol ###############
    ##########################################################
    
    def pohyb(self):
        if self.entita is None: 
            self.init_entity()       
            self.vykresli()
            self.boli_plne_riadky = False
            self.zmaz_plne_riadky()
        self.vykresli()
        self.nadol()
        if not self.koniec: canvas.after(self.rychlost, self.pohyb)
        
    def zrychli(self, arg):
        self.rychlost = self.max_rychlost
        
    def spomal(self, arg):
        self.rychlost = self.min_rychlost 
    
    ########### Koniec Automaticky pohyb utvaru nadol ###############
    
    ##########################################################
    ################## Vykresli utvar ########################
    ##########################################################
    
    def vykresli(self):
        self.zmaz()
        for r, s in self.suradnice_entity:
            x1 = self.x0 + s*self.d
            x2 = x1 + self.d
            y1 = self.y0 + r*self.d
            y2 = y1 + self.d
            self.entita_idcka.append(canvas.create_rectangle(x1, y1, x2, y2, fill=self.entita.farba))
    
    def zmaz(self):
        for id in self.entita_idcka:
            canvas.delete(id)
        self.entita_idcka = []
    
    ################## Koniec Vykresli utvar ########################
    
    ##########################################################
    ################## Posun utvar nadol #####################
    ##########################################################
    
    def nadol(self):
        if not self.koniec_entity():
            for i, (r, s) in enumerate(self.suradnice_entity.copy()):
                self.suradnice_entity[i] = (r+1, s)
        else:
            self.entita_idcka = []
            self.zaznamenaj_prekazky()
            self.entita = None
            self.zisti_ci_je_koniec()
    
    # kontrola ci je utvar mozne este posunut nadol
    # koniec posunu utvaru nadol
    def koniec_entity(self):
        koniec = False
        for r, s in self.suradnice_entity:
            if r+1 > self.pocet_r - 1: 
                koniec = True
                break
            if (r+1, s) in self.prekazky:
                koniec = True
                break
        
        return koniec
    
    ################## Posun utvar nadol #####################
    
    ##########################################################
    ################## Posun utvar dolava ####################
    ##########################################################
    
    def dolava(self, arg):
        if not self.lava_hranica():
            for i, (r, s) in enumerate(self.suradnice_entity.copy()):
                self.suradnice_entity[i] = (r, s-1)
    
    def lava_hranica(self):
        stop = False
        for r, s in self.suradnice_entity:
            if s-1 < 0:
                stop = True
                break
            if (r, s-1) in self.prekazky:
                stop = True
                break
        
        return stop
    
    ################## Koniec Posun utvar dolava ####################
    
    ##########################################################
    ################## Posun utvar doprava ###################
    ##########################################################
    
    def doprava(self, arg):
        if not self.prava_hranica():
            for i, (r, s) in enumerate(self.suradnice_entity.copy()):
                self.suradnice_entity[i] = (r, s+1)
    
    def prava_hranica(self):
        stop = False
        for r, s in self.suradnice_entity:
            if s+1 > self.pocet_s - 1:
                stop = True
                break
            if (r, s+1) in self.prekazky:
                stop = True
                break
        
        return stop
    
    ################## Koniec Posun utvar doprava ###################
    
    ##########################################################
    ##################### Rotacia utvaru #####################
    ##########################################################
    
    def rotuj(self, arg):
        if self.entita is not None:
            self.rotacia += 1
            suradnice = self.entita.suradnice(self.rotacia % self.entita.max_rotacii)
            if not self.stop_rotacia(suradnice):
                for i, (r, s) in enumerate(suradnice):
                    self.suradnice_entity[i] = (self.suradnice_entity[0][0] + r, self.suradnice_entity[0][1] + s)
            self.vykresli()
        
    def stop_rotacia(self, suradnice):
        stop = False
        for i, (r, s) in enumerate(suradnice):
            if  (self.suradnice_entity[0][0] + r, self.suradnice_entity[0][1] + s) in self.prekazky:
                stop = True
                break
            if  self.suradnice_entity[0][0] + r > self.pocet_r - 1:
                stop = True
                break
            if self.suradnice_entity[0][1] + s < 0 or self.suradnice_entity[0][1] + s > self.pocet_s - 1:
                stop = True
                break
        
        return stop
    
    ##################### Koniec Rotacia utvaru #####################
    
    ##########################################################
    ############## Zaznamena prekazky na ploche ##############
    ##########################################################
    
    def zaznamenaj_prekazky(self):
        for (r, s) in self.suradnice_entity:
            self.prekazky[(r, s)] = self.entita.farba
        
    ############## Koniec Zaznamena prekazky na ploche ##############
    
    ##########################################################
    ################### Zmazanie plnych riadkov ##############
    ##########################################################
    
    def zmaz_plne_riadky(self):
        plne_riadky = self.vrat_plne_riadky()
        if len(plne_riadky) > 0:
            self.boli_plne_riadky = True
            plne_riadky.sort(reverse=True)
            r = plne_riadky[0]
            for (rp, sp) in self.prekazky.copy():
                if r == rp:
                    self.prekazky.pop((rp, sp))
            
            canvas.after(500, self.prekresli_prekazky())
            
            self.posun_prekazky_nadol(r)
            
            self.score += 20
            
            canvas.after(200, self.zmaz_plne_riadky)
            
        else:
            if self.boli_plne_riadky:
                canvas.after(500, self.prekresli_prekazky())
                self.boli_plne_riadky = False
            
            
    def posun_prekazky_nadol(self, zmazany_riadok):
        for (rp, sp), farba in reversed(sorted(self.prekazky.copy().items())):
            if rp < zmazany_riadok:
                self.prekazky[(rp + 1), sp] = farba
                self.prekazky.pop((rp, sp))
    
    def prekresli_prekazky(self):
        canvas.delete('all')
        self.nakresli_novu_plochu()
    
    def vrat_plne_riadky(self):
        pocet_obsadenych_v_riadku = {}
        for r, s in self.prekazky:
            if r not in pocet_obsadenych_v_riadku:
                pocet_obsadenych_v_riadku[r] = 1
            else:    
                pocet_obsadenych_v_riadku[r] += 1
        
        obsadene_riadky = []
        for riadok, pocet in pocet_obsadenych_v_riadku.items():
            if pocet == self.pocet_s:
                obsadene_riadky.append(riadok)
        
        return obsadene_riadky
    
    def nakresli_novu_plochu(self):
        canvas.create_rectangle(self.x0, self.y0, self.x0 + self.pocet_s * self.d, self.y0 + self.pocet_r * self.d, width=4)
        for (r, s), farba in self.prekazky.items():
            x1 = self.x0 + s*self.d
            x2 = x1 + self.d
            y1 = self.y0 + r*self.d
            y2 = y1 + self.d
            canvas.create_rectangle(x1, y1, x2, y2, fill=farba)
        self.vypis_score_a_copy()
        if not self.test:
            self.vykresli_nasledovnu_entitu()
        
    ################### Koniec Zmazanie plnych riadkov ##############   
    
    ##########################################################
    ############# Zobrazenie nasledovneho utvaru #############
    ##########################################################
    
    def zobraz_nasledovnu_entitu(self):
        self.suradnice_nasledovnej_entity, self.rotacia_nasledovnej_entity = self.nasledovna_entita.suradnice()
        self.zmaz_nasledovnu_entitu()
        self.vykresli_nasledovnu_entitu()
        
    def vykresli_nasledovnu_entitu(self):
        x0 = self.x0 + self.pocet_s * self.d + 50
        y0 = self.y0 + self.d
        suradnice = self.suradnice_nasledovnej_entity[:]
        
        for r, s in suradnice:
            if r == -1:
                posun = 0
                break
            else:
                posun = 1
                
        for i, (r, s) in enumerate(suradnice.copy()):        
            suradnice[i] = (r - posun, s)
        
        for r, s in suradnice:
            x1 = x0 + s*self.d
            x2 = x1 + self.d
            y1 = y0 + r*self.d
            y2 = y1 + self.d
            self.nasledovna_entita_idcka.append(canvas.create_rectangle(x1, y1, x2, y2, fill=self.nasledovna_entita.farba))
    
    def zmaz_nasledovnu_entitu(self):
        for id in self.nasledovna_entita_idcka:
            canvas.delete(id)
        self.nasledovna_entita_idcka = []
        
    ############# Koniec Zobrazenie nasledovneho utvaru #############
    
    ##########################################################
    ############# Kontrola ci tetris skoncil #################
    ##########################################################
    
    def zisti_ci_je_koniec(self):
        prvy_riadok = []
        for s in range(0, self.pocet_s):
            prvy_riadok.append((0, s))
        
        for stvorec in prvy_riadok:
            if stvorec in self.prekazky:
                self.koniec = True
    
    ############# Koniec Kontrola ci tetris skoncil #################
    
    ##########################################################
    ############# Vypise score na obrazovku ##################
    ##########################################################
    
    def vypis_score_a_copy(self):
        try:
            canvas.delete(self.id_score)
            canvas.delete(self.id_copy)
        except AttributeError:
            pass
        x = self.x0 + (self.pocet_s * self.d) // 2    
        self.id_score = canvas.create_text(x, 50, text=str(self.score), font='Arial 40')
        self.id_copy = canvas.create_text(x, self.y0 + self.pocet_r * self.d + 25, text="© Norbert Jankura, nr.jankura@gmail.com", font="Arial 15")
    
    ############# Koniec Vypise score na obrazovku ##################
    
    
    
    
win = tkinter.Tk()
canvas = tkinter.Canvas(width=650, height=750)
canvas.pack()

Tetris()

tkinter.mainloop()        