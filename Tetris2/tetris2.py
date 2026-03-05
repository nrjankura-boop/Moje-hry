import tkinter, random
class Utvar:
    
    def __init__(self):
        # farby utvarov
        farby = (
                    'firebrick',
                    'red',
                    'sienna',
                    'gold',
                    'chartreuse',
                    'darkgreen',
                    'lightseagreen',
                    'navy',
                    'darkorchid4',
                    'orange',
                    'green',
                    'limegreen',
                    'darkmagenta',
                    'crimson'
                )
        self.farba = random.choice(farby) # farba objektu, utvaru
        
        self.params = [] # parametre objektu obsahuje vsetky stvorce utvaru 
                            # s ich suradnicami a id_ckami
        
        self.x0 = 250    # pociatocna x suradnica objektu, utvaru
        self.y0 = 700   # pociatocna y suradnica objekut, utvaru
        
    # zmaze cely utvar    
    def zmaz(self):
        for param in self.params:
            canvas.delete(param[0])
        self.params = []
    
    # dekorator pre vykreslenie utvaru, resp. vratenie suradnic utvaru
    # pre hypoteticke suradnice
    def vykresli_dekorator(vykresli_func):
        def wrapper(*args, **kwargs):
            self, buduce_suradnice, suradnice = vykresli_func(*args, **kwargs)
            
            if buduce_suradnice is None:
                self.zmaz()
                for x1, y1, x2, y2 in suradnice:
                    self.params.append((canvas.create_rectangle(x1, y1, x2, y2, fill=self.farba), (x1, y1, x2, y2)))
            else:
                return suradnice
        
        return wrapper
        
##############################################################################
########### Nasleduju definicie utvarov, ako triedy ##########################
##############################################################################
        
class Stvorec(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                x1 = x0 + (s - 3)*self.d
                y1 = y0 + (r - 3)*self.d
                
                x2 = x0 + (s - 2)*self.d
                y2 = y0 + (r - 2)*self.d
                suradnice.append((x1, y1, x2, y2))
        
        return self, buduce_suradnice, suradnice
        
class Hacko1(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                if r in (2, 3) or s in (0, 1, 4, 5):
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
        
        return self, buduce_suradnice, suradnice
        
class Hacko2(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                if r in (0, 1, 4, 5) or s in (2, 3):
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
        
        return self, buduce_suradnice, suradnice
        
class Plusko(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                if r in (2, 3) or s in (2, 3):
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                
        
        return self, buduce_suradnice, suradnice
        
class Sliz1(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                if r in (2, 3):
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                
        
        return self, buduce_suradnice, suradnice

class Sliz2(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                if s in (2, 3): 
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
        
        return self, buduce_suradnice, suradnice
        
class Uhol1(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        if x0 != self.x0 and y0 != self.y0:
            x0 += 2*self.d
            y0 -= 2*self.d
            
        suradnice = []
        for r in range(6):
            for s in range(6):
                if s in (0, 1) or r in (4, 5): 
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                
        return self, buduce_suradnice, suradnice
        
class Uhol2(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        if x0 != self.x0 and y0 != self.y0:
            x0 -= 2*self.d
            y0 -= 2*self.d
        
        suradnice = []
        for r in range(6):
            for s in range(6):
                if s in (4, 5) or r in (4, 5): 
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                
        return self, buduce_suradnice, suradnice
        
class Uhol3(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        if x0 != self.x0 and y0 != self.y0:
            x0 -= 2*self.d
            y0 += 2*self.d
        
        suradnice = []
        for r in range(6):
            for s in range(6):
                if s in (4, 5) or r in (0, 1): 
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                
        return self, buduce_suradnice, suradnice
        
class Uhol4(Utvar):

    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        if x0 != self.x0 and y0 != self.y0:
            x0 += 2*self.d
            y0 += 2*self.d
        
        suradnice = []
        for r in range(6):
            for s in range(6):
                if s in (0, 1) or r in (0, 1): 
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                
        return self, buduce_suradnice, suradnice

class Tecko1(Utvar):
    
    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                if s in (0, 1) or r in (2, 3): 
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                    
        return self, buduce_suradnice, suradnice
        
class Tecko2(Utvar):
    
    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                if s in (2, 3) or r in (4, 5): 
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                    
        return self, buduce_suradnice, suradnice   
        
class Tecko3(Utvar):
    
    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                if s in (4, 5) or r in (2, 3): 
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                    
        return self, buduce_suradnice, suradnice
        
class Tecko4(Utvar):
    
    def __init__(self, d):
        super().__init__()
        self.d = d
        self.vykresli(self.x0, self.y0)
        
    @Utvar.vykresli_dekorator    
    def vykresli(self, x0, y0, buduce_suradnice=None):
        suradnice = []
        for r in range(6):
            for s in range(6):
                if s in (2, 3) or r in (0, 1): 
                    x1 = x0 + (s - 3)*self.d
                    y1 = y0 + (r - 3)*self.d
                    
                    x2 = x0 + (s - 2)*self.d
                    y2 = y0 + (r - 2)*self.d
                    if (x1, y1, x2, y2) not in suradnice:
                        suradnice.append((x1, y1, x2, y2))
                    
        return self, buduce_suradnice, suradnice  
        
##############################################################################
########### Koniec definicii utvarov #########################################
##############################################################################
        
class Tetris2:
    
    def __init__(self):
        
        # pociatocne suradnice hernej plochy
        self.x0 = 25 
        self.y0 = 100
        
        self.d = 24 # strana stvoceka hernej plochy
        self.pocet_r = 20 # pocet riadkov hernej plochy
        self.pocet_s = 20 # pocet riadkov hernej plochy
        self.obsadene_polia = {} # ako kluce su suradnice objektov a 
                                 # hodnoty su idcka objektov, ktore su na hracej ploche,
                                 # obsadene polia na hracej ploche
        
        self.stvorce_siete_s = [] # suradnice stvorcov siete hernej plochy po stlpcoch
        self.stvorce_siete_r = [] # suradnice stvorcov siete hernej plochy po riadkoch
        
        self.pocet_stvorcov_na_zmazanie = 20  # pocet stvorcov z utvarov na ploche za sebou 
                                              # ktore sa vymazu z hernej plochy
        self.score = 0 # skore nadobudnute
        self.delta_score = 5 # pridavok ku skore za kazdy vymazany stvorcek
        
        # Vykreslenie score
        self.id_score = canvas.create_text((self.x0 + self.pocet_s * self.d)//2, 50, 
                                            text='Score: 0', font='Arial 18')
        # Copyright
        canvas.create_text((self.x0 + self.pocet_s * self.d)//2, 800, 
                            text = "© 2026, Norbert Jankura, nr.jankura@gmail.com", font="Arial 13")
        
        # Oramovanie hernej plochy
        canvas.create_rectangle(self.x0, self.y0, 
                                self.x0 + self.pocet_s*self.d, self.y0 + self.pocet_r*self.d)
        
        # Stvorce siete zoradene do jednej premennej po stlpcoch
        for r in range(self.pocet_r):
            for s in range(self.pocet_s):
                x1 = self.x0 + s*self.d
                y1 = self.y0 + r*self.d
                
                x2 = self.x0 + (s + 1)*self.d
                y2 = self.y0 + (r + 1)*self.d
                
                # suradnice vsetkych stvorcov hernej plochy (siete)
                # zoradenych v radoch po stlpcoch
                self.stvorce_siete_s.append((x1, y1, x2, y2))
                
                # vykreslenie siete hernej plochy
                #canvas.create_rectangle(x1, y1, x2, y2)
                
        # Stvorce siete zoradene do jednej premennej po riadkoch
        for s in range(self.pocet_s):
            for r in range(self.pocet_r):
                x1 = self.x0 + s*self.d
                y1 = self.y0 + r*self.d
                
                x2 = self.x0 + (s + 1)*self.d
                y2 = self.y0 + (r + 1)*self.d
                
                # suradnice vsetkych stvorcov hernej plochy (siete)
                # zoradenych v radoch po riadkoch
                self.stvorce_siete_r.append((x1, y1, x2, y2))
                
        self.nacitaj_dalsi_utvar()
        
        self.uchopeny_utvar = False
        
        canvas.bind('<ButtonPress>', self.uchop_utvar)
        canvas.bind("<B1-Motion>", self.presun_utvar)
        canvas.bind("<ButtonRelease>", self.pusti_utvar)
        canvas.unbind_all("<space>")
        
    # Vytvori objekt nahodneho utvaru
    def nacitaj_dalsi_utvar(self):
        utvary = [
                    #Stvorec, 
                    Hacko1,
                    Hacko2, 
                    Plusko, 
                    Sliz1, 
                    Sliz2,
                    Uhol1,
                    Uhol2,
                    Uhol3,
                    Uhol4,
                    Tecko1,
                    Tecko2,
                    Tecko3,
                    Tecko4
                 ]
                 
        #self.utvar = Hacko2(self.d)
        self.utvar = random.choice(utvary)(self.d)
        #self.utvar = random.choice((Hacko1, Hacko2))(self.d)
        
    def uchop_utvar(self, event):
        if self.utvar is not None:
            for id, (x1, y1, x2, y2) in self.utvar.params:
                if x1 <= event.x <= x2 and y1 <= event.y <= y2:
                    self.utvar.vykresli(event.x, event.y)
                    self.uchopeny_utvar = True
                    break
        
    def presun_utvar(self, event):
        if self.uchopeny_utvar and self.utvar is not None:
            self.utvar.vykresli(event.x, event.y)
    
    def pusti_utvar(self, event):
        if self.uchopeny_utvar and self.utvar is not None:
            self.umiestneny = True
            self.umiestni_na_siet(event)
            
            if self.umiestneny:
                self.skontroluj_siet()
                self.nacitaj_dalsi_utvar()
                self.je_este_mozne_pridat_na_siet()
            else:
                self.vrat_utvar_na_miesto()
                
            self.uchopeny_utvar = False
    
    def vrat_utvar_na_miesto(self):
        self.utvar.zmaz()
        self.utvar.vykresli(self.utvar.x0, self.utvar.y0)
    
    # Umiestni utvar na siet hernej plochy
    def umiestni_na_siet(self, event):
        x, y = None, None
        for x1, y1, x2, y2 in self.stvorce_siete_s:
            # Ak je x a y suradnica utvaru v konkretnom stvorci (x1, y1, x2, y2)
            # zacni umiestnovat
            if x1 <= event.x < x2 and y1 <= event.y < y2:
                # stred stvorca v ktorom su suradnice utvaru
                stred_stvorca = (round(x1 + 0.5*self.d), round(y1 + 0.5*self.d))
                
                # rozdelenie stvorca v ktorom su suradnice utvaru
                # na styri podstvorce
                stvorec_00 = x1, y1, stred_stvorca[0], stred_stvorca[1]
                stvorec_01 = stred_stvorca[0], y1, x2, stred_stvorca[1]
                stvorec_10 = x1, stred_stvorca[1], stred_stvorca[0], y2
                stvorec_11 = stred_stvorca[0], stred_stvorca[1], x2, y2
                
                # rozhodovanie v ktorom podstvorci su suradnice utvaru
                # a nasledne pridelenie suradnic na ktore sa umiestni
                # utvar
                if (stvorec_00[0] <= event.x <= stvorec_00[2] and 
                    stvorec_00[1] <= event.y <= stvorec_00[3]):
                    x, y = x1, y1
                if (stvorec_01[0] <= event.x <= stvorec_01[2] and 
                    stvorec_01[1] <= event.y <= stvorec_01[3]):
                    x, y = x2, y1
                if (stvorec_10[0] <= event.x <= stvorec_10[2] and 
                    stvorec_10[1] <= event.y <= stvorec_10[3]):
                    x, y = x1, y2
                if (stvorec_11[0] <= event.x <= stvorec_11[2] and 
                    stvorec_11[1] <= event.y <= stvorec_11[3]):
                    x, y = x2, y2
                
                # Ak je mozne vykreslit utvar na dane suradnice
                # vykresli ho ak nie vrat utvar na miesto
                if self.je_mozne_vykreslit(x, y):
                    self.utvar.vykresli(x, y)
                    for id, (xu1, yu1, xu2, yu2) in self.utvar.params:
                        self.obsadene_polia[(xu1, yu1, xu2, yu2)] = id
                    self.utvar = None
                else:
                    self.umiestneny = False
        
        # pripad ked utvar nie je umiestnovany na siet
        # teda je umiestnovany mimo siete hernej plochy
        if x is None: 
            self.umiestneny = False
    
    # Vracia True alebo False, podla toho ci je mozne 
    # utvar umiestnit na siet hernej plochy
    def je_mozne_vykreslit(self, x, y):
        # Kontrola ci je utvar umiestnovany na existujuce utvary
        # na hernej ploche
        for suradnice, id in self.obsadene_polia.items():
            if suradnice in self.utvar.vykresli(x, y, 1):
                return False
        
        # x - ova a y - ova hranica utvaru
        hranica_x_utvaru = 3*self.d        
        hranica_y_utvaru = 3*self.d        
        
        # Pripady utvarov ktore maju ine vlastnosti ako
        # standardne utvary
        if isinstance(self.utvar, Uhol1):
            x += 2*self.d
            y -= 2*self.d
        elif isinstance(self.utvar, Uhol2):
            x -= 2*self.d
            y -= 2*self.d
        elif isinstance(self.utvar, Uhol3):
            x -= 2*self.d
            y += 2*self.d
        elif isinstance(self.utvar, Uhol4):
            x += 2*self.d
            y += 2*self.d
        elif isinstance(self.utvar, Sliz1):
            hranica_y_utvaru = self.d
        elif isinstance(self.utvar, Sliz2):
            hranica_x_utvaru = self.d
        
        # Kontrola ci je utvar celou svojou plochou 
        # umiestnovany na hernu plochu alebo presahuje
        # hernu plochu, ak presahuje vrati False
        if (y - hranica_y_utvaru >= self.y0 and 
            y + hranica_y_utvaru <= self.y0 + self.pocet_r * self.d and
            x - hranica_x_utvaru >= self.x0 and
            x + hranica_x_utvaru <= self.x0 + self.pocet_s * self.d
            ):
            return True
        else:
            return False
    
    def skontroluj_siet(self):
        # kontrola ci su nejake dvojice riadkov hernej plochy vyplnene
        # objektami v pozadovanom pocte, ak ano zaznamena ich do stvorce_na_zmazanie
        stvorce_za_sebou = []
        posledny_stlpec = -1
        stvorce_na_zmazanie = []
        druhy = []
        for poradie, (x1, y1, x2, y2) in enumerate(self.stvorce_siete_s):
            stlpec = poradie%self.pocet_s
            
            if posledny_stlpec != stlpec - 1:
                if len(stvorce_za_sebou) > self.pocet_stvorcov_na_zmazanie:
                    stvorce_na_zmazanie.append(stvorce_za_sebou)
                stvorce_za_sebou = []
                druhy = []
                
            if ((x1, y1, x2, y2) in self.obsadene_polia and 
                (x1, y1 + self.d, x2, y2 + self.d) in self.obsadene_polia and
                (x1, y1, x2, y2) not in druhy):
                stvorce_za_sebou.append((self.obsadene_polia[(x1, y1, x2, y2)], (x1, y1, x2, y2)))
                stvorce_za_sebou.append((self.obsadene_polia[(x1, y1 + self.d, x2, y2 + self.d)], 
                                                                (x1, y1 + self.d, x2, y2 + self.d)))
                druhy.append((x1, y1 + self.d, x2, y2 + self.d))
                posledny_stlpec = stlpec
                
        if len(stvorce_za_sebou) > self.pocet_stvorcov_na_zmazanie:
            stvorce_na_zmazanie.append(stvorce_za_sebou)
        
        # kontrola ci su nejake dvojice stlpcov hernej plochy vyplnene
        # objektami v pozadovanom pocte, ak ano zaznamena ich do stvorce_na_zmazanie
        stvorce_za_sebou = []
        posledny_riadok = -1 
        druhy = []
        for poradie, (x1, y1, x2, y2) in enumerate(self.stvorce_siete_r):
            riadok = poradie%self.pocet_r
            
            if posledny_riadok != riadok - 1:
                if len(stvorce_za_sebou) > self.pocet_stvorcov_na_zmazanie:
                    stvorce_na_zmazanie.append(stvorce_za_sebou)
                stvorce_za_sebou = []
                druhy = []
                
            if ((x1, y1, x2, y2) in self.obsadene_polia and 
                (x2, y1, x2 + self.d, y2) in self.obsadene_polia and
                (x1, y1, x2, y2) not in druhy):
                   
                stvorce_za_sebou.append((self.obsadene_polia[(x1, y1, x2, y2)], (x1, y1, x2, y2)))
                stvorce_za_sebou.append((self.obsadene_polia[(x2, y1, x2 + self.d, y2)], 
                                                                (x2, y1, x2 + self.d, y2)))
                druhy.append((x2, y1, x2 + self.d, y2))
                posledny_riadok = riadok
                
        if len(stvorce_za_sebou) > self.pocet_stvorcov_na_zmazanie:
            stvorce_na_zmazanie.append(stvorce_za_sebou)
        
        # vymaz z hernej site stvorce ktore su za sebou v pozadovanom 
        # pocte ci uz v stlpcoch alebo v riadkoch po dvojiciach
        if stvorce_na_zmazanie != []:
            self.zmaz_zo_siete_stvorce(stvorce_na_zmazanie)
    
    # funkcia na zmazanie stvorcov zo siete
    def zmaz_zo_siete_stvorce(self, stvorce_na_zmazanie):
        self.animuj(stvorce_na_zmazanie)
        for stvorce in stvorce_na_zmazanie:    
            for id, (x1, y1, x2, y2) in stvorce:
                if (x1, y1, x2, y2) in self.obsadene_polia:
                    # zmazanie stvorcov animovane
                    self.obsadene_polia.pop((x1, y1, x2, y2)) 
                    canvas.delete(id)
                    
                    # animovany upadate score
                    self.score += self.delta_score
                    canvas.itemconfig(self.id_score, text=f'Score: {self.score}')
                    canvas.update()
                    canvas.after(20)
    
    # funkcia ktora zablika stvorcami ktore sa vymazu                
    def animuj(self, stvorce_na_zmazanie, poc=0, farby=['grey', 'lightgrey']):
        while poc < 4:
            poc += 1
            farby.append(farby.pop(0))
            for stvorec in stvorce_na_zmazanie:
                for id, (x1, y1, x2, y2) in stvorec:
                    canvas.itemconfig(id, fill = farby[0])
            canvas.update()
            canvas.after(200)
    
    # Kontrola ci je este mozne pridat novovytvoreny utvar na siet
    # hernej plochy
    def je_este_mozne_pridat_na_siet(self):
        je_mozne = False
        for poradie, (x1, y1, x2, y2) in enumerate(self.stvorce_siete_s):
            if self.je_mozne_vykreslit(x1, y1):
                je_mozne = True
                break
        
        if not je_mozne:
            # ak nie je mozne vykreslit tak zrus akcie mysi
            canvas.unbind('<ButtonPress>')
            canvas.unbind("<B1-Motion>")
            canvas.unbind("<ButtonRelease>")
            
            # Na stlacenie medzernika spusti hru odznova
            canvas.bind_all("<space>", self.odznova) 
            canvas.create_text((self.x0 + self.pocet_s * self.d)//2, 20, 
                                            text='Stlac medzernik', font='Arial 18')
            canvas.create_text((self.x0 + self.pocet_s * self.d)//2,
                               (self.y0 + self.pocet_r*self.d)//2, 
                                            text='Koniec', font='Arial 30') 
    # funkcia ktora spusta hru odznova
    def odznova(self, *arg):
        canvas.delete('all')
        self.__init__()
        
        
win = tkinter.Tk()

canvas = tkinter.Canvas(win, width=550, height=820)
canvas.pack()


Tetris2()


tkinter.mainloop()