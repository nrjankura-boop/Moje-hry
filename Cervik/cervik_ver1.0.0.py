import tkinter
import random

class Hlava:
    
    def __init__(self, r, s, d, x0, y0):
        self.r = r # riadok v ktorom lezi hlava cervicka
        self.s = s # stlpce v ktorom lezi hlava cervicka
        self.d = d # polomer hlavy cervicka, resp. dlzka strany stvorca clanku
        self.x0 = x0 # pociatocna suradnica x hracej plochy
        self.y0 = y0 # pociatocna suradnica y hracej plochy
        self.za = None # odkaz na objekt triedy Clanok ktory nasleduje za hlavou cervicka
        self.id_clanku = None # id nakresleneho objektu hlavy, resp. clanku cervicka na canvase
        
        # Prida tri clanky cervicka na zaciatok
        for _ in range(3):
            self.pridaj_clanok()
            
    def posun(self, r, s):
        # ak nasledovny clanok cervicka existuje tak ho posunie
        if self.za is not None:
            self.za.posun(self.r, self.s)
        self.r = r
        self.s = s
        self.prekresli()
        
    def prekresli(self):
        # ak existuje id clanku (hlavy cervicka) tak ho zmaze a nasledne ho znova nakresli
        # s novymi suradnicami
        if self.id_clanku is not None:
            canvas.delete(self.id_clanku)
        x1 = self.x0 + self.s * self.d
        x2 = self.x0 + (self.s + 1) * self.d
        y1 = self.y0 + self.r * self.d
        y2 = self.y0 + (self.r + 1) * self.d
        self.id_clanku = canvas.create_oval(x1, y1, x2, y2, width=0, fill="lightcoral")
    
    # Prida clanok za posledny clanok cervicka, vytvor objekt triedy Clanok
    def pridaj_clanok(self):
        za = self
        while za.za is not None:
            za = za.za
        za.za = Clanok(self.d, self.x0, self.y0, za)
        za.za.prekresli()
    
    # Vrati suradnice r, s vsetkych casti cervika    
    def vrat_suradnice(self):
        suradnice = []
        suradnice.append((self.r, self.s))
        za = self
        while za.za is not None:
            suradnice.append((za.za.r, za.za.s))
            za = za.za
        return suradnice 
        
class Clanok(Hlava):
    
    def __init__(self, d, x0, y0, pred):
        self.d = d # dlzka strany stvorca clanku
        self.x0 = x0 # pociatocna suradnica x hracej plochy
        self.y0 = y0 # pociatocna suradnica y hracej plochy
        self.pred = pred # je odkaz na objekt ktory predchadza tomuto clanku
        self.za = None # je odkaz na objekt ktory nasleduje za tymto clankom
        self.id_clanku = None # id nakresleneho objektu hlavy, resp. clanku cervicka na canvase
        self.farby = ["rosybrown", "red"] # farby blikania pridaneho clanku
        self.pocet_zablikani = 6 # Pocet zablikani pridaneho clanku, je o jedno mensi ako toto cislo
        self.prave_pridany = True # Indikator toho ze clanok bol prave pridany
        
        # Nastavenie novych suradnic novovytvoreneho clanku v zavislosti na predchadzajucich
        # dvoch clankoch. 
        if isinstance(self.pred, Clanok):
            if self.pred.r == self.pred.pred.r:
                self.r = self.pred.r
                if self.pred.s < self.pred.pred.s:
                    self.s = self.pred.s - 1
                else:
                    self.s = self.pred.s + 1
                    
            if self.pred.s == self.pred.pred.s:
                self.s = self.pred.s
                if self.pred.r < self.pred.pred.r:
                    self.r = self.pred.r - 1
                else:
                    self.r = self.pred.r + 1
        # Nasledovne else je pre pripad ze predchadzajuci objekt je triedy Hlava
        # a zaroven nie je triedy Clanok, ako jednotlive clanky, ktore su objektom 
        # ako triedy Hlava tak aj triedy Clanok. Ide o pripad ze predchodca tohto
        # vytvoreneho clanku cervicka je hlava cervicka.
        else:
            self.r = self.pred.r + 1
            self.s = self.pred.s
        
    def prekresli(self):
        # ak existuje id clanku tak ho zmaze a nasledne ho znova nakresli
        # s novymi suradnicami
        if self.id_clanku is not None:
            canvas.delete(self.id_clanku)
        x1 = self.x0 + self.s * self.d
        x2 = self.x0 + (self.s + 1) * self.d
        y1 = self.y0 + self.r * self.d
        y2 = self.y0 + (self.r + 1) * self.d
        self.id_clanku = canvas.create_oval(x1, y1, x2, y2, width=0, fill='rosybrown')
        #self.id_clanku = canvas.create_rectangle(x1, y1, x2, y2, width=0, fill='rosybrown')
        
        # Ak bol clanok prave pridany tak zablikaj farbou na tomto clanku
        if self.prave_pridany:
            self.prave_pridany = False
            self.pocet = 0
            self.zablikaj()
        
    def zablikaj(self):
        self.pocet += 1
        farba = self.farby[self.pocet%2]
        canvas.itemconfig(self.id_clanku, fill = farba)
        if self.pocet < self.pocet_zablikani:
            canvas.after(100, self.zablikaj)
        else:
            canvas.itemconfig(self.id_clanku, fill = 'rosybrown')
            
class Listocky:
    
    def __init__(self, d, x0, y0, pocet_r, pocet_s):
        self.d = d
        self.x0 = x0
        self.y0 = y0
        self.pocet_r = pocet_r
        self.pocet_s = pocet_s
        self.idcka = {}
        
    def vykresli(self, r, s):
        x1 = self.x0 + s* self.d + self.d//2 
        y1 = self.y0 + r*self.d
        x2 = self.x0 + s * self.d
        y2 = self.y0 + (r + 1) * self.d
        x3 = self.x0 + (s + 1) * self.d
        y3 = self.y0 + (r + 1) * self.d
        id = canvas.create_polygon(x1, y1, x2, y2, x3, y3, fill="green", width=0)
        self.idcka[r, s] = id
    
    def zmaz(self, r, s):
        canvas.delete(self.idcka[r, s])
        self.idcka.pop((r, s))
        
    def pridaj(self, suradnice):
        r = random.randint(0, self.pocet_r)
        s = random.randint(0, self.pocet_s)
        while (r, s) in self.idcka or (r, s) in suradnice:
            r = random.randint(0, self.pocet_r)
            s = random.randint(0, self.pocet_s)
        self.vykresli(r, s)
        
class Cervik():

    def __init__(self):
        
        self.pocet_r = 36 # pocet riadkov hracej plochy
        
        self.pocet_s = 32 # pocet stlpcov hracej plochy
        
        self.d = 15       # strana stvorca clanku, polomer hlavy cervika, 
                          # hracia plocha sa deli na stvorceky so stranou self.d  
                          
        self.x0 = 20      # pociatocna x suradnica , suradnica nuly pre x os
        self.y0 = 100      # pociatocna y suradnica , suradnica nuly pre y os
        
        self.dr = -1      # pociatocny posun cervika v smere y, posun o 1 riadok do hora
        self.ds = 0       # pociatocny posun cervika v smere x, posun o 0 stlpcov
        
        self.rychlost = 500             # Pociatocna rychlost cervicka
        
        self.delta_rychlost = 20        # Zmena rychlosti cervicka
        
        self.rychlost_po_score = 100    # Po kazdej zmene score o rychlost_po_score
                                        # sa zmeni rychlost cervicka o delta_rychlost
        
        self.score = 0    # Hodnota score, pociatocna je nula
        
        self.delta_score = 20 # Hodnota ktora sa prida ku skore ak cervik spapa listocek
        
        pocet_listockov = 40 # Konstantny pocet listockov na hracej ploche
        
        self.cervik_sa_poziera = False # Indikator toho ci cervik poziera seba sameho
        
        self.koniec = False # Indikator konca hry
        
        # Konecny bod hracej plochy
        self.x_end = self.x0 + (self.pocet_s + 1) * self.d
        self.y_end = self.y0 + (self.pocet_r + 1) * self.d
        
        # Hracia plocha
        canvas.create_rectangle(self.x0, self.y0, self.x_end, self.y_end, width=3)
        
        # Score
        self.id_score = canvas.create_text(300, 50, text=self.score, font='Arial 20')
        
        # Copyright
        canvas.create_text(self.x_end//2, self.y_end + 50, text = "© Norbert Jankura, nr.jankura@gmail.com", font="Arial 13")
        
        # Pociatocna poloha cervika, su to suradnice riadka a stlpca pre hlavu cervika
        self.r = self.pocet_r//2
        self.s = self.pocet_s//2
        
        # Pociatocne vykreslenie cervika jeho hlava a tri clanky
        self.cervik = Hlava(self.r, self.s, self.d, self.x0, self.y0)
        
        # Vykresli listocky
        self.listocek = Listocky(self.d, self.x0, self.y0, self.pocet_r, self.pocet_s)
        for _ in range(pocet_listockov):
            r = random.randint(0, self.pocet_r)
            s = random.randint(0, self.pocet_s)
            while (r, s) in self.listocek.idcka or (r, s) in self.cervik.vrat_suradnice():
                r = random.randint(0, self.pocet_r)
                s = random.randint(0, self.pocet_s)
            self.listocek.vykresli(r, s)
        
        # Previazanie sipok klavesnice pre ovladanie smeru napredovania cervika 
        canvas.bind_all('<Left>', self.dolava)
        canvas.bind_all('<Right>', self.doprava)
        canvas.bind_all('<Up>', self.hore)
        canvas.bind_all('<Down>', self.dole)
        canvas.unbind_all('<space>')
        
        self.pohyb()
    
    # automaticky pohyb cervika    
    def pohyb(self):
        self.r += self.dr
        self.s += self.ds
        
        self.kontrola_hranic()
        if self.cervik_sa_poziera:
            self.cervik.posun(self.r, self.s)
        if not self.koniec:
            self.cervik.posun(self.r, self.s)
            if (self.r, self.s) in self.listocek.idcka:
                self.listocek.zmaz(self.r, self.s)
                self.cervik.pridaj_clanok()
                self.listocek.pridaj(self.cervik.vrat_suradnice())
                self.score += self.delta_score
                self.prepis_score()
                self.zmen_rychlost()
            canvas.after(self.rychlost, self.pohyb)
        else:
            canvas.create_text(100, 50, text='Stlac medzernik', font='Arial 15')
            canvas.bind_all('<space>', self.odznova)
    
    def odznova(self, arg):
        canvas.delete('all')
        self.__init__()
    
    def kontrola_hranic(self):
        if 0 > self.r or self.r > self.pocet_r or 0 > self.s or self.s > self.pocet_s: 
            self.koniec = True
        if (self.r, self.s) in self.cervik.vrat_suradnice():
            self.koniec = True
            self.cervik_sa_poziera = True
            
    def prepis_score(self):
        canvas.itemconfig(self.id_score, text=self.score)
    
    def zmen_rychlost(self):
        if self.score % self.rychlost_po_score == 0 and self.rychlost > 100:
            self.rychlost -= self.delta_rychlost
    
    def dolava(self, arg):
        self.dr = 0
        self.ds = -1
        
    def doprava(self, arg):
        self.dr = 0
        self.ds = 1
        
    def hore(self, arg):
        self.dr = -1
        self.ds = 0
        
    def dole(self, arg):
        self.dr = 1
        self.ds = 0
        
win = tkinter.Tk()
canvas = tkinter.Canvas(width=650, height=750)
canvas.pack()

Cervik()

tkinter.mainloop()  