import tkinter
from tkinter import ttk
from tkinter import filedialog as fd

import os

import math
from pprint import pprint
from PIL import Image, ImageTk

class Figurka:

    def __init__(self, pozicia, farba, id_obrazka):
        self.pozicia = pozicia
        self.farba = farba # 0 - biely, 1 - cierny
        self.id_obrazka = id_obrazka
        self.faza_animacie = 0
        
    def mozne_tahy(self, obsadene_polia):
        mozne_pozicie = set()
        
        # urcenie riadka nasledovneho mozneho tahu
        if self.farba == 0: #biely
            riadok = self.pozicia[0] - 1
        else: # cierny
            riadok = self.pozicia[0] + 1
            
        # urcenie stlpca nasledovneho mozneho tahu
        stlpec1 = self.pozicia[1] - 1
        stlpec2 = self.pozicia[1] + 1
        if 0 <= riadok <= 7:
            if stlpec1 >= 0:
                mozne_pozicie.add((riadok, stlpec1))
            if stlpec2 <= 7:
                mozne_pozicie.add((riadok, stlpec2))
                
        preskakovane_figurky = []
        for ri, st in obsadene_polia:
            # ak je v moznych poziciach obsadena pozicia, odstran ju z moznych pozicii
            if (ri, st) in mozne_pozicie:
                mozne_pozicie = mozne_pozicie - {(ri, st)}  
                
                # ak objekt na obsadenom poli je figurka odlisnej farby ako ma tahana figurka
                # (tahana figurka je tento objekt teda self.)
                # tak je mozne ze budeme preskakovat cudziu figurku
                # a pridame mozny tah pre preskok cudzej figurky
                if obsadene_polia[(ri, st)].farba != self.farba:
                    if self.farba == 0: # biele
                        # nasledovny riadok nesmie vypadnut zo sachovnice
                        if ri - 1 >= 0:
                            # pozicia stlpca tahanej figurky + 1 sa rovna obsadenemu stlpcu
                            # a tento stlpec + 1 nesmie vypadnut zo sachovnice 
                            # pridanie ri +- 1 a st +- 1 do moznych pozicii (tahov)
                            # pridanie preskakovanej figurky do zoznamu preskakovane_figurky
                            if self.pozicia[1] + 1 == st and st + 1 <= 7:
                                # pokial policko na ktore sa skace nie je obsadene pridaj ho 
                                # do moznych tahov
                                if (ri - 1, st + 1) not in obsadene_polia: 
                                    mozne_pozicie.add((ri-1, st+1))
                                    preskakovane_figurky.append(obsadene_polia[(ri, st)])
                            elif self.pozicia[1] - 1 == st  and st - 1 >= 0:
                                if (ri - 1, st - 1) not in obsadene_polia:
                                    mozne_pozicie.add((ri-1, st-1))
                                    preskakovane_figurky.append(obsadene_polia[(ri, st)])
                    else: # cierne
                        # pozri o poschodie vyssie pre biele figurky
                        if ri + 1 <= 7:
                            if self.pozicia[1] + 1 == st and st + 1 <= 7:
                                if (ri + 1, st + 1) not in obsadene_polia:
                                    mozne_pozicie.add((ri+1, st+1))
                                    preskakovane_figurky.append(obsadene_polia[(ri, st)])
                            elif self.pozicia[1] - 1 == st  and st - 1 >= 0:
                                if (ri + 1, st - 1) not in obsadene_polia:
                                    mozne_pozicie.add((ri+1, st-1))
                                    preskakovane_figurky.append(obsadene_polia[(ri, st)])
                            
        return mozne_pozicie, preskakovane_figurky
    
    def je_mozne_skakat(self, obsadene_polia):
        if self.farba == 0: # biely
            # pozicie doskakovaneho pola
            riadok = self.pozicia[0] - 2
            stlpec1 = self.pozicia[1] - 2
            stlpec2 = self.pozicia[1] + 2
            if riadok >= 0:
                if stlpec1 >= 0:
                    # key je suradnica preskakovaneho policka
                    # zistujeme ci je na nom superova figurka
                    key = (self.pozicia[0]-1, self.pozicia[1]-1)
                    #print(f'key {key}')
                    #pprint(obsadene_polia)
                    if ((riadok, stlpec1) not in obsadene_polia and 
                        key in obsadene_polia and
                        obsadene_polia[key].farba == 1):
                        return True
                if stlpec2 <= 7:
                    key = (self.pozicia[0]-1, self.pozicia[1]+1)
                    #print(f'key {key}')
                    #pprint(obsadene_polia)
                    if ((riadok, stlpec2) not in obsadene_polia and
                        key in obsadene_polia and
                        obsadene_polia[key].farba == 1):
                        return True
        else:# cierny
            riadok = self.pozicia[0] + 2
            stlpec1 = self.pozicia[1] - 2
            stlpec2 = self.pozicia[1] + 2
            if riadok <= 7:
                if stlpec1 >= 0:
                    key = (self.pozicia[0]+1, self.pozicia[1]-1)
                    #print(f'key {key}')
                    #pprint(f'figurka ktora sa posudzuje riadok, stlpec: {self.pozicia[0]}, {self.pozicia[1]}')
                    #pprint(f'preskakovana figurka riadok stlpec: {key}')
                    #pprint(f'doskakovane pole riadok, stlpec1: {riadok}, {stlpec1}')
                    #print()
                    #pprint(f'obsadene_polia: {obsadene_polia}')
                    #print()
                    if ((riadok, stlpec1) not in obsadene_polia and
                        key in obsadene_polia and
                        obsadene_polia[key].farba == 0):
                        #print(f'je skokan  {self.pozicia[0]}, {self.pozicia[1]}')
                        return True
                if stlpec2 <= 7:
                    key = (self.pozicia[0]+1, self.pozicia[1]+1)
                    #print(f'key {key}')
                    #pprint(f'figurka riadok, stlpec: {self.pozicia[0]}, {self.pozicia[1]}')
                    #pprint(f'doskakovane pole riadok, stlpec2: {riadok}, {stlpec2}')
                    #pprint(f'obsadene_polia: {obsadene_polia}')
                    if ((riadok, stlpec2) not in obsadene_polia and
                        key in obsadene_polia and
                        obsadene_polia[key].farba == 0):
                        #print(f'je skokan  {self.pozicia[0]}, {self.pozicia[1]}')
                        return True
        return False
        
class Pesiak(Figurka):
    
    def __init__(self, pozicia, farba, id_obrazka):
        super().__init__(pozicia, farba, id_obrazka)
        
class Dama(Figurka):
            
    def __init__(self, pozicia, farba, id_obrazka):
        super().__init__(pozicia, farba, id_obrazka)
    
    # prepisana metoda pre damu
    def mozne_tahy(self, obsadene_polia):
        mozne_pozicie, preskakovane_figurky = super().mozne_tahy(obsadene_polia)
       
        # urcenie riadka nasledovneho mozneho tahu vzad pre damu
        if self.farba == 0: #biely
            riadok = self.pozicia[0] + 1
        else: # cierne
            riadok = self.pozicia[0] - 1
            
        # urcenie stlpca nasledovneho mozneho tahu vzad pre damu
        stlpec1 = self.pozicia[1] - 1
        stlpec2 = self.pozicia[1] + 1
        if 0 <= riadok <= 7:
            if stlpec1 >= 0:
                mozne_pozicie.add((riadok, stlpec1))
            if stlpec2 <= 7:
                mozne_pozicie.add((riadok, stlpec2))
        
        for ri, st in obsadene_polia:
            # ak je v moznych poziciach obsadena pozicia, odstran ju z moznych pozicii
            if (ri, st) in mozne_pozicie:
                mozne_pozicie = mozne_pozicie - {(ri, st)}  
                
                # ak objekt na obsadenom poli je figurka odlisnej farby ako ma tahana figurka
                # (tahana figurka je tento objekt teda self.)
                # tak je mozne ze budeme preskakovat cudziu figurku
                # a pridame mozny tah pre preskok cudzej figurky
                if obsadene_polia[(ri, st)].farba != self.farba:
                    if self.farba == 0: # biele
                        # nasledovny riadok nesmie vypadnut zo sachovnice
                        if ri + 1 <= 7:                            
                            # pozicia stlpca tahanej figurky + 1 sa rovna obsadenemu stlpcu
                            # a tento stlpec + 1 nesmie vypadnut zo sachovnice 
                            # pridanie ri +- 1 a st +- 1 do moznych pozicii (tahov)
                            # pridanie preskakovanej figurky do zoznamu preskakovane_figurky
                            if self.pozicia[1] + 1 == st and st + 1 <= 7:
                                # pokial policko na ktore sa skace nie je obsadene pridaj ho 
                                # do moznych tahov
                                if (ri + 1, st + 1) not in obsadene_polia: 
                                    mozne_pozicie.add((ri+1, st+1))
                                    preskakovane_figurky.append(obsadene_polia[(ri, st)])
                            elif self.pozicia[1] - 1 == st  and st - 1 >= 0:
                                if (ri + 1, st - 1) not in obsadene_polia:
                                    mozne_pozicie.add((ri+1, st-1))
                                    preskakovane_figurky.append(obsadene_polia[(ri, st)])
                    else: # cierne
                        # pozri o poschodie vyssie pre biele figurky
                        if ri - 1 >= 0:
                            if self.pozicia[1] + 1 == st and st + 1 <= 7:
                                if (ri - 1, st + 1) not in obsadene_polia:
                                    mozne_pozicie.add((ri-1, st+1))
                                    preskakovane_figurky.append(obsadene_polia[(ri, st)])
                            elif self.pozicia[1] - 1 == st  and st - 1 >= 0:
                                if (ri - 1, st - 1) not in obsadene_polia:
                                    mozne_pozicie.add((ri-1, st-1))
                                    preskakovane_figurky.append(obsadene_polia[(ri, st)])
       
        return mozne_pozicie, preskakovane_figurky
    
    # prepisana metoda je_mozne_skakat() pre damu
    def je_mozne_skakat(self, obsadene_polia):
        if not self.farba:
            farba = 1
        else:
            farba = 0
        # pozicie doskakovanych poli
        riadok1 = self.pozicia[0] - 2
        riadok2 = self.pozicia[0] + 2
        stlpec1 = self.pozicia[1] - 2
        stlpec2 = self.pozicia[1] + 2
        if riadok1 >= 0:
            if stlpec1 >= 0:
                # key je suradnica preskakovaneho policka
                # zistujeme ci je na nom superova figurka
                key = (self.pozicia[0]-1, self.pozicia[1]-1)
                #print(f'key {key}')
                #pprint(obsadene_polia)
                if ((riadok1, stlpec1) not in obsadene_polia and 
                    key in obsadene_polia and
                    obsadene_polia[key].farba == farba):
                    return True
            if stlpec2 <= 7:
                key = (self.pozicia[0]-1, self.pozicia[1]+1)
                #print(f'key {key}')
                #pprint(obsadene_polia)
                if ((riadok1, stlpec2) not in obsadene_polia and
                    key in obsadene_polia and
                    obsadene_polia[key].farba == farba):
                    return True
                    
        if riadok2 <= 7:
            if stlpec1 >= 0:
                # key je suradnica preskakovaneho policka
                # zistujeme ci je na nom superova figurka
                key = (self.pozicia[0]+1, self.pozicia[1]-1)
                #print(f'key {key}')
                #pprint(obsadene_polia)
                if ((riadok2, stlpec1) not in obsadene_polia and 
                    key in obsadene_polia and
                    obsadene_polia[key].farba == farba):
                    return True
            if stlpec2 <= 7:
                key = (self.pozicia[0]+1, self.pozicia[1]+1)
                #print(f'key {key}')
                #pprint(obsadene_polia)
                if ((riadok2, stlpec2) not in obsadene_polia and
                    key in obsadene_polia and
                    obsadene_polia[key].farba == farba):
                    return True            
        
        return False
    
class Sachovnica:
    
    def __init__(self, cierny_pesiak,
                        biely_pesiak, 
                        cierna_dama, 
                        biela_dama,
                        zoz_miz_cier, 
                        zoz_miz_biel,
                        zoz_miz_cier_d,
                        zoz_miz_biel_d,
                        zoz_vzn_cier_d,
                        zoz_vzn_biel_d):
        
        self.button_nova = ttk.Button(text='Nová partia', command=self.nova_partia)
        self.button_nova.pack(anchor=tkinter.N)
        
        self.button_otvor = ttk.Button(text='Otvor partiu', command=self.otvor_partiu)
        self.button_otvor.pack(anchor=tkinter.N)
        
        self.button_uloz = ttk.Button(text='Ulož partiu', command=self.uloz_partiu)
        self.button_uloz.pack(anchor=tkinter.N)
        
        self.canvas = tkinter.Canvas(width=820, height=820, bg='white')
        self.canvas.pack(anchor=tkinter.CENTER)
        
        self.obrazok_cierna_dama = cierna_dama
        self.obrazok_cierny_pesiak = cierny_pesiak
        self.obrazok_biela_dama = biela_dama
        self.obrazok_biely_pesiak = biely_pesiak
        self.zoz_miz_biel = zoz_miz_biel
        self.zoz_miz_cier = zoz_miz_cier
        self.zoz_miz_biel_d = zoz_miz_biel_d
        self.zoz_miz_cier_d = zoz_miz_cier_d
        self.zoz_vzn_biel_d = zoz_vzn_biel_d
        self.zoz_vzn_cier_d = zoz_vzn_cier_d
        
        self.zoz_mazanych_fig = []
        self.zoz_vznik_dam = []
        self.na_tahu = True # True-biely, False-cierny
        self.tahana_figurka = None # objekt figurky ktora je prave tahana
        self.x0, self.y0, self.d = 10, 10, 100 # pociatocne suradnice 
                                               # a dlzka d strany stvorca 
                                               # sachovnice
        self.biele_figurky = []
        self.obsadene_polia = {}
        self.cierne_figurky = []
        
        farba1, farba2 = '#DA8A67', '#E23D28' # farby sachovnice
        # vytvorenie sachovnice v cykle
        for r in range(8):
            farba1, farba2 = farba2, farba1
            farba = farba2
            for s in range(8):
                x1 = self.x0 + s * self.d
                y1 = self.y0 + r * self.d
                x2 = x1  + self.d
                y2 = y1 + self.d
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=farba)
                farba1, farba2 = farba2, farba1
                farba = farba2
                
        # popis riadkov sachovnice
        for r in range(8):
            self.canvas.create_text((5, 5 + (r + 0.5)*self.d), text=str(8-r),
                                    font='Arial 10 bold')
        # popis stlpcov sachovnice                            
        for s, text in enumerate('ABCDEFGH'):
            self.canvas.create_text((5 + (s + 0.5)*self.d, 817), text=text, 
                                    font='Arial 10 bold')  
        
        # pociatocne rozlozenie figurok na sachovnici
        self.nova_partia()
        
    def nova_partia(self):
        for figurka in self.biele_figurky:
            self.canvas.delete(figurka.id_obrazka)
            
        self.biele_figurky = []
        
        for figurka in self.cierne_figurky:
            self.canvas.delete(figurka.id_obrazka)
            
        self.cierne_figurky = []
        
        self.obsadene_polia = {}
        
        for s in range(1, 8, 2):
            id = self.canvas.create_image(self.x0 + (s + 0.5)*self.d,
                                          self.y0 + self.d/2, 
                                          image=self.obrazok_cierny_pesiak)
            p = Pesiak(pozicia=(0, s), farba=1, id_obrazka=id)
            self.cierne_figurky.append(p)
            self.obsadene_polia[(0, s)] = p # riadok, stlpec, 
                                            # objekt Pesiak
            
        for s in range(0, 8, 2):
            id = self.canvas.create_image(self.x0 + (s + 0.5)*self.d,
                                          self.y0 + 3 * self.d/2, 
                                          image=self.obrazok_cierny_pesiak)
            p = Pesiak(pozicia=(1, s), farba=1, id_obrazka=id)
            self.cierne_figurky.append(p)
            self.obsadene_polia[(1, s)] = p
            
        for s in range(0, 8, 2):
            id = self.canvas.create_image(self.x0 + (s + 0.5)*self.d,
                                          self.y0 + 7.5*self.d,
                                          image=self.obrazok_biely_pesiak)
            p = Pesiak(pozicia=(7, s), farba=0, id_obrazka=id)
            self.biele_figurky.append(p)
            self.obsadene_polia[(7, s)] = p
            
        for s in range(1, 8, 2):
            id = self.canvas.create_image(self.x0 + (s + 0.5)*self.d, 
                                          self.y0 + 6.5*self.d, 
                                          image=self.obrazok_biely_pesiak)
            p = Pesiak(pozicia=(6, s), farba=0, id_obrazka=id)
            self.biele_figurky.append(p)
            self.obsadene_polia[(6, s)] = p
        try:    
            self.canvas.delete(self.id_text_vyhra)
        except AttributeError:
            pass
        
        # pridaj udalosti mysi
        self.pridaj_udalosti()

    def pridaj_udalosti(self):
        self.canvas.bind('<ButtonPress-1>', self.mouse_down)
        self.canvas.bind('<B1-Motion>', self.mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self.mouse_up)
  
    def otvor_partiu(self):
        meno_suboru = fd.askopenfilename(
                            title = 'Zvoľte subor',
                            initialdir = os.getcwd(),
                            defaultextension = ".txt",
                            filetypes = [('textové súbory', '*.txt')]
                            )
        
        for figurka in self.biele_figurky:
            self.canvas.delete(figurka.id_obrazka)
            
        self.biele_figurky = []
        
        for figurka in self.cierne_figurky:
            self.canvas.delete(figurka.id_obrazka)
            
        self.cierne_figurky = []
        
        self.obsadene_polia = {}
        
        with open(meno_suboru) as f:
            # vyradim legendu k zapisu v subore
            f.readline()
            f.readline()
            f.readline()
            
            #na tahu je 1-biely, 0-cierny
            line = f.readline()
            line = line.rstrip()
            if line == '1': # na tahu biely
                self.na_tahu = True
            else:
                self.na_tahu = False
                
            for line in f:
                line = line.rstrip()
                figurka, farba, riadok, stlpec = line.split()
                self.poloz_figurku_na_sachovnicu(figurka, int(farba), int(riadok), int(stlpec))
        try:    
            self.canvas.delete(self.id_text_vyhra)
            self.pridaj_udalosti()
        except AttributeError:
            pass
            
    def uloz_partiu(self):
        meno_suboru = fd.asksaveasfilename(
                            title = 'Zvoľte subor',
                            initialdir = os.getcwd(),
                            defaultextension = ".txt",
                            filetypes = [('textové súbory', '*.txt')]
                            )
                            
        with open(meno_suboru, 'w') as f:
            f.write('#legenda:\n')
            f.write('# na tahu je 1-biely 0-cierny\n')
            f.write('#p-pesiak/d-dama farba(0 - biely, 1 - cierny) riadok stlpec\n')
            
            if self.na_tahu: #na tahu je biely
                f.write('1\n')
            else: #na tahu je cierny
                f.write('0\n')
            
            for figurka in self.biele_figurky:
                if isinstance(figurka, Dama):
                    f.write('d ')
                else:
                    f.write('p ')
                    
                f.write('0 ')#farba figurky
                
                f.write(f'{figurka.pozicia[0]} {figurka.pozicia[1]}\n')
                
            for figurka in self.cierne_figurky:
                if isinstance(figurka, Dama):
                    f.write('d ')
                else:
                    f.write('p ')
                    
                f.write('1 ')#farba figurky
                
                f.write(f'{figurka.pozicia[0]} {figurka.pozicia[1]}\n')
            
    # prida figurku na sachovnicu
    def poloz_figurku_na_sachovnicu(self, figurka, farba, riadok, stlpec):
        x, y = self.daj_suradnice(riadok, stlpec)
        
        if farba == 0:#biele
            if figurka == 'p':
                image = self.obrazok_biely_pesiak
            else:
                image = self.obrazok_biela_dama
        else: # cierne
            if figurka == 'p':
                image = self.obrazok_cierny_pesiak
            else:
                image = self.obrazok_cierna_dama
                
        id = self.canvas.create_image(x, y, image=image)
        if figurka == 'p':
            fig = Pesiak(pozicia=(riadok, stlpec), farba=farba, id_obrazka=id)
        else:
            fig = Dama(pozicia=(riadok, stlpec), farba=farba, id_obrazka = id)
        if farba == 0: #biele
            self.biele_figurky.append(fig)
        else: # cierne  
            self.cierne_figurky.append(fig)
        self.obsadene_polia[(riadok, stlpec)] = fig
        
        
    # metoda ktora vrati riadok a stlpec sachovnice podla x a y suradnic
    def daj_poziciu(self, x, y):
        s = math.floor((x - self.x0) / self.d)
        r = math.floor((y - self.y0) / self.d)
        return r, s
        
    # metoda ktora vrati x, y suradnice stredu stvorca sachovnice podla r, s    
    def daj_suradnice(self, r, s):
        x = self.x0 + (s + 0.5) * self.d
        y = self.y0 + (r + 0.5) * self.d
        return x, y
        
        
    def mouse_down(self, event):
        r, s = self.daj_poziciu(event.x, event.y)
        self.tahana_figurka = None
        if self.na_tahu:
            # na tahu su biele figurky
            # zistovanie v cykle ktora figurka je vybrana
            for figurka in self.biele_figurky:
                if figurka.pozicia == (r, s):
                    self.obsadene_polia.pop((r, s))
                    self.canvas.lift(figurka.id_obrazka) # sposobi ze ostatne
                                                         # obrazky budu pod 
                                                         # tahanou figurkou
                    self.canvas.coords(figurka.id_obrazka, event.x, event.y)
                    self.tahana_figurka = figurka
                    break
        else: # na tahu su cierne figurky
            # zistovanie v cykle ktora figurka je vybrana
            for figurka in self.cierne_figurky:
                if figurka.pozicia == (r, s):
                    self.obsadene_polia.pop((r, s))
                    self.canvas.lift(figurka.id_obrazka)
                    self.canvas.coords(figurka.id_obrazka, event.x, event.y)
                    self.tahana_figurka = figurka
                    break
    
    def mouse_move(self, event):
        if self.tahana_figurka is not None:
            self.canvas.coords(self.tahana_figurka.id_obrazka,
                               event.x, event.y)
            
    def mouse_up(self, event):
        if self.tahana_figurka is not None:
            r, s = self.daj_poziciu(event.x, event.y)
            tahy, preskakovane_figurky = self.tahana_figurka.mozne_tahy(self.obsadene_polia)
            
            # ak je tahana pozicia v moznych tahoch pre tahanu figurku tak spracuj
            if (r, s) in tahy:
                # minuly stav skokanov na sachovnici
                    # je nutne pridat do obsadenych poli aj pole 
                    # ktore je povodne pole tahanej figurky , pretoze aj toto pole je obsadene
                    # (toto pole je z obsadenych poli zmazane v mouse_down() metode
                    # a tu je v dalsich riadkoch kodu prepisana pozicia tahanej figurky)
                obsadene_polia = self.obsadene_polia.copy()
                obsadene_polia[(self.tahana_figurka.pozicia)] = self.tahana_figurka
                self.pred_bieli_skokani, self.pred_cierni_skokani = self.figurky_skokani(obsadene_polia)
              
                # nastavenie pozicii a presun obrazka figurky na nove pole
                self.obsadene_polia[(r, s)] = self.tahana_figurka
                self.tahana_figurka.pozicia = (r, s)
                x, y = self.daj_suradnice(r, s)
                self.canvas.coords (self.tahana_figurka.id_obrazka, x, y)
                
                # zmazanie preskocenej figurky
                self.tahana_figurka_skakala = False
                for figurka in preskakovane_figurky:
                    if figurka.farba == 0:
                        if (figurka.pozicia == (r-1, s-1) or figurka.pozicia == (r-1, s+1) or
                            figurka.pozicia == (r+1, s-1) or figurka.pozicia == (r+1, s+1)):
                            self.zmaz_figurku(figurka)
                            self.tahana_figurka_skakala = True
                    elif figurka.farba == 1:
                        if (figurka.pozicia == (r+1, s-1) or figurka.pozicia == (r+1, s+1) or
                            figurka.pozicia == (r-1, s-1) or figurka.pozicia == (r-1, s+1)):
                            self.tahana_figurka_skakala = True
                            self.zmaz_figurku(figurka)
                
               
                # ponechanie tahu na tu istu farbu figuriek ak je dvoj skok alebo viac skok
                if len(preskakovane_figurky) != 0:
                    tahy, preskakovane_figurky = self.tahana_figurka.mozne_tahy(self.obsadene_polia)
                    if len(preskakovane_figurky) == 0:
                        self.na_tahu = not self.na_tahu
                else:
                    self.na_tahu = not self.na_tahu
                
                # najnovsi stav skokanov na sachovnici
                self.bieli_skokani, self.cierni_skokani = self.figurky_skokani(self.obsadene_polia)
                
                # vymaze figurky ktore mali skakat a neskakali
                self.vyrad_skokanov(self.tahana_figurka) 
                
                # skontroluje ci je kamen na pozicii pre premenu na damu
                # a nahradi figurku pesiaka figurkou damy
                self.premena_na_damu(r, s)
                
                # kontrola ci niekto nevyhral alebo nie je remiza
                self.kontrola_vyhry()
                
                # tahana figurka dokoncila tah a tak je None, prestala byt tahanou
                self.tahana_figurka = None
                
            else: # ak je ukladana figurka na nemoznu poziciu
                  # vrati tahanu figurku na jej vychodziu poziciu
                r, s = self.tahana_figurka.pozicia
                self.obsadene_polia[(r, s)] = self.tahana_figurka
                x, y = self.daj_suradnice(r, s)
                self.canvas.coords (self.tahana_figurka.id_obrazka, x, y)
                self.tahana_figurka = None
    
    # Tato metoda zmaze figurku, odstrani ju z premennych a zmaze obrazok 
    # tejto figurky - sem zrejme dam animaciu miznutia pesiaka/damy
    def zmaz_figurku(self, figurka):
        self.obsadene_polia.pop(figurka.pozicia)
       
        if figurka.farba == 0:
            self.biele_figurky.remove(figurka)
        elif figurka.farba == 1:
            self.cierne_figurky.remove(figurka)
        
        # animacia miznutia figurok
        self.zoz_mazanych_fig.append(figurka)
        self.miznutie_figurok()
        
    
    # Tato metoda sluzi na najdenie vsetkych figurok skokanov
    # bielych aj ciernych
    def figurky_skokani(self, obsadene_polia):
        bieli_skokani = set()
        for figurka in self.biele_figurky:
            if figurka.je_mozne_skakat(obsadene_polia):
                bieli_skokani.add(figurka)
                
        cierni_skokani = set()
        for figurka in self.cierne_figurky:
            if figurka.je_mozne_skakat(obsadene_polia):
                cierni_skokani.add(figurka)
        
        return bieli_skokani, cierni_skokani
    
 
    # tato metoda sluzi na zmazanie figuriek skokanou ktori neskakali    
    def vyrad_skokanov(self, tahana_figurka):
        
        #print('pred bieli skokani')
        #pprint(self.pred_bieli_skokani)
        #print('pred cierni skokani')
        #pprint(self.pred_cierni_skokani)
        #print('po bieli skokani')
        #pprint(self.bieli_skokani)
        #print('po cierni skokani')
        #pprint(self.cierni_skokani)
        
        if self.na_tahu: # bieli
            skokani_neskakali = self.pred_cierni_skokani & self.cierni_skokani
            jeden_skokan_zmazany = False # osetrenie toho ak su dvaja skokani
                                         # a jeden z nich je tahana figurka
            
            # zistuje ci je tahana figurka dama a ta ma prednost, preto ju zmaze
            if (isinstance(tahana_figurka, Dama) and 
                tahana_figurka in self.pred_cierni_skokani and 
                not self.tahana_figurka_skakala):
                self.zmaz_figurku(tahana_figurka) 
                jeden_skokan_zmazany = True
                
            # zistovanie ci je skokan dama a ta ma prednost, preto ju zmaze 
            if not jeden_skokan_zmazany and not self.tahana_figurka_skakala:
                for skokan in skokani_neskakali:
                    if isinstance(skokan, Dama):
                        self.zmaz_figurku(skokan)
                        jeden_skokan_zmazany = True
                        break
                        
            # skontroluje ci dama nemala skakat a ak ano vymaze ju 
            #  ak uz jedna dama nebola zmazana
            if not jeden_skokan_zmazany:
                for skokan in self.pred_cierni_skokani:
                    if (isinstance(skokan, Dama) and skokan != self.tahana_figurka and
                        skokan in self.cierne_figurky and
                        not isinstance(self.tahana_figurka, Dama)):
                        self.zmaz_figurku(skokan)
                        jeden_skokan_zmazany = True
                        break
                
            # zistuje ci je tahana figurka (Pesiak, pretoze damy 
            # sme vyradili v predchadzajucich krokoch) medzi skokanmi 
            # a ak neskakala tak ju zmaze       
            if (not jeden_skokan_zmazany and tahana_figurka in self.pred_cierni_skokani and 
                not self.tahana_figurka_skakala):
                self.zmaz_figurku(tahana_figurka) 
                jeden_skokan_zmazany = True
                
            # ak ziadna z predchadzajucich figuriek nebola zmazana
            # zmaze jedneho skokana (Pesiaka, lebo damy sme vyradili v predch. krokoch)    
            if not jeden_skokan_zmazany and not self.tahana_figurka_skakala:
                for skokan in skokani_neskakali:
                    self.zmaz_figurku(skokan)
                    jeden_skokan_zmazany = True
                    break
            
            # skontroluje ci nejaki pesiaci nemali skakat 
            # a zostali na mieste a ak ano zmazem jedneho
            # ak uz jeden nebol zmazany predtym
            # (to ze nieje tahanou figurkou znamena ze zostal na mieste)
            if not jeden_skokan_zmazany and not self.tahana_figurka_skakala:
                for skokan in self.pred_cierni_skokani:
                    if (skokan != self.tahana_figurka and
                        skokan in self.cierne_figurky):
                        self.zmaz_figurku(skokan)
                        break
                       
        else: #cierni
            skokani_neskakali = self.pred_bieli_skokani & self.bieli_skokani
            jeden_skokan_zmazany = False
            
            if (isinstance(tahana_figurka, Dama) and 
                tahana_figurka in self.pred_bieli_skokani and 
                not self.tahana_figurka_skakala):
                self.zmaz_figurku(tahana_figurka) 
                jeden_skokan_zmazany = True
                
            if not jeden_skokan_zmazany and not self.tahana_figurka_skakala:
                for skokan in skokani_neskakali:
                    if isinstance(skokan, Dama):
                        self.zmaz_figurku(skokan)
                        jeden_skokan_zmazany = True
                        break
                        
            if not jeden_skokan_zmazany:
                for skokan in self.pred_bieli_skokani:
                    if (isinstance(skokan, Dama) and skokan != self.tahana_figurka and
                        skokan in self.biele_figurky and not isinstance(self.tahana_figurka, Dama)):
                        self.zmaz_figurku(skokan)
                        jeden_skokan_zmazany = True
                        break
                
            if (not jeden_skokan_zmazany and tahana_figurka in self.pred_bieli_skokani and 
                not self.tahana_figurka_skakala):
                self.zmaz_figurku(tahana_figurka)
                jeden_skokan_zmazany = True
                
            if not jeden_skokan_zmazany and not self.tahana_figurka_skakala:
                for skokan in skokani_neskakali:
                    self.zmaz_figurku(skokan)
                    jeden_skokan_zmazany = True
                    break
            
            if not jeden_skokan_zmazany and not self.tahana_figurka_skakala:
                for skokan in self.pred_bieli_skokani:
                    if (skokan != self.tahana_figurka and
                        skokan in self.biele_figurky):
                        self.zmaz_figurku(skokan)
                        break
                    
    # Tato metoda skontroluje ci je figurka na prvom alebo poslednom riadku
    # sachovnice podla farby figurky a ak je tak premeni figurku na damu
    # Niekde sem by som mohol dat animaciu premeny figurky na damu
    # alebo to spravim vsetko v metode zmaz_figurku()
    def premena_na_damu(self, r, s):
        if isinstance(self.tahana_figurka, Pesiak):
            x, y = self.daj_suradnice(r, s)
            if self.tahana_figurka.farba == 0: # biela
                if self.tahana_figurka.pozicia[0] == 0:
                    #id = self.canvas.create_image(x, y, image=self.obrazok_biela_dama)
                    id = self.canvas.create_image(x, y)
                    d = Dama(pozicia=(r, s), farba=0, id_obrazka=id)
                    
                    # animacia vzniku damy
                    self.zoz_vznik_dam.append(d)
                    self.vznik_damy()
                    
                    self.biele_figurky.append(d)
                    self.zmaz_figurku(self.tahana_figurka) # toto musi byt pred dalsim riadkom
                    self.obsadene_polia[(r, s)] = d # toto musi byt za predchadzajucim riadkom
            else: # cierna
                if self.tahana_figurka.pozicia[0] == 7:
                    #id = self.canvas.create_image(x, y, image=self.obrazok_cierna_dama)
                    id = self.canvas.create_image(x, y)
                    d = Dama(pozicia=(r, s), farba=1, id_obrazka=id)
                    
                    # animacia vzniku damy
                    self.zoz_vznik_dam.append(d)
                    self.vznik_damy()
                    
                    self.cierne_figurky.append(d)
                    self.zmaz_figurku(self.tahana_figurka)
                    self.obsadene_polia[(r, s)] = d
    
    # Tato metoda sluzi na animaciu vyhodenych figuriek
    # postupne miznutie figurky
    def miznutie_figurok(self):
        for figurka in self.zoz_mazanych_fig:
            if isinstance(figurka, Pesiak):# figurka je pesiak
                if figurka.farba == 0: #bieli
                    image = self.zoz_miz_biel[figurka.faza_animacie]
                else:# cierni
                    image = self.zoz_miz_cier[figurka.faza_animacie]
            else: # figurka je dama
                if figurka.farba == 0: #bieli
                    image = self.zoz_miz_biel_d[figurka.faza_animacie]
                else:# cierni
                    image = self.zoz_miz_cier_d[figurka.faza_animacie]
                    
            self.canvas.itemconfig(figurka.id_obrazka, image=image)
            figurka.faza_animacie += 1
            
            if figurka.faza_animacie < 3:
                self.canvas.after(100, self.miznutie_figurok)
            else:
                self.canvas.delete(figurka.id_obrazka)
                self.zoz_mazanych_fig.remove(figurka)
                
                    
    # Tato metoda sluzi na animaciu vzniku damy
    def vznik_damy(self):
        for figurka in self.zoz_vznik_dam:
            if figurka.farba == 0: #bieli
                image = self.zoz_vzn_biel_d[figurka.faza_animacie]
            else:# cierni
                image = self.zoz_vzn_cier_d[figurka.faza_animacie]
                
            self.canvas.itemconfig(figurka.id_obrazka, image=image)
            figurka.faza_animacie += 1
            
            if figurka.faza_animacie < 3:
                self.canvas.after(300, self.vznik_damy)
            else:
                figurka.faza_animacie = 0
                self.zoz_vznik_dam.remove(figurka)
                if figurka.farba == 0: #bieli
                    self.canvas.itemconfig(figurka.id_obrazka, image=self.obrazok_biela_dama)
                else:# cierni
                    self.canvas.itemconfig(figurka.id_obrazka, image=self.obrazok_cierna_dama)  


    def kontrola_vyhry(self):
        vitazstvo = False
        if len(self.biele_figurky) == 0:
            self.id_text_vyhra = self.canvas.create_text(400, 400, text='Vyhral cierny', 
                                    fill='white',
                                    font='Arial 50 bold')
            self.vyrad_udalosti()
            vitazstvo = True
        if len(self.cierne_figurky) == 0:
            self.id_text_vyhra = self.canvas.create_text(400, 400, text='Vyhral biely',
                                    fill='white',
                                    font='Arial 50 bold')        
            self.vyrad_udalosti()
            vitazstvo = True
            
        # ak nie je mozne urobit tah tak remiza
        if not vitazstvo and not self.su_mozne_tahy():
            self.id_text_vyhra = self.canvas.create_text(400, 400, text='Remiza',
                                    fill='white',
                                    font='Arial 50 bold')        
            self.vyrad_udalosti()
    
    # vyradi udalosti na canvase
    def vyrad_udalosti(self):
        self.canvas.unbind('<ButtonPress-1>')
        self.canvas.unbind('<B1-Motion>')
        self.canvas.unbind('<ButtonRelease-1>')
    
    # metoda zisti ci su mozne tahy pre hraca ktory je na tahu
    # a vrati True alebo False
    def su_mozne_tahy(self):
        if self.na_tahu:#na tahu je biely
            for figurka in self.biele_figurky:
                tahy, presk = figurka.mozne_tahy(self.obsadene_polia)
                if len(tahy) != 0:
                    return True
        else: #na tahu su cierni
            for figurka in self.cierne_figurky:
                tahy, presk = figurka.mozne_tahy(self.obsadene_polia)
                if len(tahy) != 0:
                    return True
                    
                    
class Program:

    def __init__(self):
        
        win = tkinter.Tk()
        
        cierny_pesiak = Image.open('obrazky/cierny_pesiak.png')
        cierny_pesiak = cierny_pesiak.resize((100, 100))
        cierny_pesiak = ImageTk.PhotoImage(cierny_pesiak)
        
        biely_pesiak = Image.open('obrazky/biely_pesiak.png')
        biely_pesiak = biely_pesiak.resize((100, 100))
        biely_pesiak = ImageTk.PhotoImage(biely_pesiak)
        
        cierna_dama = Image.open('obrazky/cierna_dama.png')
        cierna_dama = cierna_dama.resize((100, 100))
        cierna_dama = ImageTk.PhotoImage(cierna_dama)
        
        biela_dama = Image.open('obrazky/biela_dama.png')
        biela_dama = biela_dama.resize((100, 100))
        biela_dama = ImageTk.PhotoImage(biela_dama)
        
        # zoznam miznutia bieleho pesiaka
        zoz_miz_biel = []
        for i in range(1, 4):
            obr = Image.open(f'obrazky/biely_pesiak_faza1.{i}.png')
            obr = obr.resize((100, 100))
            zoz_miz_biel.append(ImageTk.PhotoImage(obr))
        
        # zoznam miznutia cierneho pesiaka    
        zoz_miz_cier = []
        for i in range(1, 4):
            obr = Image.open(f'obrazky/cierny_pesiak_faza1.{i}.png')
            obr = obr.resize((100, 100))
            zoz_miz_cier.append(ImageTk.PhotoImage(obr)) 
        
        # zoznam miznutia bielej damy    
        zoz_miz_biel_d = []
        for i in range(1, 4):
            obr = Image.open(f'obrazky/biela_dama_faza1.{i}.png')
            obr = obr.resize((100, 100))
            zoz_miz_biel_d.append(ImageTk.PhotoImage(obr))
        
        # zoznam miznutia ciernej damy 
        zoz_miz_cier_d = []
        for i in range(1, 4):
            obr = Image.open(f'obrazky/cierna_dama_faza1.{i}.png')
            obr = obr.resize((100, 100))
            zoz_miz_cier_d.append(ImageTk.PhotoImage(obr)) 
        
        # zoznam vzniku bielej damy    
        zoz_vzn_biel_d = []
        for i in range(1, 4):
            obr = Image.open(f'obrazky/biela_dama_vznik1.{i}.png')
            obr = obr.resize((100, 100))
            zoz_vzn_biel_d.append(ImageTk.PhotoImage(obr))
        
        # zoznam vzniku ciernej damy  
        zoz_vzn_cier_d = []
        for i in range(1, 4):
            obr = Image.open(f'obrazky/cierna_dama_vznik1.{i}.png')
            obr = obr.resize((100, 100))
            zoz_vzn_cier_d.append(ImageTk.PhotoImage(obr)) 
            
        Sachovnica(cierny_pesiak, 
                    biely_pesiak, 
                    cierna_dama, 
                    biela_dama,
                    zoz_miz_cier, 
                    zoz_miz_biel,
                    zoz_miz_cier_d,
                    zoz_miz_biel_d,
                    zoz_vzn_cier_d,
                    zoz_vzn_biel_d)
                                
        win.mainloop()
                    
Program()        