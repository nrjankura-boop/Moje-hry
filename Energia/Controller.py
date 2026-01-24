import decimal
import re
import threading

class Controller():

    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.controller = self # Toto je velmi nutne aby View mohlo komunikovat s controllerom
        
        self.global_nazov_diety = '' # nazov diety ktora sa prave spracuva ci zobrazuje
        self.global_id_diety = 0 # id_diety ktore sa prave spracuva ci zobrazuje
        
        self.kategorie_jedla = False # list of tuples s id a nazvom pre kateg. jedla
        
        self.lock = threading.Lock() # lock pre vykonanie iba jedneho threadu pri zobrazovni potravin v sprave potravin
       
        # =========== main Frame parts =========================
        
        self.zobraz_menu()
        self.zobraz_combo()
        self.zobraz_entry()
        self.zobraz_canvas_diety()
        self.zobraz_frame_udajov()
        
        # =============== Koniec main Frame parts =====================
        
    # ================== Ovladanie menu; metody menu ===================== 
    
    def zobraz_menu(self):
        self.view.menu()
        
        # ------ Zobrazenie zoznamu vsetkych potravin v tabulke ------------
    
    def zobraz_vsetky (self):
        self.zobraz_zoznam(self.model.zoznam_vsetkych_potravin())
   
        # ------------------- Koniec zobrazenia zoznamu vsetkych potravin v tabulke --------------------
    
    # ===================== Koniec ovladania menu, metody menu ===============================  
    
    
    # ==========================================================================
    # ==================             ===========================================
    # ================== Navrh diety ===========================================
    # ==================             ===========================================
    # ==========================================================================
    
    
    # ===================== Zobraz combobox kategorie jedla ======================
    
    def zobraz_combo(self):
        data = self.data_pre_combo()
        self.view.add_combo((' - Vyberte kategoriu jedla - ', ) + tuple(data))
    
    def zobraz_podla_kategorie(self, event):
        self.view.entry.delete(0, 'end')
        id = self.dict_id_kategoria[self.view.vybrana_kategoria.get()]
        if id != 0:
            self.zobraz_zoznam(self.model.zoznam_potravin_podla_kategorie(id))
        else:
            self.zobraz_vsetky()
        
    # ======================== Koniec combobox kategorie jedla =======================

    # ================= Entry pre vyhladavanie potravin ===============================
    
    def zobraz_entry (self):
        self.view.add_entry()
    
    def zobraz_podla_retazca(self, *args):
        retazec = self.view.zadany_retazec.get()
        if len(retazec) > 2:
            self.zobraz_zoznam(self.model.zoznam_potravin_podla_retazca(retazec))
        else:
            self.zobraz_vsetky()
    
    def entry_focusin(self, event):
        self.view.combo.current(0)
    
    # ================= Koniec Entry pre vyhladavanie potravin ==========================
    
    # ========== Zobraz tabulku s datami =======================
    
    def zobraz_zoznam (self, zoznam): 
        # column names:
        # riadok[0] -> id_potravina
        # riadok[1] -> id_kategoria_jedla
        # riadok[2] -> nazov
        # riadok[3] -> sacharidy
        # riadok[4] -> tuky
        # riadok[5] -> bielkoviny
        # riadok[6] -> timestamp
        
        data = []
        for riadok in zoznam:
            data.append ((riadok[0], riadok[2], riadok[3] + ' g', riadok[4] + ' g', riadok[5] + ' g'))
            
        columns = ('id_potravina', 'nazov', 'sacharidy', 'tuky', 'bielkoviny')
        column_names = ('ID', 'Názov', 'Sacharidy', 'Tuky', 'Bielkoviny')
        
        self.view.okno_zoznamu(
            height = 40,
            columns = columns, 
            column_names = column_names, 
            data = data
        )
        
    # ================= Koniec zobrazenia tabulky s udajmi ======================
    
    # ================= Ovladanie canvas_diety ==================================
        
    def zobraz_canvas_diety (self):
        self.view.add_canvas_diety()
    
    # ================= Koniec Ovladanie canvas_diety ==================================
    
    # ================= Ovladanie udajov diety ==========================================
    
    def zobraz_frame_udajov(self):
        self.view.add_frame_udajov()
    
    # ================= Koniec ovladanai udajov diety ===================================
    
    # ================ Ovladanie pre vyber prvku z Treeview zoznam (select) =============================
    
    def zobraz_pridavaci_dialog(self, event):
        vybrana_potravina = self.view.zoznam.focus()
        
        # -- ['values'] je list [] s hodnotami v poradi ako je v tabulke zoznam potravin -----
        riadok = self.view.zoznam.item(vybrana_potravina)['values']
        if  riadok != '':
            self.id_potravina_posledna = riadok[0]
            self.view.zobraz_okno_pre_potvrdenie_prvku (riadok[1])
    
    # ================ Koniec vyber prvku z Treeview zoznam (select) =============================
    
    # =============== Ovladanie pre pridanie prvku do diety ======================================
    
    def pridaj_prvok_diety(self):
        nazov_diety = self.view.text_nazov_diety.get()
        if len(nazov_diety) == 0:
            self.view.show_error('Vyplňte nazov diety')
        else:
            # -- pridaj nazov diety do tabulky dieta ak uz taky nazov neexistuje
            
            if not self.dieta_existuje(nazov_diety):
                self.model.pridaj_dietu(nazov_diety)
                
            if self.global_nazov_diety != nazov_diety:
            
                self.global_nazov_diety = nazov_diety
                self.global_id_diety = self.model.vrat_id_diety(nazov_diety)[0][0] 
                
                # vymaz canvas_diety
                self.view.zmaz_canvas_diety()
                
                # vypln canvas_diety
                self.vypln_canvas_diety()
                
                # vypocitaj hodnoty diety a vypln ich
                self.vypocitaj_hodnoty_a_vypln()
                
                # -- Nastav nadpis diety  
 
                self.view.nastav_nadpis_diety()
                
                # odblokuj menu items pre pridanie diety do suboru pdf a txt
                self.odblokuj_pridanie_do_suboru()
                
                
            # ak neexistuje potravina v diete tak ju pridaj
            # kontrola ci existuje v diete potravina
            data_pre_potravinu = self.model.vrat_potravinu(self.global_id_diety, self.id_potravina_posledna)
            if len(data_pre_potravinu) == 0:
            
                # -- pridaj potravinu do tabulky potraviny diety pre konkretnu dietu
                self.model.pridaj_potravinu_do_diety(self.global_id_diety, self.id_potravina_posledna)
            
                # -- zobraz na canvas prvok diety
                data_pre_potravinu = self.model.vrat_potravinu(self.global_id_diety, self.id_potravina_posledna)
            
                self.view.pridaj_potravinu_na_canvas_diety(data_pre_potravinu[0])
            else:
                self.view.show_error('Potravina: ' + data_pre_potravinu[0][1] + ' je už pridaná')
            
            self.view.okno_pre_potvrdenie_prvku.destroy()    
    
    # =============== Koniec ovladania pre pridanie prvku do diety ======================================
    
    # ============== Overenie ci dieta existuje podla nazvu ===============================
    
    def dieta_existuje(self, nazov_diety):
        zoznam_nazvov_diet = self.model.vrat_nazvy_diet()    
            
        for dieta in zoznam_nazvov_diet:
            if nazov_diety == dieta[0]:
                return True
        return False
        
    # =============== Koniec overenia ci dieta existuje podla nazvu =======================
    # ================ Zmaz prvok diety ==========================================================
    
    def zmaz_prvok_diety(self, id_potravina):
        self.model.zmaz_prvok_diety(self.global_id_diety, id_potravina)
        self.view.zmaz_canvas_diety()
        self.vypln_canvas_diety()
        self.vypocitaj_hodnoty_a_vypln()
        self.view.okno_potvrd_zmaz_prvku.destroy()
        
    # ================ Koniec zmaz prvok diety ===================================================
    
    # ================= Uloz udaj mnozstva a spusti vypocet ==========================================
    
    def uloz_udaj_mnozstva(self, var, index, mode, id_potravina):
        mnozstvo = self.view.canvas_entry_mnozstvo[id_potravina].get()
        pocet_znakov = 4
        if len(mnozstvo) > pocet_znakov:
            self.view.canvas_entry[id_potravina].delete(pocet_znakov, 'end')
            mnozstvo = self.view.canvas_entry_mnozstvo[id_potravina].get()
            
        if re.fullmatch(r'(\d+\.)?\d*', str(mnozstvo)):
            self.model.uloz_mnozstvo(self.global_id_diety, id_potravina, mnozstvo)
            self.model.zmaz_prerozdelenie_prvku(self.global_id_diety, id_potravina)
            self.vypocitaj_hodnoty_a_vypln()
        else:
            self.view.canvas_entry[id_potravina].delete(0, 'end')
            #self.view.canvas_entry[id_potravina].insert(0, '0')
            
    # ================== Koniec uloz udaj mnozstva a spusti vypocet ===================================
    
    # ================ Vypln canvas diety ============================
    
    def vypln_canvas_diety(self):
        data = self.model.vrat_potraviny_diety(self.global_id_diety)
        self.view.vypln_canvas_diety(data)
        
    # ================= Koniec vypln_canvas_diety ==========================
    
    # =================== Vypocitaj a nastav hodnoty =============================================================
    
    def vypocitaj_stratu_tuku(self, var, index, mode):
        denna_spotreba_energie = self.view.hodnota_den_spotr_energ.get()
        
        pocet_znakov = 5
        if len(denna_spotreba_energie) > pocet_znakov:
            self.view.denna_spotreba_energie.delete(pocet_znakov, 'end')
            denna_spotreba_energie = self.view.hodnota_den_spotr_energ.get()
            
        celkova_energia_diety = self.view.hod_celk_energia["text"].rstrip(' kJ')
        if celkova_energia_diety != '-' and re.fullmatch(r'\d*', str(denna_spotreba_energie)):
            if denna_spotreba_energie == '':
                denna_spotreba_energie = 0

            den, tyzden, mesiac, rok = self.vypocet_straty_tuku(denna_spotreba_energie, celkova_energia_diety)
            
            self.view.nastav_stratu_tuku(den, tyzden, mesiac, rok)
        else: 
            self.view.denna_spotreba_energie.delete(0, 'end')
            self.view.denna_spotreba_energie.insert(0, self.view.root.denna_spotreba_energie)
    
    def vypocet_straty_tuku(self, denna_spotreba_energie, celkova_energia_diety):
        den = round((float(denna_spotreba_energie) - float(celkova_energia_diety)) / 37.656, 2)
        tyzden = round((den * 7), 2)
        mesiac = round(den * 30)
        rok = round(den * 365)
        return den, tyzden, mesiac, rok
    # ----------- Vrati zoznam potravin diety (prvky diety) a ich hodnoty S T B mnozstvo --------
    
    def vrat_zoznam_potravin_diety(self):
        return self.model.vrat_potraviny_diety(self.global_id_diety)
    
    # ---------- Vypocita hodnotu S T B E pre dane mnozstvo kazdej potraviny v diete ------------
    
    def vypocitaj_hodnoty_pre_prvky_diety(self):
        zoznam_potravin_diety = self.vrat_zoznam_potravin_diety()
        
        # riadok [0]-> id_potravina
        # riadok [1]-> nazov
        # riadok [2]-> sacharidy
        # riadok [3]-> tuky
        # riadok [4]-> bielkoviny
        # riadok [5]-> mnozstvo
        
        energia_kj = {}
        sacharidy = {}
        tuky = {}
        bielkoviny = {}
        mnozstvo_arr = {}
        
        for riadok in zoznam_potravin_diety:
            mnozstvo = riadok[5]
           
            if mnozstvo == None or mnozstvo == '':
                mnozstvo = 0
                
            mnozstvo_arr[riadok[0]] = mnozstvo   
            energia_kj[riadok[0]] = (float(riadok[2]) * 16.736 + float(riadok[3]) * 37.656 + float(riadok[4]) * 16.736) / 100 * float(mnozstvo)
            sacharidy[riadok[0]] = float(riadok[2]) / 100 * float(mnozstvo)
            tuky[riadok[0]] = float(riadok[3]) / 100 * float(mnozstvo)
            bielkoviny[riadok[0]] = float(riadok[4]) / 100 * float(mnozstvo)
        
        return energia_kj, sacharidy, tuky, bielkoviny, mnozstvo_arr

    # ----------------------- Vypocita celkove hodnoty diety S T B E ----------------------------
    
    def vypocitaj_celkove_hodnoty_diety(self):
        energia_kj, sacharidy, tuky, bielkoviny, mnozstvo_arr = self.vypocitaj_hodnoty_pre_prvky_diety()
        
        celk_energia_kj = round(sum(energia_kj.values()))
        celk_sacharidy = round(sum(sacharidy.values()), 1)
        celk_tuky = round(sum(tuky.values()), 1)
        celk_bielkoviny = round(sum(bielkoviny.values()), 1)
        
        return celk_energia_kj, celk_sacharidy, celk_tuky, celk_bielkoviny
    
    # ---------------- Vypocita odporucene hodnoty S T B pre dietu z celkovej energie -----------
    
    def vypocitaj_odporucane_hodnoty_diety(self):
        celk_energia_kj, celk_sacharidy, celk_tuky, celk_bielkoviny = self.vypocitaj_celkove_hodnoty_diety()
        
        odp_celk_sacharidy = round((0.4 * celk_energia_kj) / 16.736)
        odp_celk_tuky = round((0.3 * celk_energia_kj) / 37.656)
        odp_celk_bielkoviny = round((0.3 * celk_energia_kj) / 16.736)
        
        return odp_celk_sacharidy, odp_celk_tuky, odp_celk_bielkoviny
    
    # ------------------ Vypocita vsetko a vyplni vsetko --------------------------------------
    
    def vypocitaj_hodnoty_a_vypln(self):
        energia_kj, sacharidy, tuky, bielkoviny, mnozstvo_arr = self.vypocitaj_hodnoty_pre_prvky_diety()
        for id_potravina in energia_kj.keys():
            self.view.nastav_jednotlive_hodnoty(id_potravina, round(sacharidy[id_potravina], 1), round(tuky[id_potravina], 1), round(bielkoviny[id_potravina], 1))
        
        celk_energia_kj, celk_sacharidy, celk_tuky, celk_bielkoviny = self.vypocitaj_celkove_hodnoty_diety()   
        self.view.nastav_celkove_hodnoty(celk_energia_kj, celk_sacharidy, celk_tuky, celk_bielkoviny)
        
        odp_celk_sacharidy, odp_celk_tuky, odp_celk_bielkoviny = self.vypocitaj_odporucane_hodnoty_diety()
        self.view.nastav_odp_celkove_hodnoty(odp_celk_sacharidy, odp_celk_tuky, odp_celk_bielkoviny)
    
        self.vypocitaj_stratu_tuku(1,1,1)
    '''
    def vypocitaj_hodnoty_a_vypln(self):
        zoznam_potravin_diety = self.model.vrat_potraviny_diety(self.global_id_diety)
        # riadok [0]-> id_potravina
        # riadok [1]-> nazov
        # riadok [2]-> sacharidy
        # riadok [3]-> tuky
        # riadok [4]-> bielkoviny
        # riadok [5]-> mnozstvo
        
        energia_kj = {}
        sacharidy = {}
        tuky = {}
        bielkoviny = {}
        
        for riadok in zoznam_potravin_diety:
            mnozstvo = riadok[5]
           
            if mnozstvo == None or mnozstvo == '':
                mnozstvo = 0
                
            energia_kj[riadok[0]] = (float(riadok[2]) * 16.736 + float(riadok[3]) * 37.656 + float(riadok[4]) * 16.736) / 100 * float(mnozstvo)
            sacharidy[riadok[0]] = float(riadok[2]) / 100 * float(mnozstvo)
            tuky[riadok[0]] = float(riadok[3]) / 100 * float(mnozstvo)
            bielkoviny[riadok[0]] = float(riadok[4]) / 100 * float(mnozstvo)
        
            self.view.nastav_jednotlive_hodnoty(riadok[0], round(sacharidy[riadok[0]], 1), round(tuky[riadok[0]], 1), round(bielkoviny[riadok[0]], 1))
        
        celk_energia_kj = round(sum(energia_kj.values()))
        celk_sacharidy = round(sum(sacharidy.values()), 1)
        celk_tuky = round(sum(tuky.values()), 1)
        celk_bielkoviny = round(sum(bielkoviny.values()), 1)
        
        self.view.nastav_celkove_hodnoty(celk_energia_kj, celk_sacharidy, celk_tuky, celk_bielkoviny)
        
        odp_celk_sacharidy = round((0.4 * celk_energia_kj) / 16.736)
        odp_celk_tuky = round((0.3 * celk_energia_kj) / 37.656)
        odp_celk_bielkoviny = round((0.3 * celk_energia_kj) / 16.736)
        
        self.view.nastav_odp_celkove_hodnoty(odp_celk_sacharidy, odp_celk_tuky, odp_celk_bielkoviny)
        
        self.vypocitaj_stratu_tuku(1,1,1)
    '''
    
    # =================== Koniec Vypocitaj a nastav hodnoty =============================================================
    
    # =================== Vyber dietu dialog a pridanie diety ovladanie ===================================================
    
    def vyber_dietu_dialog(self):
        # z databazy ziskaj mena diet a datumy vytvorenia a celkove hodnoty Energie a T B S
        data = self.model.vrat_diety_a_ich_sumar()
        # zavolaj metodu view pre zobrazenie okna pre vyber diety 
        self.view.zobraz_dialog_diet(data, 'vyber')
        
    def nacitaj_dietu (self, event, id_dieta):
        self.global_id_diety = id_dieta
        
        nazov_diety = self.model.vrat_nazov_diety(self.global_id_diety)
        self.global_nazov_diety = nazov_diety[0][0]
        
        self.odblokuj_pridanie_do_suboru()
        
        self.view.zmaz_canvas_diety()
        self.vypln_canvas_diety()
        
        self.vypocitaj_hodnoty_a_vypln()
        self.view.nastav_nadpis_diety()
        
        self.view.okno_vyberu_diety.destroy()
        
    # =================== Koniec Vyber dietu dialog ovladanie ===================================================
    
    # ==================== Zmazanie diety dialog ovladanie ==========================================
    
    def zmaz_dietu_dialog(self):
        # z databazy ziskaj mena diet a datumy vytvorenia a celkove hodnoty Energie a T B S
        data = self.model.vrat_diety_a_ich_sumar()
        # zavolaj metodu view pre zobrazenie okna pre vyber diety 
        self.view.zobraz_dialog_diet(data, 'zmaz')
        
    def zmaz_dietu(self, id_dieta):
        self.model.zmaz_dietu(id_dieta)
        
        self.view.okno_vyberu_diety.destroy()
        
        if self.global_id_diety == id_dieta:
            self.view.zmaz_canvas_diety()
            self.view.zmaz_nadpis_diety()
            self.view.zmaz_frame_udajov()
            self.global_id_diety = 0
            self.global_nazov_diety = ''
            self.zablokuj_pridanie_do_suboru()
            
        self.zmaz_dietu_dialog()
        
    # ==================== Koniec Zmazanie diety dialog ovladanie ==========================================
    
    # ====================== Vytvor dietu =================================================
    
    def vytvor_dietu (self, nazov_diety_stringvar):
        nazov_diety = nazov_diety_stringvar.get()
        if nazov_diety.strip() != '' and not self.dieta_existuje(nazov_diety):
            self.global_nazov_diety = nazov_diety
        
            self.model.pridaj_dietu(self.global_nazov_diety)
            self.global_id_diety = self.model.vrat_id_diety(self.global_nazov_diety)[0][0]
        
            self.odblokuj_pridanie_do_suboru()
        
            self.view.zmaz_canvas_diety()
            self.view.nastav_nadpis_diety()
            self.view.zmaz_frame_udajov()
            
            self.view.okno_pre_vytvorenie_diety.destroy()
        elif nazov_diety.strip() == '':
            self.view.show_error("Vyplňte názov diety!")
        else:
            self.view.show_error("Dieta " + nazov_diety + " už existuje, zvoľte iný názov!")
        
    # ====================== Koniec Vytvor dietu =================================================
    
    
    # ==========================================================================
    # ==================                 =======================================
    # ================== Sprava potravin =======================================
    # ==================                 =======================================
    # ==========================================================================
    
    
    # ========== zobraz Combo kategoria_jedla pre spravu ========================
    
    def zobraz_sprava_combo(self):
        data = self.data_pre_combo()
        self.view.add_sprava_combo((' - Vyberte kategoriu jedla - ', ) + tuple(data), self.view.main_frame_sprava, self.sprava_zobraz_podla_kategorie)
    
    # ========== Koniec zobraz Combo kategoria_jedla pre spravu ========================
    
    # =================== Vyhlada potraviny podla kategorie jedla ======================
    
    def sprava_zobraz_podla_kategorie(self, event):
        cbname = str(self.view.sprava_zadany_retazec.trace_info()[0][1])
        self.view.sprava_zadany_retazec.trace_remove('write', cbname = cbname)
        self.view.sprava_entry.delete(0, 'end')
        self.view.sprava_zadany_retazec.trace('w', callback = self.sprava_zobraz_podla_retazca)
        
        id = self.dict_id_kategoria[self.view.sprava_vybrana_kategoria.get()]
        
        if id != 0:
            self.vsetky_su_zobrazene = False
            data = self.model.zoznam_potravin_podla_kategorie(id)
            self.thread_zobraz_potraviny = threading.Thread(target = self.view.sprava_zobraz_potraviny, args = (data, ), daemon = True)
            self.thread_zobraz_potraviny.start()
        else:
            if not self.vsetky_su_zobrazene:
                self.sprava_zobraz_vsetky()
           
    # =================== Koniec Vyhlada potraviny podla kategorie jedla ======================
    
    # ========= Vyhlada potraviny podla zadaneho retazca v entry pre spravu ========================
    
    def sprava_zobraz_podla_retazca(self, *args):
        retazec = self.view.sprava_zadany_retazec.get()
        
        if len(retazec) > 2:
            data = self.model.zoznam_potravin_podla_retazca(retazec)
            self.thread_zobraz_potraviny = threading.Thread(target = self.view.sprava_zobraz_potraviny, args = (data, ), daemon = True)
            self.thread_zobraz_potraviny.start()
            self.vsetky_su_zobrazene = False
        else:
            if not self.vsetky_su_zobrazene:
                self.sprava_zobraz_vsetky()
    
    def sprava_entry_focusin(self, event):
        self.view.sprava_combo.unbind('<<ComboboxSelected>>')
        self.view.sprava_combo.current(0)
        self.view.sprava_combo.bind('<<ComboboxSelected>>', self.sprava_zobraz_podla_kategorie)
        
    # ========= Koniec Vyhlada potraviny podla zadaneho retazca v entry pre spravu ========================        
            
    # =============== Zobraz potraviny ==================================================
    
    def sprava_zobraz_vsetky(self):
        data = self.model.zoznam_vsetkych_potravin()
        
        self.thread_zobraz_potraviny = threading.Thread(target = self.view.sprava_zobraz_potraviny, args = (data, ), daemon = True)
        self.thread_zobraz_potraviny.start()
        self.vsetky_su_zobrazene = True
    
    def zobraz_potravinu(self, nazov_potraviny):
        data = self.model.vrat_potravinu_z_nazvu(nazov_potraviny)
        self.view.sprava_zobraz_potraviny(data)
    
    def zobraz_potravinu_podla_id(self, id_potravina):
        data = self.model.vrat_potravinu_z_id(id_potravina)
        self.view.sprava_zobraz_potraviny(data)
        
    # =============== Koniec zobraz potraviny ==================================================
    
    # ================ Pridaj potravinu do tabulky vsetkych potravin =========================
    
    def sprava_pridaj_potravinu(self):
        nazov_potraviny = self.view.stringvar_entry_pridaj_nazov.get().strip()
        sacharidy = self.view.stringvar_entry_pridaj_sacharidy.get().strip()
        tuky = self.view.stringvar_entry_pridaj_tuky.get().strip()
        bielkoviny = self.view.stringvar_entry_pridaj_bielkoviny.get().strip()
        kategoria_jedla = self.view.stringvar_combo_pridaj.get()
        
        if nazov_potraviny == '':
            self.view.show_error('Vyplňte nazov potraviny')
        elif not self.je_cislo(sacharidy):
            self.view.show_error('Množstvo sacharidov má byť číslo')
        elif not self.je_cislo(tuky):
            self.view.show_error('Množstvo tukov má byť číslo')
        elif not self.je_cislo(bielkoviny):
            self.view.show_error('Množstvo bielkovin má byť číslo')
        elif kategoria_jedla == '':
            self.view.show_error('Vyberte kategóriu jedla')
        else:
            id_kategoria_jedla = self.dict_id_kategoria[kategoria_jedla]
            self.model.pridaj_potravinu_do_potravin(
                nazov_potraviny,
                sacharidy,
                tuky,
                bielkoviny,
                id_kategoria_jedla
            )
            self.zobraz_potravinu(nazov_potraviny)
            self.reset_vyhladavania()
            
    # ================ Koniec Pridaj potravinu do tabulky vsetkych potravin =========================
    
    # ===================== Zmaz potravinu =====================================
    
    def zmaz_potravinu(self, id_potravina):
        self.view.dialog_zmaz_potravinu.destroy()
        self.model.zmaz_potravinu(id_potravina)
        self.sprava_zobraz_vsetky()
    
    # ===================== Zmaz potravinu =====================================
    
    # ==================== Zmen hodnoty potraviny ==============================
 
    def zmen_hodnoty_potraviny(self, id_potravina):
        nazov_potraviny = self.view.stringvar_entry_nazov[id_potravina].get().strip()
        sacharidy = self.view.stringvar_entry_sacharidy[id_potravina].get().strip()
        tuky = self.view.stringvar_entry_tuky[id_potravina].get().strip()
        bielkoviny = self.view.stringvar_entry_bielkoviny[id_potravina].get().strip()
        kategoria_jedla = self.view.stringvar_combo[id_potravina].get()
        
        if nazov_potraviny == '':
            self.view.show_error('Vyplňte nazov potraviny')
        elif not self.je_cislo(sacharidy):
            self.view.show_error('Množstvo sacharidov má byť číslo')
        elif not self.je_cislo(tuky):
            self.view.show_error('Množstvo tukov má byť číslo')
        elif not self.je_cislo(bielkoviny):
            self.view.show_error('Množstvo bielkovin má byť číslo')
        elif kategoria_jedla == '':
            self.view.show_error('Vyberte kategóriu jedla')
        else:
            id_kategoria_jedla = self.dict_id_kategoria[kategoria_jedla]
            self.model.zmen_potravinu_v_potravinach(
                id_potravina,
                nazov_potraviny,
                sacharidy,
                tuky,
                bielkoviny,
                id_kategoria_jedla
            )
        
        self.zobraz_potravinu_podla_id(id_potravina)
        self.reset_vyhladavania()
        
    # ==================== Koniec Zmen hodnoty potraviny ==============================
    
    # ================= reset combo a entry vyhladavania ==============================
    
    def reset_vyhladavania(self):
        self.view.sprava_combo.unbind('<<ComboboxSelected>>')
        self.view.sprava_combo.current(0)
        self.view.sprava_combo.bind('<<ComboboxSelected>>', self.sprava_zobraz_podla_kategorie)
    
        cbname = str(self.view.sprava_zadany_retazec.trace_info()[0][1])
        self.view.sprava_zadany_retazec.trace_remove('write', cbname = cbname)
        self.view.sprava_entry.delete(0, 'end')
        self.view.sprava_zadany_retazec.trace('w', callback = self.sprava_zobraz_podla_retazca)
        
    # ================= Koniec reset combo a entry vyhladavania ==============================
    
    
    # ==========================================================================
    # ==================                                  ======================
    # ================== Rozdelenie potravin do jedal dna ======================
    # ==================                                  ======================
    # ==========================================================================
    
    
    # ================= data pre Vypln canvas priradenia ================================
    
    def data_pre_canvas_priradenia(self):
        data = self.model.vrat_potraviny_diety_pre_priradenie(self.global_id_diety)
        data_prerozdelenia = self.model.vrat_rozdelenie_do_jedal(self.global_id_diety)
        self.view.vypln_canvas_priradenia(data, data_prerozdelenia)
       
    
    # ================= Koniec data pre Vypln canvas priradenia ================================
    
    # ================ Ovladanie pre prerozdelenie potravin do jedal ==================
    
    def prerozdel_potraviny_do_jedal(self, var, index, mode, id_potravina, jedlo):
        mnozstvo = {}
        for i in range(1, 7):
            mnozstvo[i] = self.view.rozdelenie_stringvar[id_potravina][i].get()
            if mnozstvo[i] == '':
                mnozstvo[i] = 0
        
        pocet_znakov = 4
        if len(str(mnozstvo[jedlo])) > pocet_znakov:
            self.view.rozdelenie_entry[id_potravina][jedlo].delete(pocet_znakov, 'end')
            mnozstvo[jedlo] = self.view.rozdelenie_stringvar[id_potravina][jedlo].get()
            
        if not re.fullmatch(r'(\d+\.)?\d*', str(mnozstvo[jedlo])):
            self.view.rozdelenie_entry[id_potravina][jedlo].delete(0, 'end')
            mnozstvo[jedlo] = self.view.rozdelenie_stringvar[id_potravina][jedlo].get()
               
        decimal.getcontext().prec = 5
        
        priradene_mnozstvo = self.suma_mnozstva(mnozstvo)
        zostatok_mnozstva = decimal.Decimal(self.view.celkove_mnozstvo_potraviny[id_potravina]) - priradene_mnozstvo
        
        if zostatok_mnozstva < 0:
            mnozstvo[jedlo] = decimal.Decimal(mnozstvo[jedlo]) + zostatok_mnozstva
            
            self.view.rozdelenie_entry[id_potravina][jedlo].delete(0, 'end')
            self.view.rozdelenie_entry[id_potravina][jedlo].insert(0, mnozstvo[jedlo])
           
            priradene_mnozstvo = self.suma_mnozstva(mnozstvo)
            zostatok_mnozstva = decimal.Decimal(self.view.celkove_mnozstvo_potraviny[id_potravina]) - priradene_mnozstvo
        
        self.view.rozdelenie_zostatok_mnozstvo_label[id_potravina]['text'] = str(zostatok_mnozstva) + ' g'
        
        existuje_zaznam = self.model.vrat_zaznam(self.global_id_diety, id_potravina)
        
        if existuje_zaznam:
            self.model.zmen_hodnoty_prerozdelenia(self.global_id_diety, id_potravina, mnozstvo)
        else:
            self.model.pridaj_hodnoty_prerozdelenia(self.global_id_diety, id_potravina, mnozstvo)
            
        self.zobraz_zoznam_jedal()

    def zobraz_zoznam_jedal(self):
        data = self.model.vrat_rozdelenie(self.global_id_diety)
        self.view.vypln_canvas_zoznam_jedal(data)
        
    # ================ Koniec Ovladanie pre prerozdelenie potravin do jedal ===========
    
    # ==========================================================================
    # ==================                       =================================
    # ================== Vytvorenie pdf suboru =================================
    # ==================                       =================================
    # ==========================================================================
    
    
    # ==========================================================================
    # ==================                 =======================================
    # ================== Spolocne metody =======================================
    # ==================                 =======================================
    # ==========================================================================
    
    # ======================= Data pre combo kategoria_jedla ===================
    
    def data_pre_combo (self):
        if not self.kategorie_jedla:
            self.kategorie_jedla = self.model.zoznam_kategorie_jedla()
        
        # column names:
        # riadok[0] -> id_kategoria_jedla
        # riadok[1] -> nazov_kategorie
        # riadok[2] -> ts
        
        data = []
        self.dict_id_kategoria = {}
        self.dict_val_kategoria = {}
        self.dict_id_kategoria.update({' - Vyberte kategoriu jedla - ' : 0})
        for riadok in self.kategorie_jedla:
            data.append(riadok[1])
            self.dict_id_kategoria.update({riadok[1] : riadok[0]})
            self.dict_val_kategoria.update({riadok[0] : riadok[1]})
            
        return data
    
    # ================== odblokuj a zablokuj menu items pre pridanie do suboru ================
    
    def odblokuj_pridanie_do_suboru(self):   
        self.view.do_suboru_menu.entryconfig("Dieta do pdf súboru", state = "normal")
        self.view.do_suboru_menu.entryconfig("Dieta do textového súboru", state = "normal")
    
    def zablokuj_pridanie_do_suboru(self):   
        self.view.do_suboru_menu.entryconfig("Dieta do pdf súboru", state = "disabled")
        self.view.do_suboru_menu.entryconfig("Dieta do textového súboru", state = "disabled")
    
    # ================= kontrola ci je retazec cislo ===============================
    
    @staticmethod
    def je_cislo(retazec):
        return re.fullmatch(r'(\d+\.)?\d+', str(retazec))
        
    @staticmethod
    def suma_mnozstva(mnozstvo):
        decimal.getcontext().prec = 5
        priradene_mnozstvo = 0
        for m in mnozstvo.values():
            if m != '':
                priradene_mnozstvo += decimal.Decimal(m)
        return priradene_mnozstvo