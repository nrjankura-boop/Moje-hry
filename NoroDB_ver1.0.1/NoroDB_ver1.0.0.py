import re, os, shutil, math, time
from decimal import localcontext, Decimal

# globalne premenne
used_database = ''

KEYWORDS = {
            'USE',
            'CREATE',
            'DROP',
            'DATABASE',
            'TABLE',
            'SELECT',
            'FROM',
            'INSERT',
            'INTO',
            'VALUES',
        }
        
KEYWORDS_TYPES = {
            'TEXT',
            'INT',
            'DEC',
        }
        
class NoroDBException(Exception): pass

# funkcia na vyhladanie nastavenia v NoroDB.ini
def najdi_nastavenie(nazov_nastavenia):
    with open('NoroDB.ini', 'r') as f:
        for line in f:
            line = line.strip()
            rovnica = re.split("\s*=\s*", line)
            if rovnica[0].upper() == nazov_nastavenia:
                if rovnica[1][-1] != '/' or rovnica[1][-1] != '\\': rovnica[1] += '/'
                if rovnica[1][-1] == '\\': rovnica[1][-1] = '/'
                return rovnica[1]

# Preveri ci bola vybrata databaza a vrati cestu k tabulke
def vrat_cestu_k_tabulke():
    if used_database != '':
        cesta_k_tabulke = najdi_nastavenie("CESTA_K_DATABAZAM") + used_database + '/'
    else:
        raise NoroDBException('Nebola vybrana databaza!')
    return cesta_k_tabulke

# Vrati hlavicku tabulky
def nacitaj_hlavicku_tabulky(subor):
    with open(subor, 'rb') as f:
        koniec_hlavicky = 0
        pb = f.read(1)
        nazov_tabulky = f.read(pb[0]).decode('utf-8')
        pocet_stlpcov = int.from_bytes(f.read(1)) + 1
        stlpce = []
        typy_stlpcov = ('TEXT', 'INT', 'DEC')
        typy_stlpcov2 = ('RETAZEC', 'CISLO', 'CISLO')
        koniec_hlavicky += 2 + pb[0]
        for _ in range(pocet_stlpcov):
            pb = f.read(1)
            
            koniec_hlavicky += 1
            
            meno_stlpca = f.read(pb[0]).decode('utf-8')
            typ_stlpca = int.from_bytes(f.read(1))
            
            koniec_hlavicky += 1 + pb[0]
            
            dlzka_v_bytoch = []
            for _ in range(typ_stlpca):
                dlzka_v_bytoch.append(int.from_bytes(f.read(1)))
                koniec_hlavicky += 1
                
            dlzka = []
            for _ in range(typ_stlpca):
                pb = f.read(1)
                koniec_hlavicky += 1
                dlzka.append(int.from_bytes(f.read(pb[0]), 'big'))
                koniec_hlavicky += pb[0]
            typ_stlpca = typy_stlpcov[typ_stlpca], typy_stlpcov2[typ_stlpca], typ_stlpca
            
            stlpce.append({
                'meno_stlpca': meno_stlpca,
                'typ_stlpca': typ_stlpca,
                'dlzka': dlzka,
                'dlzka_v_bytoch': dlzka_v_bytoch
            })
            
    return nazov_tabulky, pocet_stlpcov, stlpce, koniec_hlavicky
    
# funkcia ktora vrati pocet bytov zo zadaneho cisla                
def pocet_bytov(cislo):
    pb = 0
    while cislo > 0:
        cislo //= 256
        pb += 1
    return pb

# Nasledovne dve funkcie sluzia na zoradenie pola podla ineho pola
# pomocou zoznamu indexov
def zorad_pole(pole, zoz_indexov, reverse=False):
            return [val for (_, val) in sorted(zip(zoz_indexov, pole), key=lambda x: x[0], reverse=reverse)]
            
def vrat_zoz_indexov(pole, podla_pola):
    return [j for i, prvok1 in enumerate(pole) for j, prvok2 in enumerate(podla_pola) if prvok1 == prvok2]
    
################################################################    

# Hlavna trieda ktorej vstupom je retazec pozostavajuci
# z niekolkych dotazov ktore su oddelene ';' bodkociarkou    
class Dotaz:
    
    def __init__(self, dotaz):
        self.dotaz = dotaz
        self.vytvor_prikazy()
        self.vykonaj()
    
    # rozparsuje dotazy na jednotlive prikazy
    def vytvor_prikazy(self):
        
        token_specification = [
            #('NUMBER',   r'\d+(\.\d*)?'),  # Integer or decimal number
            #('ASSIGN',   r':='),           # Assignment operator
            ('KONIEC',      r';'),            # Statement terminator
            #('ID',       r'[A-Za-z]+'),    # Identifiers
            ('NAZOV',       r'[A-Za-z_]+[A-Za-z0-9_]+'),    # nazov 
            #('RETAZEC',       r"(?P<quote>['\"])((?:\\.|(?!(?P=quote)).)*)(?P=quote)"),    # Retazec
            ('RETAZEC',       r"(?P<quote>['\"])(?P=quote)(\n|.)+?(?P=quote)(?P=quote)"),    # Retazec
            #('CISLO',   r'[\+-]?\d+([\.,]\d*)?(?!\w)'),  # Integer number or decimal number
            ('CISLO',   r'[\+-]?\d+(([\.,]\d*)?([eE][\+-]?\d*)?)?(?!\w)'),  # Integer number or decimal number
            #('OP',       r'[+\-*/]'),      # Arithmetic operators
            ('STLPCE',       r'[*]'),      # Vyber vsetky stlpce
            ('NOVYRIADOK',  r'\n'),           # Line endings
            ('PRESKOC',     r'[ \t]+'),       # Skip over spaces and tabs
            ('COMMENT',     r'#.*\n?'),       # Skip comment
            ('NENASIEL', r'.'),            # Any other character
        ]
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in token_specification)
        
        line_num = 1
        line_start = 0
        self.prikazy = []
        dotaz = 0
        self.prikazy.append([])
        for mo in re.finditer(tok_regex, self.dotaz):
            kind = mo.lastgroup
            value = mo.group()
            column = mo.start() - line_start
            
            if kind == 'NAZOV' and value.upper() in KEYWORDS:
                kind = "PRIKAZ"
                value = value.upper()
            elif kind == 'NAZOV' and value.upper() in KEYWORDS_TYPES:
                kind = "TYP"
                value = value.upper()
            elif kind == 'NAZOV':
                kind = 'NAZOV'
            elif kind == 'RETAZEC':
                value = value[2:-2]
            elif kind == 'CISLO':
                value = re.sub(",", ".", value)
                poz_des_bodky = value.find(".")
                pocet_des_miest = None
                if poz_des_bodky != -1 and 'e' not in value and 'E' not in value: 
                    pocet_des_miest = len(value[poz_des_bodky+1:])
                elif 'e' in value or 'E' in value:
                    poz_e = value.find('e')
                    if poz_e == -1:
                        poz_e = value.find('E')
                    if poz_des_bodky != -1:
                        pocet_des_miest = len(value[poz_des_bodky+1:poz_e])
                        if value[poz_e+1] == '-':
                            pocet_des_miest += int(value[poz_e+2:])
                        elif value[poz_e+1] == '+':
                            if pocet_des_miest > int(value[poz_e+2:]):
                                pocet_des_miest -= int(value[poz_e+2:])
                            else:
                                pocet_des_miest = None
                        else:
                            if pocet_des_miest > int(value[poz_e+1:]):
                                pocet_des_miest -= int(value[poz_e+1:])
                            else:
                                pocet_des_miest = None
                    else:
                        if value[poz_e+1] == '-':
                            pocet_des_miest = int(value[poz_e+2:])
                    
                if pocet_des_miest is not None:
                    with localcontext() as ctx:
                        ctx.prec = pocet_des_miest
                        value = Decimal(value)
                else:
                    value = int(format(float(value), 'f').rstrip('0').rstrip('.'))
                
                #value = float(value) if '.' in value else int(value)
                #print(f'{value!r}')
                #value = int(value)
            elif kind == 'STLPCE':
                pass
            elif kind == 'KONIEC':
                dotaz += 1
                self.prikazy.append([])
                continue
            elif kind == 'NOVYRIADOK':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'PRESKOC':
                continue
            elif kind == 'COMMENT':
                line_start = mo.end()
                line_num += 1
                continue
            elif kind == 'NENASIEL':
                raise NoroDBException(RuntimeError(f'{value!r} neocakavane na riadku {line_num} v stlpci {column}'))
            
            self.prikazy[dotaz].append({
                "value": value,
                "typ" : kind,
                "line_num": line_num,
                "column": column
            })
        
        if self.prikazy[-1] == []: self.prikazy.pop()
        
        #self.dump_prikazov()
    
    # Vypis dotazov a ich jednotlivych prikazov (poloziek) na obrazovku
    # Sluzi iba na kontrolu
    def dump_prikazov(self):
        for dotaz in range(len(self.prikazy)):
            print(str(dotaz + 1) + '. dotaz:')
            for slovnik in self.prikazy[dotaz]: 
                hodnota = slovnik['value']
                typ = slovnik['typ']
                cislo_riadka = slovnik['line_num']
                stlpec = slovnik['column']
                print(f'hodnota: {hodnota:<20} typ: {typ:8} cislo riadka: {cislo_riadka:<5} stlpec: {stlpec:<5}')
    
    # vykona postupne jeden dotaz za druhym
    def vykonaj(self):
        for dotaz in range(len(self.prikazy)):
            rad_prikazov = []
            rad_prikazov_s_typmi = []
            for prikaz in self.prikazy[dotaz]:
                rad_prikazov.append(prikaz['value'])
                rad_prikazov_s_typmi.append((prikaz['value'], prikaz['typ'], prikaz['line_num'], prikaz['column']))
            
            if rad_prikazov[0] == 'CREATE':
                Create(rad_prikazov[1:], rad_prikazov_s_typmi[1:])
            elif rad_prikazov[0] == 'DROP':
                Drop(rad_prikazov[1:], rad_prikazov_s_typmi[1:])
            elif (  rad_prikazov[0] == 'USE' and 
                    len(rad_prikazov) == 3 and 
                    rad_prikazov[1] == 'DATABASE' and 
                    rad_prikazov_s_typmi[2][1] == 'NAZOV'
                 ):
                if os.path.exists(najdi_nastavenie("CESTA_K_DATABAZAM") + rad_prikazov[2]):
                    global used_database
                    used_database = rad_prikazov[2]
                else:
                    raise NoroDBException('Databaza >>' + rad_prikazov[2] + '<< neexistuje.')
            elif rad_prikazov[0] == 'INSERT' and rad_prikazov[1] == 'INTO':
                Insert(rad_prikazov[2:], rad_prikazov_s_typmi[2:])
            elif rad_prikazov[0] == 'SELECT':
                Select(rad_prikazov[1:], rad_prikazov_s_typmi[1:])
            else:
                raise NoroDBException('Dotaz na riadku ' + str(rad_prikazov_s_typmi[0][2]) + 
                                      ' nie je v poriadku!'
                                      )
# Trieda pre dotazy CREATE
class Create:
    
    def __init__(self, prikazy, prikazy_s_typmi):
        self.prikazy = prikazy
        self.prikazy_s_typmi = prikazy_s_typmi
        self.prever_prikazy()
        self.vykonaj()
    
    # preveri prikazy v dotaze, ci je dotaz v poriadku
    def prever_prikazy(self):
        if self.prikazy[0] == "DATABASE":
            # Preveri ci je za USE DATABASE meno_databazy dana bodkociarka.
            if len(self.prikazy) > 2:
                raise NoroDBException('Dotaz na riadku ' + 
                                       str(self.prikazy_s_typmi[0][2]) + 
                                     ' nie je v poriadku!')
            # Preveri ci je treti retazec v dotaze nazov databazy a nie 
            # niektory z keywords ...
            if self.prikazy_s_typmi[1][1] != "NAZOV":
                raise NoroDBException('Meno databazy >>' + self.prikazy_s_typmi[1][0] + '<< nie je dovolene.')
        elif self.prikazy[0] == "TABLE":
            # Preveri ci je nazov tabulky spravny a nie niektory z keywords ...
            if self.prikazy_s_typmi[1][1] != "NAZOV":
                raise NoroDBException("Meno tabulky >>" + self.prikazy_s_typmi[1][0] + '<< nie je dovolene.')
            
            prikazy_s_typmi = self.prikazy_s_typmi[2:]
            
            # preveri ci je aspon jeden stlpec v dotaze
            if len(prikazy_s_typmi) == 0:
                raise NoroDBException('Chyba! Dotaz pre vytvorenie tabulky neobsahuje ziadne stlpce!')
            
            # Preveri ci je niektory z nazvov stlpcov
            # tabulky pouzity viackrat ak ano vyhlasi chybu
            slovnik_poctov = {}
            for hodnota, typ, line_num, column in prikazy_s_typmi:
                if typ == "NAZOV":
                    if hodnota not in slovnik_poctov:
                        slovnik_poctov[hodnota] = 1
                    else:
                        slovnik_poctov[hodnota] += 1
            for meno_stlpca, pocet in slovnik_poctov.items():
                if pocet > 1:
                    raise NoroDBException('Chyba! Meno stlpca >>'
                                            + meno_stlpca + '<< je v dotaze '
                                            + str(pocet) + " krat.")
                
            # Preveri ci su deklaracie stlpcov v dotaze v poriadku    
            stlpec = ["NAZOV", "TYP", "CISLO"]
            i = 0            
            while i < len(prikazy_s_typmi):
                if ( i + 1 >= len(prikazy_s_typmi) or
                    i + 2 >= len(prikazy_s_typmi) and prikazy_s_typmi[i+1][0] != 'TEXT'
                    ):
                    raise NoroDBException("Chyba na konci dotazu!")
                for j in range(3):
                    if j == 1 and prikazy_s_typmi[i+1][0] == 'TEXT':
                        i -= 1
                        break
                    
                    if prikazy_s_typmi[i+j][1] != stlpec[j]:
                        raise NoroDBException("Chyba na riadku " + str(prikazy_s_typmi[i+j][2]) 
                                                + " v stlpci " + str(prikazy_s_typmi[i+j][3])
                                                + "! Hodnota >>" + str(prikazy_s_typmi[i+j][0])
                                                + "<< nie je na spravnom mieste.")
                    
                    if (    prikazy_s_typmi[i+j][1] == 'CISLO' and 
                            isinstance(prikazy_s_typmi[i+j][0], float)
                       ):                            
                        raise NoroDBException("Chyba na riadku " + str(prikazy_s_typmi[i+j][2]) 
                                                + " v stlpci " + str(prikazy_s_typmi[i+j][3])
                                                + "! Hodnota >>" + str(prikazy_s_typmi[i+j][0])
                                                + "<< ma byt cele cislo.")
                                     
                if prikazy_s_typmi[i+1][0] == "DEC":
                    if i + 3 >= len(prikazy_s_typmi):
                        raise NoroDBException("Chyba na konci dotazu!")
                    i += 1
                    if prikazy_s_typmi[i+2][1] != "CISLO":
                        raise NoroDBException("Chyba! Hodnota poctu desatinnych miest pre stlpec >>" 
                                                + prikazy_s_typmi[i-1][0] + "<< je zle zadana. Chybna hodnota >>" 
                                                + prikazy_s_typmi[i+2][0]
                                                + "<< na riadku "
                                                + str(prikazy_s_typmi[i+2][2]) + " a stlpci "
                                                + str(prikazy_s_typmi[i+2][3]) + "."
                                              )
                    elif (  prikazy_s_typmi[i+2][1] == 'CISLO' and 
                            isinstance(prikazy_s_typmi[i+2][0], Decimal)
                         ):                            
                        raise NoroDBException("Chyba na riadku " + str(prikazy_s_typmi[i+2][2]) 
                                                + " v stlpci " + str(prikazy_s_typmi[i+2][3])
                                                + "! Hodnota >>" + str(prikazy_s_typmi[i+2][0])
                                                + "<< ma byt cele cislo.")
                i += 3
        else:
            raise NoroDBException('Dotaz na riadku ' + 
                                    str(self. prikazy_s_typmi[0][2]) + ' nie je v poriadku!')   
    # Vykona dotazy CREATE
    def vykonaj(self):
        if self.prikazy[0] == "DATABASE":
            self.create_database()
        elif self.prikazy[0] == "TABLE":
            self.create_table()
    
    # Vykona dotaz CREATE DATABASE meno_databazy        
    def create_database(self):
        cesta = najdi_nastavenie("CESTA_K_DATABAZAM")
        try:
            os.mkdir(cesta + self.prikazy[1])
            print("Databaza " + self.prikazy[1] + " bola vytvorena.")   
        except:
            raise NoroDBException("\n\n Databaza nebola vytvorena. \n\n")
    
    # Vykona dotaz CREATE TABLE ...        
    def create_table(self):
        self.meno_tabulky = self.prikazy[1]
        self.nacitaj_stlpce()
        self.vytvor_tabulku()
    
    # Nacita stlpce do premennej self.stlpce z
    # prikazov vytvorenych v Dotaz.vytvor_prikazy()
    def nacitaj_stlpce(self):
        self.stlpce = []
        meno_stlpca = None
        for hodnota, typ, line_num, column in self.prikazy_s_typmi[2:]:
            if typ == 'NAZOV':
                if meno_stlpca is not None:
                    self.stlpce.append({
                        'meno_stlpca': meno_stlpca,
                        'typ_stlpca': typ_stlpca,
                        'dlzka': dlzka
                    })
                dlzka = []
                meno_stlpca = hodnota
            elif typ == 'TYP':
                typ_stlpca = hodnota
            elif typ == 'CISLO':
                dlzka.append(hodnota)
                
        self.stlpce.append({
            'meno_stlpca': meno_stlpca,
            'typ_stlpca': typ_stlpca,
            'dlzka': dlzka
        })
    
    # Vytvori subor tabulky meno_tabulky.ndb
    # s hlavickou ktoru tvoria meno tabulky, 
    # pocet_stlpcov ako jeden byte (teda maximum 256 stlpcov) a 
    # jednotlive stlpce s ich typmi a velkostami
    def vytvor_tabulku(self):
        bin_meno_tabulky = bytes(self.meno_tabulky, 'utf-8')
        pb_meno_tabulky = len(bin_meno_tabulky).to_bytes(1)
        pocet_stlpcov = (len(self.stlpce) - 1).to_bytes(1)
        bin_data = pb_meno_tabulky + bin_meno_tabulky + pocet_stlpcov
        for stlpec_def in self.stlpce:
            meno = bytes(stlpec_def['meno_stlpca'], 'utf-8')
            bin_data += len(meno).to_bytes(1) + meno
            if stlpec_def['typ_stlpca'] == 'TEXT':
                bin_data += b'\x00'
            elif stlpec_def['typ_stlpca'] == 'INT':
                bin_data += b'\x01'
                bin_data += pocet_bytov(10 ** stlpec_def['dlzka'][0] - 1).to_bytes(1)
                pb_dlzka = pocet_bytov(stlpec_def['dlzka'][0])
                bin_data += pb_dlzka.to_bytes(1)
                bin_data += stlpec_def['dlzka'][0].to_bytes(pb_dlzka, 'big')
            elif stlpec_def['typ_stlpca'] == 'DEC':
                bin_data += b'\x02'
                bin_data += pocet_bytov(10 ** stlpec_def['dlzka'][0] - 1).to_bytes(1)
                bin_data += pocet_bytov(10 ** stlpec_def['dlzka'][1] - 1).to_bytes(1)
                pb_dlzka1 = pocet_bytov(stlpec_def['dlzka'][0])
                bin_data += pb_dlzka1.to_bytes(1) + stlpec_def['dlzka'][0].to_bytes(pb_dlzka1, 'big')
                pb_dlzka2 = pocet_bytov(stlpec_def['dlzka'][1])
                bin_data += pb_dlzka2.to_bytes(1) + stlpec_def['dlzka'][1].to_bytes(pb_dlzka2, 'big')
                
        # Preveri ci bola vybrata databaza a vrati cestu k tabulke
        cesta_k_tabulke = vrat_cestu_k_tabulke()
        
        subor = cesta_k_tabulke + self.meno_tabulky + '.ndb'
        if not os.path.isfile(subor):
            with open(subor, 'wb') as f:
                f.write(bin_data)
        else:
            raise NoroDBException('Tabulka s menom >>' + 
                                   self.meno_tabulky + 
                                   '<< uz existuje a preto nebola vytvorena!'
                                  )

# Trieda pre zmazanie databazy a tabulky
class Drop():
    
    def __init__(self, rad_prikazov, rad_prikazov_s_typmi):
        self.rad_prikazov = rad_prikazov
        self.rad_prikazov_s_typmi = rad_prikazov_s_typmi
        self.prever_prikazy()
        self.vykonaj()
    
    def prever_prikazy(self):
        if self.rad_prikazov[0] == 'DATABASE':
            # Preveri ci je za DROP DATABASE meno_databazy dana bodkociarka.
            if len(self.rad_prikazov) > 2:
                raise NoroDBException('Dotaz na riadku ' + 
                                       str(self.rad_prikazov_s_typmi[0][2]) + 
                                     ' nie je v poriadku!')
            # Preveri ci je treti retazec v dotaze nazov databazy a nie 
            # niektory z keywords ...
            if self.rad_prikazov_s_typmi[1][1] != "NAZOV":
                raise NoroDBException('Meno databazy >>' + self.rad_prikazov_s_typmi[1][0] + '<< nie je dovolene.')
            
            if not os.path.exists(najdi_nastavenie("CESTA_K_DATABAZAM") + self.rad_prikazov[1]):
                raise NoroDBException('Databaza >>' + self.rad_prikazov[1] + '<< neexistuje.')
        elif self.rad_prikazov[0] == 'TABLE':
            # Preveri ci je za DROP TABLE meno_tabulky dana bodkociarka.
            if len(self.rad_prikazov) > 2:
                raise NoroDBException('Dotaz na riadku ' + 
                                       str(self.rad_prikazov_s_typmi[0][2]) + 
                                     ' nie je v poriadku!')
            
            # Preveri ci je nazov tabulky spravny a nie niektory z keywords ...
            if self.rad_prikazov_s_typmi[1][1] != "NAZOV":
                raise NoroDBException("Meno tabulky >>" + self.rad_prikazov_s_typmi[1][0] + '<< nie je dovolene.')
            
            # Preveri ci bola vybrata databaza a vrati cestu k tabulke
            cesta_k_tabulke = vrat_cestu_k_tabulke()
            
            # Preveri ci existuje tabulka v danej databaze
            self.subor = cesta_k_tabulke + self.rad_prikazov[1] + '.ndb'
            if not os.path.isfile(self.subor):
                raise NoroDBException('Tabulka s menom >>' + self.rad_prikazov[1] + '<< neexistuje!')
        
            
    def vykonaj(self):
        if self.rad_prikazov[0] == 'DATABASE':
            shutil.rmtree(najdi_nastavenie("CESTA_K_DATABAZAM") + self.rad_prikazov[1])
        elif self.rad_prikazov[0] == 'TABLE':
            os.remove(najdi_nastavenie("CESTA_K_DATABAZAM") + used_database + '/' + self.rad_prikazov[1] + '.ndb')
            
            
# Trieda pre vkladanie riadkov do tabulky
class Insert:
    
    def __init__(self, rad_prikazov, rad_prikazov_s_typmi):
        self.rad_prikazov = rad_prikazov
        self.rad_prikazov_s_typmi = rad_prikazov_s_typmi
        self.prever_prikazy()
        self.vykonaj()
    
    def prever_prikazy(self):
        # Preveri ci bola vybrata databaza a vrati cestu k tabulke
        cesta_k_tabulke = vrat_cestu_k_tabulke()
        
        # Preveri ci existuje tabulka v danej databaze
        self.subor = cesta_k_tabulke + self.rad_prikazov[0] + '.ndb'
        if not os.path.isfile(self.subor):
            raise NoroDBException('Tabulka s menom >>' + self.rad_prikazov[0] + '<< neexistuje!')
        
        self.hlavicka = nacitaj_hlavicku_tabulky(self.subor)
        
        # Preveri ci je v dotaze VALUES
        try:
            self.koniec_mien_stlpcov = self.rad_prikazov.index("VALUES")
        except ValueError:
            raise NoroDBException("Dotaz na riadku " + 
                                    str(self.rad_prikazov_s_typmi[0][2]) + 
                                    " nie je v poriadku")
        
        # Preveri ci stlpce z dotazu su v tabulke
        for meno_stlpca_v_dotaze in self.rad_prikazov[1:self.koniec_mien_stlpcov]:
            existuje = False
            for stlpec_v_tabulke in self.hlavicka[2]:
                if stlpec_v_tabulke["meno_stlpca"] == meno_stlpca_v_dotaze:
                    existuje = True
                    break
            if existuje == False:
                raise NoroDBException('Chyba! V dotaze INSERT INTO na riadku ' + 
                                        str(self.rad_prikazov_s_typmi[0][2]) + 
                                         ". Stlpec s menom >>" + meno_stlpca_v_dotaze + 
                                         "<< sa nenachadza v tabulke!")
        
        # Preveri ci je niektory z nazvov stlpcov
        # v dotaze pouzity viackrat ak ano vyhlasi chybu
        slovnik_poctov = {}
        for hodnota in self.rad_prikazov[1:self.koniec_mien_stlpcov]:
            if hodnota not in slovnik_poctov:
                slovnik_poctov[hodnota] = 1
            else:
                slovnik_poctov[hodnota] += 1
        
        for meno_stlpca, pocet in slovnik_poctov.items():
            if pocet > 1:
                raise NoroDBException('Chyba na riadku ' + str(self.rad_prikazov_s_typmi[0][2]) 
                                        + '! Meno stlpca >>'
                                        + meno_stlpca + '<< je v dotaze '
                                        + str(pocet) + " krat.")
        
        # Preveri ci pocty stlpcov a pocty hodnot pre stlpce su rovnake
        if len(self.rad_prikazov[self.koniec_mien_stlpcov + 1:]) % (self.koniec_mien_stlpcov - 1) != 0:
            raise NoroDBException("Chyba! Pocet stlpcov a pocet zodpovedajucich hodnot pre stlpce sa lisi!")
        
        # Upravi data a stlpce z dotazu podla hlavicky tabulky
        # vrati self.hodnoty_s_typmi_pre_stlpce, chybajuce stlpce
        # nahradi s tuple (None, None, None, None)
        self.uprav_vstupy()
        
        # Preveri ci hodnoty pre stlpce su spravneho typu
        # Zaroven preveri aj to ci je dotaz spravne ukonceny bodkociarkou
        for poradie, (hodnota, typ, riadok, column) in enumerate(self.hodnoty_s_typmi_pre_stlpce):
            stlpec = self.hlavicka[2][poradie%len(self.hlavicka[2])]
            
            # Preveri ci typ hodnoty pre stlpec v dotaze je zhodny s typom stlpca v tabulke
            if stlpec['typ_stlpca'][1] != typ and typ is not None:
                raise NoroDBException("Chyba na riadku " + str(riadok) + 
                                        " v stlpci " + str(column) + 
                                        "! Typ stlpca >>" + stlpec['meno_stlpca'] + 
                                        "<< sa nezhoduje s typom zadanym v dotaze. Vami zadana hodnota " + 
                                        "pre tento stlpec je >>" + hodnota + "<< !"
                                    )
            # Preveri ci je cislo pre stlpec typu INT cele cislo                           
            if stlpec['typ_stlpca'][0] == 'INT':
                if isinstance(hodnota, Decimal):
                    raise NoroDBException("Chyba na riadku " + str(riadok) + 
                                        " v stlpci " + str(column) + 
                                        "! Zadana hodnota >>" + str(hodnota) + 
                                        "<< pre stlpec >>" + stlpec["meno_stlpca"] +
                                        "<< je desatinne cislo. Ma byt cele cislo!"                                        
                                            )
                                            
            # Preveri ci hodnota v dotaze pre stlpec, ktora je cislo,
            # ma pocet cifier celej a desatinnej casti rovnu alebo mensiu
            # ako je pocet cifier definovanych v tabulke
            if stlpec['typ_stlpca'][1] == "CISLO":
                if isinstance(hodnota, int):
                    if hodnota != 0:
                        pocet_cifier_hodnoty = int(math.log10(abs(hodnota))) + 1
                    else:
                        pocet_cifier_hodnoty = 1
                    
                    if pocet_cifier_hodnoty > stlpec['dlzka'][0]:
                        raise NoroDBException( "Chyba na riadku " + str(riadok) + 
                                                " v stlpci " + str(column) + 
                                                "! Pocet cifier cisla hodnoty >>" + str(hodnota)
                                                + "<< v dotaze je >>" + str(pocet_cifier_hodnoty) 
                                                + "<< a to je viac ako je definovanych >>" + 
                                                str(stlpec['dlzka'][0]) + "<< cifier pre stlpec >>" +
                                                stlpec['meno_stlpca'] + "<<."
                                                )
                elif isinstance(hodnota, Decimal):
                    
                    hod = format(hodnota, 'f').split('.')
                    
                    val_cel_casti = abs(int(hod[0]))
                    
                    if val_cel_casti != 0:
                        pocet_cifier_celej_casti_hodnoty = int(math.log10(val_cel_casti)) + 1
                    else:
                        pocet_cifier_celej_casti_hodnoty = 1
                    
                    
                    if pocet_cifier_celej_casti_hodnoty > stlpec['dlzka'][0]:
                        raise NoroDBException( "Chyba na riadku " + str(riadok) + 
                                                " v stlpci " + str(column) + 
                                                "! Pocet cifier celej casti cisla hodnoty >>" + str(hodnota)
                                                + "<< v dotaze je >>" + str(pocet_cifier_celej_casti_hodnoty) 
                                                + "<< a to je viac ako je definovanych >>" + 
                                                str(stlpec['dlzka'][0]) + "<< cifier pre stlpec >>" +
                                                stlpec['meno_stlpca'] + "<<."
                                                )
                                                
                   
                    val_des_casti = int(hod[1][::-1]) 
                    
                    if val_des_casti != 0:
                        pocet_cifier_desatinnej_casti_hodnoty = int(math.log10(val_des_casti)) + 1
                    else:
                        pocet_cifier_desatinnej_casti_hodnoty = 1
                                              
                    if pocet_cifier_desatinnej_casti_hodnoty > stlpec['dlzka'][1]:
                        raise NoroDBException( "Chyba na riadku " + str(riadok) + 
                                                " v stlpci " + str(column) + 
                                                "! Pocet cifier desatinnej casti cisla hodnoty >>" + str(hodnota)
                                                + "<< v dotaze je >>" + str(pocet_cifier_desatinnej_casti_hodnoty) 
                                                + "<< a to je viac ako je definovanych >>" + 
                                                str(stlpec['dlzka'][1]) + "<< cifier pre stlpec >>" +
                                                stlpec['meno_stlpca'] + "<<."
                                                )
    def uprav_vstupy(self):  
        stlpce_hlavicka = []
        for stlpec in self.hlavicka[2]:
            stlpce_hlavicka.append(stlpec['meno_stlpca'])
        stlpce_dotaz = self.rad_prikazov[1:self.koniec_mien_stlpcov]
        
        dlzka_stlpcov_dotazu = len(stlpce_dotaz)
        dlzka_stlpcov_hlavicky = len(stlpce_hlavicka)
        
        rozdiel_v_stlpcoch = dlzka_stlpcov_hlavicky - dlzka_stlpcov_dotazu
        
        hodnoty_s_typmi_pre_stlpce = []
        j=0
        for i in range(dlzka_stlpcov_dotazu, len(self.rad_prikazov_s_typmi[self.koniec_mien_stlpcov + 1:]) + 1, dlzka_stlpcov_dotazu):
            hodnoty_s_typmi_pre_stlpce.append(self.rad_prikazov_s_typmi[self.koniec_mien_stlpcov + 1:][j:i])
            j = i
        
        zoznam_indexov = vrat_zoz_indexov(stlpce_dotaz, stlpce_hlavicka) 
        for i in range(dlzka_stlpcov_hlavicky):
            if i not in zoznam_indexov:
                zoznam_indexov.append(i)
                
        for riadok in hodnoty_s_typmi_pre_stlpce:
            for _ in range(rozdiel_v_stlpcoch):
                riadok.append((None, None, None, None))
            riadok[:] = zorad_pole(riadok, zoznam_indexov)
        
        self.hodnoty_s_typmi_pre_stlpce = []
        for hodnoty in hodnoty_s_typmi_pre_stlpce:
            self.hodnoty_s_typmi_pre_stlpce.extend(hodnoty)
        
          
    def vykonaj(self):
        with open(self.subor, 'ab') as f:
            for poradie, (hodnota, typ, riadok, stlpec) in enumerate(self.hodnoty_s_typmi_pre_stlpce):
                stlpec_tabulky = self.hlavicka[2][poradie%len(self.hlavicka[2])]
                if stlpec_tabulky['typ_stlpca'][0] == "TEXT":
                    if hodnota is not None:
                        text = bytes(hodnota, "utf-8")
                        pb_text = len(text)
                        pb = pocet_bytov(pb_text)
                    else:
                        text = b'\x8f'
                        pb_text = 1
                        pb = 1
                    f.write(pb.to_bytes(1) + pb_text.to_bytes(pb, 'big') + text)    
                elif stlpec_tabulky['typ_stlpca'][0] == "INT":
                    if hodnota is not None:
                        if hodnota < 0 : sign = 1
                        else: sign = 0
                        f.write(sign.to_bytes(1))
                        f.write(abs(hodnota).to_bytes(stlpec_tabulky['dlzka_v_bytoch'][0], 'big'))
                    else:
                        sign = 2
                        f.write(sign.to_bytes(1))
                        f.write(int(0).to_bytes(stlpec_tabulky['dlzka_v_bytoch'][0], 'big'))
                elif stlpec_tabulky['typ_stlpca'][0] == "DEC":
                    if hodnota is not None:
                        if hodnota < 0 : sign = 1
                        else: sign = 0
                        f.write(sign.to_bytes(1))
                        hodnota = format(hodnota, 'f').split('.')
                        f.write(abs(int(hodnota[0])).to_bytes(stlpec_tabulky['dlzka_v_bytoch'][0], 'big'))
                        f.write(int(hodnota[1][::-1]).to_bytes(stlpec_tabulky['dlzka_v_bytoch'][1], 'big'))
                    else:
                        sign = 2
                        f.write(sign.to_bytes(1))
                        f.write(int(0).to_bytes(stlpec_tabulky['dlzka_v_bytoch'][0], 'big'))
                        f.write(int(0).to_bytes(stlpec_tabulky['dlzka_v_bytoch'][1], 'big'))
                        
# Trieda pre zobrazenie udajov z tabulky
class Select:
    
    def __init__(self, rad_prikazov, rad_prikazov_s_typmi):
        self.rad_prikazov = rad_prikazov
        self.rad_prikazov_s_typmi = rad_prikazov_s_typmi
        self.prever_prikazy()
        self.vykonaj()
    
    def prever_prikazy(self):
        # Preveri ci bola vybrata databaza a vrati cestu k tabulke
        cesta_k_tabulke = vrat_cestu_k_tabulke()
        
        # Preveri ci je v dotaze FROM
        try:
            self.koniec_mien_stlpcov = self.rad_prikazov.index("FROM")
        except ValueError:
            raise NoroDBException("Dotaz na riadku " + 
                                    str(self.rad_prikazov_s_typmi[0][2]) + 
                                    " nie je v poriadku")
                                    
        # Preveri ci existuje tabulka v danej databaze
        self.subor = cesta_k_tabulke + self.rad_prikazov[self.koniec_mien_stlpcov+1] + '.ndb'
        if not os.path.isfile(self.subor):
            raise NoroDBException('Tabulka s menom >>' + 
                                    self.rad_prikazov[self.koniec_mien_stlpcov+1] +
                                    '<< neexistuje!')
        
        self.hlavicka = nacitaj_hlavicku_tabulky(self.subor)
        
        # Preveri ci mena stlpcov z dotazu su v tabulke
        # a ci su nejake stlpce v dotaze a ci nie je zmiesana * s 
        # menami stlpcov
        if len(self.rad_prikazov[:self.koniec_mien_stlpcov]) == 0:
            raise NoroDBException('Chyba! V dotaze SELECT na riadku ' + 
                                    str(self.rad_prikazov_s_typmi[0][2]) + 
                                    " nie su zadane ziadne stlpce."
                                    )
        elif '*' not in self.rad_prikazov[:self.koniec_mien_stlpcov]:
            # Preveri ci stlpce z dotazu su v tabulke
            for meno_stlpca_v_dotaze in self.rad_prikazov[:self.koniec_mien_stlpcov]:
                existuje = False
                for stlpec_v_tabulke in self.hlavicka[2]:
                    if stlpec_v_tabulke["meno_stlpca"] == meno_stlpca_v_dotaze:
                        existuje = True
                        break
                if existuje == False:
                    raise NoroDBException('Chyba! V dotaze SELECT na riadku ' + 
                                            str(self.rad_prikazov_s_typmi[0][2]) + 
                                            ". Stlpec s menom >>" + meno_stlpca_v_dotaze + 
                                            "<< sa nenachadza v tabulke!")
        
        else:
            if len(self.rad_prikazov[:self.koniec_mien_stlpcov]) > 1:
                raise NoroDBException('Chyba! V dotaze SELECT na riadku ' + 
                                        str(self.rad_prikazov_s_typmi[0][2]) + 
                                        " nesmie byt * zaroven s inymi menami stlpcov."
                                        )

        
    def vykonaj(self):
        if '*' in self.rad_prikazov[:self.koniec_mien_stlpcov]:
            self.nacitaj_data_z_tabulky()
        else:
            self.nacitaj_data_z_tabulky(self.rad_prikazov[:self.koniec_mien_stlpcov])
        self.uprav_data()
        self.vypis_data()
        
    def nacitaj_data_z_tabulky(self, stlpce_z_dotazu = None):
        pointer = []
        self.data = []
        self.data.append([])
        for stlpec in self.hlavicka[2]:
            pointer.append((
                stlpec['meno_stlpca'],
                stlpec['typ_stlpca'][2],
                stlpec['dlzka_v_bytoch'],
            ))
            if stlpce_z_dotazu == None or stlpec['meno_stlpca'] in stlpce_z_dotazu:
                self.data[0].append(stlpec['meno_stlpca'])   
        with open(self.subor, 'rb') as f:
            x = f.read(self.hlavicka[3])
            riadok = 0
            koniec = False
            while True:
                riadok += 1
                self.data.append([])
                for meno_stlpca, typ, dlzka in pointer:
                    if typ == 0:
                        pb = f.read(1)
                        if pb == b'':
                            koniec = True
                            break
                        dlzka_textu = int.from_bytes(f.read(pb[0]), 'big')
                        if stlpce_z_dotazu == None or meno_stlpca in stlpce_z_dotazu:
                            text = f.read(dlzka_textu)
                            if text != b'\x8f':
                                self.data[riadok].append(text.decode("utf-8"))
                            else:
                                self.data[riadok].append('')
                        else:
                            f.seek(dlzka_textu, 1)
                    if typ == 1:
                        if stlpce_z_dotazu == None or meno_stlpca in stlpce_z_dotazu:
                            sign = f.read(1)
                            if sign == b'':
                                koniec = True
                                break
                            if sign[0] != 2:
                                cislo = int.from_bytes(f.read(dlzka[0]), 'big')
                                sign = -1*sign[0]
                                if sign == -1: cislo *= -1
                            else:
                                cislo = ''
                                f.seek(dlzka[0], 1)
                            self.data[riadok].append(cislo)
                        else:
                            f.seek(1+dlzka[0], 1)
                    if typ == 2:
                        if stlpce_z_dotazu == None or meno_stlpca in stlpce_z_dotazu:
                            sign = f.read(1)
                            if sign == b'':
                                koniec = True
                                break
                            if sign[0] != 2:
                                cela_cast = int.from_bytes(f.read(dlzka[0]), 'big')
                                desatinna_cast = int.from_bytes(f.read(dlzka[1]), 'big')
                                
                                if sign[0] == 1: sign = '-'
                                else: sign = ''
                                
                                str_cislo = sign + str(cela_cast) + '.' + str(desatinna_cast)[::-1]
                                presnost = len(str(desatinna_cast))
                                
                                with localcontext() as ctx:
                                    ctx.prec = presnost
                                    cislo = Decimal(str_cislo)
                            else:
                                cislo = ''
                                f.seek(dlzka[0]+dlzka[1], 1)
                            self.data[riadok].append(cislo)
                        else:
                            f.seek(1+dlzka[0]+dlzka[1], 1)
                if koniec:
                    self.data.pop(-1)
                    break
    
    def uprav_data(self):    
        # Pripad ze miesto mien stlpcov nie je *
        if '*' not in self.rad_prikazov[:self.koniec_mien_stlpcov]:
            # Pripad ze tie iste stlpce sa v dotaze neopakuju
            if len(self.rad_prikazov[:self.koniec_mien_stlpcov]) == len(set(self.rad_prikazov[:self.koniec_mien_stlpcov])):
                # Usporiada data (stlpce) podla poradia v dotaze
                zoz_indexov = vrat_zoz_indexov(self.data[0], self.rad_prikazov[:self.koniec_mien_stlpcov])
                for riadok in self.data:
                    riadok[:] = zorad_pole(riadok, zoz_indexov)
            
            # Nasledovne else je pripad ze rovnake stlpce sa v dotaze opakuju
            else:
                indexy_stlpca = {}
                for index, stlpec_z_dotazu in enumerate(self.rad_prikazov[:self.koniec_mien_stlpcov]):
                    if stlpec_z_dotazu not in indexy_stlpca:
                        indexy_stlpca[stlpec_z_dotazu] = [index]
                    else:
                        indexy_stlpca[stlpec_z_dotazu].append(index)
                
                # Pocet stlpcov navyse, rozdiel medzi poctom stlpcov v dotaze a poctom 
                # nacitanych stlpcov z tabulky
                # Ak mame opakujuce sa stlpce tieto sa v self.data vyskytuju iba raz
                nazvy_stlpcov = []
                nazvy_stlpcov[:] = self.data[0]
                pocet_stlpcov_navyse = len(self.rad_prikazov[:self.koniec_mien_stlpcov]) - len(self.data[0])
                for riadok in self.data:
                    for _ in range(pocet_stlpcov_navyse):
                        riadok.append(0)
                
                # Preusporiada data podla poradia stlpcov v dotaze
                for i, riadok in enumerate(self.data.copy()):
                    mena = set()
                    for j, stlpec in enumerate(riadok.copy()):
                        meno_stlpca = nazvy_stlpcov[j%len(nazvy_stlpcov)]
                        if meno_stlpca not in mena:
                            mena.add(meno_stlpca)
                            for index in indexy_stlpca[meno_stlpca]:
                                self.data[i][index] = stlpec 
        
        # Nasledovne else je pripad ze namiesto mien stlpcov v dotaze je *
        else:
            # Usporiada data (stlpce) podla poradia v dotaze
            zoz_indexov = vrat_zoz_indexov(self.data[0], [stlpec['meno_stlpca'] for stlpec in self.hlavicka[2]])
            for riadok in self.data:
                riadok[:] = zorad_pole(riadok, zoz_indexov)
        
    def vypis_data(self):  
        if self.data[1:] == []:
            print('Tabulka neobsahuje zaznamy')
        else:
            for i, riadok in enumerate(self.data[1:], 1):
                print('='*90)
                print('riadok c.' + str(i))
                print('='*90)
                for j, stlpec in enumerate(riadok):
                    print(str(self.data[0][j]) + ': ' + str(stlpec))
                
dotaz1 = '''
                
            use database prva;
            CREATE TABLE meno_tabulky
                id_meno_tabulky int 10  
                meno text   
                desatinne_cislo dec 10 10  
                plat dec 10   25
                meno2 text
                cena dec 10 10
                pocet int 10
                
                
        '''

text1 = '''
        Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.

Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.

Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.

Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.

Lorem ipsum dolor sit amet consectetur adipiscing elit. Quisque faucibus ex sapien vitae pellentesque sem placerat. In id cursus mi pretium tellus duis convallis. Tempus leo eu aenean sed diam urna tempor. Pulvinar vivamus fringilla lacus nec metus bibendum egestas. Iaculis massa nisl malesuada lacinia integer nunc posuere. Ut hendrerit semper vel class aptent taciti sociosqu. Ad litora torquent per conubia nostra inceptos himenaeos.
'''

dotaz2 = f'''
           
            use database prva;
            drop table meno_tabulky;
            CREATE TABLE meno_tabulky
                id_meno_tabulky int 10  
                meno text   
                desatinne_cislo dec 10 10  
                plat dec 10   25
                meno2 text
                cena dec 10 10
                pocet int 10;
            INSERT INTO meno_tabulky
            id_meno_tabulky meno desatinne_cislo plat meno2 cena pocet
            values
            1 ''Norbert 'Uzasny' 
            a "neprekonatelny"'' -23.56e-5 -5000.25 ""Jankura"" -999,00044e3 100
            2 ''{text1}'' 0.5 500.56 ""Kery d'Arno"" 25.3 45;
            select 
                *
            from 
                meno_tabulky
                
        '''   
dotaz3 = '''
            use database prva;
            select 
               meno2 desatinne_cislo cena id_meno_tabulky
            from 
                meno_tabulky

'''
dotaz4 = '''
            use database prva;
            drop table meno_tabulky;
            CREATE TABLE meno_tabulky
                id_meno_tabulky int 10  
                meno text   
                desatinne_cislo dec 10 10  
                plat dec 10   25
                meno2 text
                cena dec 10 10
                pocet int 10;
            INSERT INTO meno_tabulky
                id_meno_tabulky pocet meno plat
            values
            1 45 ""Peter"" 2500.58
            2 150 ""Jano"" 3500.87
            3 250 ""Noro"" 8900.58;
            select * from meno_tabulky;
'''
Dotaz(dotaz3)

'''
start = time.time()
for _ in range(50000):
    Dotaz(dotaz4)        
print('celkovy cas dotazu:', time.time() - start, 'sekund')
# 262 sek, co je viac ako 4 min - trva insert into 100 000 riadkov s textami ktore nie su velke
# select 3 riadkov a uprava pretoze je z nich sest riadkov trvala menej ako 4 sekundy
# vypis selectu trva dlho pre 100 000 riadkov
'''