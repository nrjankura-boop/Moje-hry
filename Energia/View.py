import tkinter as tk
from tkinter import ttk
import tkinter.font as font
from tkinter.messagebox import showerror, askyesno
from tkinter import filedialog as fd

from fpdf import FPDF

import os

import threading

import datetime
import time
import decimal

import Frames
import Okna

class View():
    
    def __init__(self, root):
        self.root = root
        
        # ======================== inicializacia premennych ===========================
        
        self.canvas_text_y = 0 # pozicia y pre prvky zoznamu v canvase diety
       
        self.canvas_entry_mnozstvo = {} # {id_potravina : StringVar} pre vsetky entry v canvase diety
        self.canvas_entry = {} # {id_potravina : ttk.Entry} na canvase diety
        
        self.nazov_prvok_label = {} # {id_potravina : ttk.Label} na canvase diety
        self.tuky_prvok_label = {} # {id_potravina : ttk.Label} na canvase diety
        self.bielkoviny_prvok_label = {} # {id_potravina : ttk.Label} na canvase diety
        self.sacharidy_prvok_label = {} # {id_potravina : ttk.Label} na canvase diety
        
            # --------------------- premenne pre spravu potravin ----------------
            
        self.view_for_the_first_time = True # zobrazenie zoznamu potravin sa vykonava po prvy krat
        
        # ====================== konie inicializacie premennych =========================
        
        # ================== nastavenie grid root window =============
        
        self.root.columnconfigure(0, weight = 1)
        self.root.rowconfigure(0, weight = 1)
        
        # =============== koniec nastavenia grid root window ==========
        
        # ==================== Frames =================================
            # ---------- Frame rozdelenie -----------------------------
            
        self.main_frame_rozdelenie = Frames.MainFrameRozdelenie(self.root)
        
            # ---------- Koniec Frame rozdelenie -----------------------------
            
            # ---------- Frame sprava frames------------------------------------
        
        self.main_frame_sprava = Frames.MainFrameSprava(self.root)
        
            # ---------- Koniec Frame sprava frames ------------------------------------
            
            # --------- main Frame frames -------------------------
        
        self.main_frame = Frames.MainFrame(self.root)
        self.sub_frame_udaje = Frames.SubFrameUdaje(self.main_frame)
        
            # ---------- Koniec main Frame frames ----------------------------
            
        # =================== Koniec frames ==============================
        
        # =============== Nastavenie stylov ===============
        
        self.style = ttk.Style(self.root)
        
            # -------------- hlavicky stlpcov tabulky zoznamu potravin----------------
            
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", font = ("Verdana", 14), background = "lightgrey")
        
            # -------------- Koniec stylov hlavicky tabulky --------------------------
        
        # =============== Koniec nastavenia stylov ========
        
        
    def menu(self):
        '''
            Zobrazi hlavnu ponuku (menu programu)
        '''
        # ==== pas menu okna ==============================
        
        menubar = tk.Menu(self.root)
        self.root.config(menu = menubar)
        
        # =================================================
        
        # ====== Prve menu s nazvom Menu ==================
        
        self.menu_menu = tk.Menu(menubar, tearoff = False)
        
        self.menu_menu.add_command(
            label = "Zobraz všetky potraviny",
            command = self.zobraz_vsetky
        )
        
        self.menu_menu.add_command(
            label = "Vyber dietu",
            command = self.controller.vyber_dietu_dialog
        )

        self.menu_menu.add_command(
            label = "Vytvor dietu",
            command = self.vytvor_dietu
        )
        
        self.menu_menu.add_command(
            label = "Zmaž dietu",
            command = self.controller.zmaz_dietu_dialog
        )
        
        self.menu_menu.add_separator()
        
        self.menu_menu.add_command(
            label = "Návrh diety",
            command = self.zobraz_navrh_diety
        )
        
        self.menu_menu.add_command(
            label = "Rozdelenie do jedál",
            command = self.zobraz_rozdelenie
        )
        
        self.menu_menu.add_separator()
        
        self.menu_menu.add_command(
            label = "Správa potravín",
            command = self.zobraz_spravu_potravin
        )
        
        self.menu_menu.add_separator()
        
        self.menu_menu.add_command(
            label = "Ukončiť program",
            command = self.root.destroy
        )
        
        menubar.add_cascade(
            label = "Menu",
            menu = self.menu_menu
        )
        
        # --------------- Koniec prveho menu s nazvom Menu --------------
        
        # --------------- Menu s nazvom Uloz dietu -----------------
        
        self.do_suboru_menu = tk.Menu(menubar, tearoff = False)
        
        self.pdf_sub_menu = tk.Menu(self.do_suboru_menu, tearoff = False)
        
        self.pdf_sub_menu.add_command(
            label = "Krátky výpis do pdf suboru",
            command = self.kratky_v_do_pdf
        )
        
        self.pdf_sub_menu.add_command(
            label = "Celkový výpis do pdf suboru",
            command = self.celkovy_v_do_pdf
        )
        
        self.txt_sub_menu = tk.Menu(self.do_suboru_menu, tearoff = False)
        
        self.txt_sub_menu.add_command(
            label = "Krátky výpis do textového suboru",
            command = self.kratky_v_do_txt
        )
        
        self.txt_sub_menu.add_command(
            label = "Celkový výpis do textového suboru",
            command = self.celkovy_v_do_txt
        )
        
        self.do_suboru_menu.add_cascade(
            label = "Dieta do pdf súboru",
            menu = self.pdf_sub_menu,
            state = 'disabled'
        )
        
        self.do_suboru_menu.add_cascade(
            label = "Dieta do textového súboru",
            menu = self.txt_sub_menu,
            state = 'disabled'
        )
        
        menubar.add_cascade(
            label = "Ulož dietu",
            menu = self.do_suboru_menu
        )
        
        # --------------- Koniec menu s nazom Uloz dietu ----------
        
        # -------------- Menu s nazvom Pomoc ---------------------
        
        help_menu = tk.Menu(menubar, tearoff = False)
        
        help_menu.add_command(
            label = "O programe Energia",
            command = self.zobraz_credits
        )
        
        menubar.add_cascade(
            label = "Pomoc",
            menu = help_menu
        )
        
        # -------------- Koniec Menu s nazvom Pomoc --------------
        
    # ================ koniec def menu ======================
    
    # ================= metody menu =========================
    
    def zobraz_vsetky(self):
        self.entry.delete(0, 'end')
        self.combo.current(0)
        self.controller.zobraz_vsetky()
        
        #---------------- Zobraz credits -------------
        
    def zobraz_credits(self):
        Okna.OknoPreCredits(self.root)
        
        # -------------- Zobraz spravu potravin ---------------------
        
    def zobraz_spravu_potravin(self):
        self.controller.zablokuj_pridanie_do_suboru()
        self.disable_menu_items()
        self.main_frame_sprava.tkraise()
        self.controller.zobraz_sprava_combo()
        self.add_sprava_entry()
        self.add_canvas_potravin()
        self.controller.sprava_zobraz_vsetky()
        
        # -------------- Zobraz navrh diety ---------------------
    
    def zobraz_navrh_diety(self):
        self.menu_menu.entryconfig("Zobraz všetky potraviny", state = "normal")
        self.menu_menu.entryconfig("Vyber dietu", state = "normal")
        self.menu_menu.entryconfig("Vytvor dietu", state = "normal")
        self.menu_menu.entryconfig("Zmaž dietu", state = "normal")
        if self.controller.global_id_diety != 0:    
            self.controller.odblokuj_pridanie_do_suboru()
        else:
            self.controller.zablokuj_pridanie_do_suboru()
        self.main_frame.tkraise()
    
        # ---------------- Zobraz rozdelenie do jedal ------------
        
    def zobraz_rozdelenie(self):
        if self.controller.global_id_diety != 0:    
            self.controller.odblokuj_pridanie_do_suboru()
        else:
            self.controller.zablokuj_pridanie_do_suboru()
        self.disable_menu_items()
        self.zobraz_hlavicku_jedal()
        self.zobraz_canvas_priradenia()
        self.zobraz_canvas_zoznam_jedal()
        self.controller.data_pre_canvas_priradenia()
        self.controller.zobraz_zoznam_jedal()
        self.main_frame_rozdelenie.tkraise()
        
        # -------------- Kratky vypis do pdf suboru ------------------
    
    def kratky_v_do_pdf(self):
        cesta_a_subor_pdf = self.daj_subor_pdf()
        if cesta_a_subor_pdf != '':
            self.vytvor_objekt_pdf()
            self.vytvor_kratky_pdf()
            self.uloz_a_otvor_subor_pdf(cesta_a_subor_pdf)
        
        # -------------- Celkovy vypis do pdf suboru ------------------
    
    def celkovy_v_do_pdf(self):
        cesta_a_subor_pdf = self.daj_subor_pdf()
        if cesta_a_subor_pdf != '':
            self.vytvor_objekt_pdf()
            self.vytvor_celkovy_pdf()
            self.uloz_a_otvor_subor_pdf(cesta_a_subor_pdf)
        
        # ------------- Kratky vypis do textoveho suboru --------------
    
    def kratky_v_do_txt(self):
        cesta_a_subor_txt = self.daj_subor_txt()
        if cesta_a_subor_txt != '':
            self.otvor_txt_pre_zapis(cesta_a_subor_txt)
            self.vytvor_kratky_txt()
            self.zatvor_txt()
            self.otvor_subor_txt(cesta_a_subor_txt)
          
        # ------------- Celkovy vypis do textoveho suboru --------------
    
    def celkovy_v_do_txt(self):
        cesta_a_subor_txt = self.daj_subor_txt()
        if cesta_a_subor_txt != '':
            self.otvor_txt_pre_zapis(cesta_a_subor_txt)
            self.vytvor_celkovy_txt()
            self.zatvor_txt()
            self.otvor_subor_txt(cesta_a_subor_txt)
            
        # -------------- metoda na disable menu items -----------------
        
    def disable_menu_items(self):
        self.menu_menu.entryconfig("Zobraz všetky potraviny", state = "disabled")
        self.menu_menu.entryconfig("Vyber dietu", state = "disabled")
        self.menu_menu.entryconfig("Vytvor dietu", state = "disabled")
        self.menu_menu.entryconfig("Zmaž dietu", state = "disabled")
        
    # ================= koniec metod menu ==================
    
    
    # ==========================================================================
    # ==================             ===========================================
    # ================== Navrh diety ===========================================
    # ==================             ===========================================
    # ==========================================================================
    
    
    # ================= okno zoznamu potravin ===================
    
    def okno_zoznamu (self, height, columns, column_names, data):
        '''
            zobrazi tabulku so zoznamom potravin
            a nutricnymi hodnotami
            
        '''
        if not hasattr(self, "zoznam"):# ak tabulka s framemom zoznam neexistuje vytvor ju
            self.zoznam = ttk.Treeview(self.main_frame,
                columns = columns,
                show = 'headings',
                height = height,
                selectmode = "browse"
            )
            
            self.zoznam['displaycolumns'] = ('nazov', 'sacharidy', 'tuky', 'bielkoviny')
            
            # ======== styly tabulky zoznamu ===========================================
            
                # ----------- velkost pisma a pozadie data ----------------------------
            
            self.zoznam.tag_configure ('parne', background = "#AAAAAA", font = ("Verdana", 12))
            self.zoznam.tag_configure ('neparne', background = "#888888", font = ("Verdana", 12))
            
            # ====================== koniec stylov ==================================
            
            for i, column in enumerate(columns):    
                self.zoznam.heading(column, text = column_names[i])
                if i > 1:
                    self.zoznam.column(column, width = 50, anchor = 'e')
                else:
                    self.zoznam.column(column, width = 300)
               
            self.add_lines_to_zoznam(data)
            
            # ---------------------- scrollbar pre okno zoznamu -----------------------
            
            grid_attr = {'row' : 1, 'column' : 2, 'rowspan' : 2, 'sticky' : 'ns', 'pady' : (0, 10)}
            
            self.add_scrollbar(self.main_frame, self.zoznam, **grid_attr)
            
            # ----------------------- end scrollbar -------------------------------------
            
            # ------------------- Priradenie eventu select item -------------------------
            
            self.zoznam.bind('<<TreeviewSelect>>', self.controller.zobraz_pridavaci_dialog)
            
            # ------------------- Priradenie eventu select item -------------------------
            
            self.zoznam.grid(row = 1, column = 0, rowspan = 2, columnspan = 2, padx = (10, 0), pady = (0, 10), sticky = "nswe")
            
        else:# ak tabulka s frameom zoznam_potravin existuje zmaz v nej data a napln ju novymi
            for line in self.zoznam.get_children():
                self.zoznam.delete(line)
            
            self.add_lines_to_zoznam(data)    
    
    def add_lines_to_zoznam(self, data):
        for idx, line in enumerate(data):
            if (idx % 2) == 0:
                self.zoznam.insert('', tk.END, values = line, tags = "parne")
            else:
                self.zoznam.insert('', tk.END, values = line, tags = "neparne")
                
    # ============== Koniec okno_zoznamu =========================================
    
    # ======= entry pre vyhladanie konkretnej potraviny ===============================
    
    def add_entry (self):
        self.zadany_retazec = tk.StringVar()
        self.entry = ttk.Entry(self.main_frame, textvariable = self.zadany_retazec, font = ("Verdana", 12))
        self.entry.focus()
        self.entry.grid(row = 0, column = 1, ipady = 3, pady = 5, sticky = 'ew')
        self.zadany_retazec.trace('w', self.controller.zobraz_podla_retazca)
        self.entry.bind("<FocusIn>", self.controller.entry_focusin)
       
    # =============== Koniec add_entry ===============================================
       
    # ============= Combobox pre zadanie kategorie jedla =============================
       
    def add_combo (self, data):
        self.vybrana_kategoria = tk.StringVar()
        self.combo = ttk.Combobox(self.main_frame, textvariable = self.vybrana_kategoria, font = ("Verdana", 12))
        self.combo['state'] = 'readonly'
        self.combo['values'] = data
        self.combo.current(0)
        self.combo.grid (row = 0, column = 0, padx = 10, pady = 5, ipady = 3, sticky = 'ew')
        self.combo.bind('<<ComboboxSelected>>', self.controller.zobraz_podla_kategorie)
        
    # ============ Koniec add_combo ==================================================
    
    # ============ Canvas pre dietu (zoznam diety) ===========================================
    
    # -------------- zobraz canvas_diety -----------------
    
    def add_canvas_diety (self):
        self.canvas_diety = tk.Canvas(self.main_frame)
        
        self.canvas_diety.grid(row = 2, column = 3, padx = 10, pady = (0, 10), sticky = 'nswe')
        
        # --------------------- scrollbar pre canvas diety ---------------------------------
            
        grid_attr = {'row' : 2, 'column' : 4, 'sticky' : 'ns'}
            
        self.add_scrollbar(self.main_frame, self.canvas_diety, **grid_attr)
            
        # ---------------------- end scrollbar pre canvas diety -------------------------------
    
    # --------------- Pridaj na canvas_diety potravinu --------------
    
    def pridaj_potravinu_na_canvas_diety(self, data):
        
        # data[0] -> id_potravina
        # data[1] -> nazov
        # data[2] -> sacharidy
        # data[3] -> tuky
        # data[4] -> bielkoviny
        # data[5] -> mnozstvo
        
        mnozstvo = data[5]
        if mnozstvo == None:
                mnozstvo = 0
                
        id_potravina = data[0]
        
        self.canvas_text_y += 50
        
        self.canvas_diety.configure(scrollregion = (0, 0, 600, self.canvas_text_y + 50))
        
        
        self.nazov_prvok_label[id_potravina] = ttk.Label(self.canvas_diety, text = data[1], wraplength = 300, cursor = "hand2", font = ("Verdana, 12"), background = "#ffffff", anchor= 'nw')
        self.canvas_diety.create_window((15, self.canvas_text_y), window = self.nazov_prvok_label[id_potravina], anchor = 'nw')
        self.nazov_prvok_label[id_potravina].bind("<Button-1>", lambda event, id_potravina = data[0], nazov = data[1] : self.prever_zmazanie_prvku_diety(event, id_potravina, nazov))
        
        self.sacharidy_prvok_label[id_potravina] = ttk.Label(self.canvas_diety,  text = "S: " + str(data[2]) + " g", background = "#ffffff", font = ("Verdana, 12"), anchor= 'nw')
        self.canvas_diety.create_window((320, self.canvas_text_y), window = self.sacharidy_prvok_label[id_potravina], anchor = 'nw')
        
        self.tuky_prvok_label[id_potravina] = ttk.Label(self.canvas_diety, text = "T: " + str(data[3]) + " g", font = ("Verdana, 12"), background = "#ffffff", anchor= 'nw')
        self.canvas_diety.create_window((410, self.canvas_text_y), window = self.tuky_prvok_label[id_potravina], anchor = 'nw')
        
        self.bielkoviny_prvok_label[id_potravina] = ttk.Label(self.canvas_diety,  text = "B: " + str(data[4]) + " g", background = "#ffffff", font = ("Verdana, 12"), anchor= 'nw')
        self.canvas_diety.create_window((500, self.canvas_text_y), window = self.bielkoviny_prvok_label[id_potravina], anchor = 'nw')
        
        self.canvas_entry_mnozstvo[id_potravina] = tk.StringVar()
        
        self.canvas_entry[id_potravina] = ttk.Entry(self.canvas_diety,
                width = 5,
                textvariable = self.canvas_entry_mnozstvo[id_potravina],
                font = "Verdana 12"
        )
        
        self.canvas_entry[id_potravina].insert(0, mnozstvo)
        
        self.canvas_diety.create_window((590, self.canvas_text_y), window = self.canvas_entry[id_potravina], anchor='nw')
        
        
        self.canvas_entry_mnozstvo[id_potravina].trace('w', 
            lambda var, index, mode, id_potravina = id_potravina : self.controller.uloz_udaj_mnozstva(var, index, mode, id_potravina)
            )
        
        self.canvas_diety.create_text( (650, self.canvas_text_y), text = "g", font = "Verdana 12", anchor="nw")
        
    # -------------- vypln canvas_diety vsetkymi potravinami z diety ----------------
        
    def vypln_canvas_diety(self, zoznam):
        for data in zoznam:
            self.pridaj_potravinu_na_canvas_diety(data)
        
    # -------------- zmaz canvas_diety ----------------------
    
    def zmaz_canvas_diety(self):
        for objekt in self.nazov_prvok_label.values():
            objekt.destroy()
            
        for objekt in self.tuky_prvok_label.values():
            objekt.destroy()
        
        for objekt in self.bielkoviny_prvok_label.values():
            objekt.destroy()
        
        for objekt in self.sacharidy_prvok_label.values():
            objekt.destroy()
            
        for objekt in self.canvas_entry.values():
            objekt.destroy()
            
        self.canvas_diety.delete('all')
        self.canvas_text_y = 0
        
        self.canvas_entry.clear()
        self.canvas_entry_mnozstvo.clear()
        self.nazov_prvok_label.clear()
        self.tuky_prvok_label.clear()
        self.bielkoviny_prvok_label.clear()
        self.sacharidy_prvok_label.clear()
        
    # ============ Koniec Canvas pre dietu ===========================================
    
    # ================== Zobraz frame udajov =======================================
    
    def add_frame_udajov (self):
        
        # ------------- Nadpisy vo frame udajov -----------------
        
        self.nazov_diety_nadpis = ttk.Label(self.sub_frame_udaje, text = "-- Žiadna dieta --", font = "Verdana, 14")
        self.nazov_diety_nadpis.grid(row = 0, column = 0, columnspan = 5)
        
        font = ("Verdana", 12)
        padding_x = (10, 0)
        
        ttk.Label(self.sub_frame_udaje,
            text = "Množstvo tuku:",
            font = font
        ).grid(row = 1, column = 0, padx = padding_x, sticky = "w")
        
        ttk.Label(self.sub_frame_udaje,
            text = "Množstvo bielkovin:",
            font = font
        ).grid(row = 2, column = 0, padx = padding_x, sticky = "w")
        
        ttk.Label(self.sub_frame_udaje,
            text = "Množstvo sacharidov:",
            font = font
        ).grid(row = 3, column = 0, padx = padding_x, sticky = "w")
        
        ttk.Label(self.sub_frame_udaje,
            text = "Celková energia:",
            font = font
        ).grid(row = 4, column = 0, padx = padding_x, sticky = "w")
        
        # ---------------- Koniec nadpisov vo frame udajov -------------------------------
        
        # ----------------- Hodnoty pre nadpisy vo frame udajov --------------------------
        
        self.hod_mn_tuku = ttk.Label(self.sub_frame_udaje, text = "- g")
        self.hod_mn_tuku['font'] = font
        self.hod_mn_tuku.grid(row = 1, column = 1, sticky = "w")
        
        self.hod_mn_bielkovin = ttk.Label(self.sub_frame_udaje, text = "- g")
        self.hod_mn_bielkovin['font'] = font
        self.hod_mn_bielkovin.grid(row = 2, column = 1, sticky = "w")
        
        self.hod_mn_sacharidov = ttk.Label(self.sub_frame_udaje, text = "- g")
        self.hod_mn_sacharidov['font'] = font
        self.hod_mn_sacharidov.grid(row = 3, column = 1, sticky = "w")
        
        self.hod_celk_energia = ttk.Label(self.sub_frame_udaje, text = "- kJ")
        self.hod_celk_energia['font'] = font
        self.hod_celk_energia.grid(row = 4, column = 1, sticky = "w")
        
            # ----------------- Odporucane hodnoty T B S -----------------------------------
            
        self.odp_hod_mn_tuku = ttk.Label(self.sub_frame_udaje, text = "(- g)", foreground = '#666666')
        self.odp_hod_mn_tuku['font'] = font
        self.odp_hod_mn_tuku.grid(row = 1, column = 2, sticky = "w")
        
        self.odp_hod_mn_bielkovin = ttk.Label(self.sub_frame_udaje, text = "(- g)", foreground = '#666666')
        self.odp_hod_mn_bielkovin['font'] = font
        self.odp_hod_mn_bielkovin.grid(row = 2, column = 2, sticky = "w")
        
        self.odp_hod_mn_sacharidov = ttk.Label(self.sub_frame_udaje, text = "(- g)", foreground = '#666666')
        self.odp_hod_mn_sacharidov['font'] = font
        self.odp_hod_mn_sacharidov.grid(row = 3, column = 2, sticky = "w")
            
            # ----------------- Koniec Odporucane hodnoty T B S ----------------------------
    
        # ----------------- Koniec hodnot pre nadpisy vo frame udajov --------------------------
        
        # ---------------- Hodnoty straty tuku pri diete --------------------------------------
           
            # ----------------- Nadpisy --------------------------
        ttk.Label(self.sub_frame_udaje,
            text = "Denná spotreba energie (kJ):",
            font = font
        ).grid(row = 1, column = 3, sticky = "w")
        
        ttk.Label(self.sub_frame_udaje,
            text = "Denná strata tuku:",
            font = font
        ).grid(row = 2, column = 3, sticky = "w")
        
        ttk.Label(self.sub_frame_udaje,
            text = "Týždenná strata tuku:",
            font = font
        ).grid(row = 3, column = 3, sticky = "w")
        
        ttk.Label(self.sub_frame_udaje,
            text = "Mesačna strata tuku (30 dni):",
            font = font
        ).grid(row = 4, column = 3, sticky = "w")
        
        ttk.Label(self.sub_frame_udaje,
            text = "Ročná strata tuku:",
            font = font
        ).grid(row = 5, column = 3, sticky = "w")
        
            # ------------------------ Hodnoty pre nadpisy ---------------------
        
        self.hodnota_den_spotr_energ = tk.StringVar()
        self.hodnota_den_spotr_energ.trace('w', self.controller.vypocitaj_stratu_tuku)
        self.denna_spotreba_energie = ttk.Entry(self.sub_frame_udaje, width = 5, textvariable = self.hodnota_den_spotr_energ)
        self.denna_spotreba_energie['font'] = font
        self.denna_spotreba_energie.grid(row = 1, column = 4, sticky = "w")
        self.denna_spotreba_energie.insert(0, self.root.denna_spotreba_energie)
        
        
        self.strata_tuku_den = ttk.Label(self.sub_frame_udaje, text = "- g")
        self.strata_tuku_den['font'] = font
        self.strata_tuku_den.grid(row = 2, column = 4, sticky = "w")
        
        self.strata_tuku_tyzden = ttk.Label(self.sub_frame_udaje, text = "- g")
        self.strata_tuku_tyzden['font'] = font
        self.strata_tuku_tyzden.grid(row = 3, column = 4, sticky = "w")
        
        self.strata_tuku_mesiac = ttk.Label(self.sub_frame_udaje, text = "- g")
        self.strata_tuku_mesiac['font'] = font
        self.strata_tuku_mesiac.grid(row = 4, column = 4, sticky = "w")
        
        self.strata_tuku_rok = ttk.Label(self.sub_frame_udaje, text = "- g")
        self.strata_tuku_rok['font'] = font
        self.strata_tuku_rok.grid(row = 5, column = 4, sticky = "w")
        
         # ----------------Koniec Hodnoty straty tuku pri diete --------------------------------------
    # ================== Koniec zobraz frame udajov ================================
    
    # =================== Zobraz okno pre potvrdenie prvku diety ===================
    
    def zobraz_okno_pre_potvrdenie_prvku(self, potravina):
        self.okno_pre_potvrdenie_prvku = Okna.OknoPrePrvokDiety(self.root)
        
        self.okno_pre_potvrdenie_prvku.nazov_potraviny_label['text'] = potravina
        
        self.text_nazov_diety = tk.StringVar()
        self.okno_pre_potvrdenie_prvku.nazov_diety_entry['textvariable'] = self.text_nazov_diety
       
        self.okno_pre_potvrdenie_prvku.nazov_diety_entry.insert(0, self.controller.global_nazov_diety)
        
        self.okno_pre_potvrdenie_prvku.button_nie['command'] = self.okno_pre_potvrdenie_prvku.destroy
        self.okno_pre_potvrdenie_prvku.button_ano['command'] = self.controller.pridaj_prvok_diety
        
    # ================== Koniec zobrazenia okna pre potvrdenie prvku diety =========
    
    # ===================== Zobrazenie udajov diety sumar aj jednotlivo =====================
    
    def nastav_jednotlive_hodnoty(self, id_potravina, sacharidy, tuky, bielkoviny):
        self.tuky_prvok_label[id_potravina]["text"] = "T: " + str(tuky) + ' g'
        self.bielkoviny_prvok_label[id_potravina]["text"] = "B: " + str(bielkoviny) + ' g'
        self.sacharidy_prvok_label[id_potravina]["text"] = "S: " + str(sacharidy) + ' g'
        
    def nastav_celkove_hodnoty(self, celk_energia_kj, celk_sacharidy, celk_tuky, celk_bielkoviny):
        self.hod_mn_tuku["text"] = str(celk_tuky) + ' g'
        self.hod_mn_bielkovin["text"] = str(celk_bielkoviny) + ' g'
        self.hod_mn_sacharidov["text"] = str(celk_sacharidy) + ' g'
        self.hod_celk_energia["text"] = str(celk_energia_kj) + ' kJ'
    
    def nastav_odp_celkove_hodnoty(self, odp_celk_sacharidy, odp_celk_tuky, odp_celk_bielkoviny):
        self.odp_hod_mn_tuku["text"] = "(" + str(odp_celk_tuky) + ' g)'
        self.odp_hod_mn_bielkovin["text"] = "(" + str(odp_celk_bielkoviny) + ' g)'
        self.odp_hod_mn_sacharidov["text"] = "(" + str(odp_celk_sacharidy) + ' g)'
    
    def nastav_stratu_tuku (self, den, tyzden, mesiac, rok):
        self.strata_tuku_den["text"] = str(den) + ' g'
        self.strata_tuku_tyzden["text"] = str(tyzden) + ' g'
        self.strata_tuku_mesiac["text"] = str(mesiac) + ' g'
        self.strata_tuku_rok["text"] = str(rok) + ' g'
    
    # ===================== Koniec Zobrazenie udajov diety sumar aj jednotlivo aj odporucane =====================
    
    # ==================== Zobraz dialog vyberu diety zo zoznamu diet ===============================
    
    def zobraz_dialog_diet(self, data, fnc):
        self.okno_vyberu_diety = Okna.OknoPreVyberDiety(self.root)
        
        if fnc == 'vyber':
            titulok = "Výber diety"
            nadpis = "Načítajte dietu"
        elif fnc == 'zmaz':
            titulok = "Zmazanie diety"
            nadpis = "Zmažte dietu"
            
        self.okno_vyberu_diety.title(titulok)
        self.okno_vyberu_diety.nadpis["text"] = nadpis
        
        canvas_okna_vyberu_diety = tk.Canvas(self.okno_vyberu_diety, background = "#ffffff")
        
        canvas_okna_vyberu_diety.grid(row = 2, column = 0, sticky = 'nswe')
        
        # --------------------- scrollbar pre canvas vyberu diety ---------------------------------
            
        grid_attr = {'row' : 2, 'column' : 1, 'sticky' : 'ns'}
            
        self.add_scrollbar(self.okno_vyberu_diety, canvas_okna_vyberu_diety, **grid_attr)
            
        # riadok[0] -> id_dieta
        # riadok[1] -> nazov_diety
        # riadok[2] -> celk_tuky
        # riadok[3] -> celk_sacharidy
        # riadok[4] -> celk_bielkoviny
        # riadok[5] -> celk_energia
        # riadok[6] -> ts = datetime.datetime(2023, 7, 23, 19, 6, 49) 
        
        # datum = str(datetime.datetime(2023, 7, 23, 19, 6, 49))
        # print(datum[8:10] + '.' + datum[5:7] + ' ' + datum[0:4] + " " + datum[11:])
        
        font_popis = "Verdana 13 bold"
        frame = ttk.Frame(self.okno_vyberu_diety)
        frame.grid(row = 1, column = 0, columnspan = 2, sticky = 'nswe')
        
        ttk.Label(frame, text = "Názov diety", font = font_popis).place(x = 50, y = 5)
        ttk.Label(frame, text = "Tuky", font = font_popis).place(x = 260, y = 5)
        ttk.Label(frame, text = "Bielkoviny", font = font_popis).place(x = 350, y = 5)
        ttk.Label(frame, text = "Sacharidy", font = font_popis).place(x = 470, y = 5)
        ttk.Label(frame, text = "Energia", font = font_popis).place(x = 590, y = 5)
        ttk.Label(frame, text = "Dátum vzniku", font = font_popis).place(x = 700, y = 5)
       
        text_y = 0
        
        for riadok in data:
            text_y += 50
            riadok = list(riadok)
            
            if fnc == 'vyber':
                funkcia = lambda event, id_dieta = riadok[0] : self.controller.nacitaj_dietu(event, id_dieta)
            elif fnc == 'zmaz':
                funkcia = lambda event, id_dieta = riadok[0], nazov_diety = riadok[1]: self.prever_zmazanie_diety(event, id_dieta, nazov_diety)
               
            label_nazov_diety = ttk.Label(canvas_okna_vyberu_diety, text = riadok[1], wraplength = 150, cursor = "hand2", background = "#ffffff", font = ("Verdana, 12"), anchor= 'nw')
            canvas_okna_vyberu_diety.create_window((50, text_y), window = label_nazov_diety, anchor = 'nw')
            label_nazov_diety.bind('<Button-1>', funkcia)
            
            
            if riadok[2] == None: 
                riadok.insert(2, 0.0)
            label_pre_tuky = ttk.Label(canvas_okna_vyberu_diety, text = str(riadok[2]) + ' g', wraplength = 100, background = "#ffffff", font = ("Verdana, 12"), anchor= 'nw')
            canvas_okna_vyberu_diety.create_window((260, text_y), window = label_pre_tuky, anchor = 'nw')
            
            if riadok[4] == None: 
                riadok.insert(4, 0.0)
            label_pre_bielkoviny = ttk.Label(canvas_okna_vyberu_diety, text = str(riadok[4]) + ' g', wraplength = 100, background = "#ffffff", font = ("Verdana, 12"), anchor= 'nw')
            canvas_okna_vyberu_diety.create_window((360, text_y), window = label_pre_bielkoviny, anchor = 'nw')
            
            if riadok[3] == None: 
                riadok.insert(3, 0.0)
            label_pre_sacharidy = ttk.Label(canvas_okna_vyberu_diety, text = str(riadok[3]) + ' g', wraplength = 100, background = "#ffffff", font = ("Verdana, 12"), anchor= 'nw')
            canvas_okna_vyberu_diety.create_window((480, text_y), window = label_pre_sacharidy, anchor = 'nw')
            
            if riadok[5] == None: 
                riadok.insert(5, 0.0)
            label_pre_energiu = ttk.Label(canvas_okna_vyberu_diety, text = str(round(riadok[5])) + ' kJ', wraplength = 100, background = "#ffffff", font = ("Verdana, 12"), anchor= 'nw')
            canvas_okna_vyberu_diety.create_window((600, text_y), window = label_pre_energiu, anchor = 'nw')
            
            if riadok[6] == None: 
                datum = "-"
            else:
                datum = str(riadok[6])
                datum = datum[8:10] + '.' + datum[5:7] + ' ' + datum[0:4] + " " + datum[11:]
            
            label_pre_ts = ttk.Label(canvas_okna_vyberu_diety, text = datum, background = "#ffffff", font = ("Verdana, 12"), anchor= 'nw')
            canvas_okna_vyberu_diety.create_window((720, text_y), window = label_pre_ts, anchor = 'nw')
            
        canvas_okna_vyberu_diety.configure(scrollregion = (0, 0, 900, text_y + 50))
        
        ttk.Button(self.okno_vyberu_diety, text = "Zrušiť", command = self.okno_vyberu_diety.destroy).grid(row = 3, column = 0, columnspan = 2, pady = 20)
        
    # ==================== Koniec Zobraz dialog vyberu diety zo zoznamu diet ===============================
    
    # ==================== Vytvor dietu ==============================================
    
    def vytvor_dietu(self):
        self.okno_pre_vytvorenie_diety = Okna.OknoPreVytvorenieDiety(self.root)
        
        nazov_diety_pre_vytvorenie = tk.StringVar()
        
        self.okno_pre_vytvorenie_diety.nazov_diety_entry["textvariable"] = nazov_diety_pre_vytvorenie
        self.okno_pre_vytvorenie_diety.button_uloz["command"] = lambda nazov_diety_stringvar = nazov_diety_pre_vytvorenie : self.controller.vytvor_dietu(nazov_diety_stringvar)
        
    # ==================== Koniec Vytvor dietu ==============================================
    
    # =================== Nastav nadpis diety ================================
    
    def nastav_nadpis_diety(self):
        self.nazov_diety_nadpis['text'] = "Názov diety: " + self.controller.global_nazov_diety
    
    # ================ Koniec nadpis diety ====================================
    
    # ============== Vynuluj nadpis diety a frame udajov =======================================
    
    def zmaz_nadpis_diety(self):
        self.nazov_diety_nadpis['text'] = "-- Žiadna dieta --"
    
    def zmaz_frame_udajov(self):
        self.hod_mn_tuku["text"] ='- g'
        self.hod_mn_bielkovin["text"] = '- g'
        self.hod_mn_sacharidov["text"] = '- g'
        self.hod_celk_energia["text"] = '- kJ'
        
        self.odp_hod_mn_tuku["text"] = '(- g)'
        self.odp_hod_mn_bielkovin["text"] = '(- g)'
        self.odp_hod_mn_sacharidov["text"] = '(- g)'
        
        self.strata_tuku_den["text"] = '- g'
        self.strata_tuku_tyzden["text"] = '- g'
        self.strata_tuku_mesiac["text"] = '- g'
        self.strata_tuku_rok["text"] = '- g'
        
    # ============== Koniec Vynuluj nadpis diety a frame udajov =======================================
    
    # ===================== Zmazanie diety a prvku diety ========================================
    
    def prever_zmazanie_diety(self, event, id_dieta, nazov_diety):
        okno_potvrd = Okna.OknoDialogPotvrdenia(self.okno_vyberu_diety)
        okno_potvrd.nadpis["text"] = "Naozaj chcete zmazat dietu " + nazov_diety + " ?"
        
        okno_potvrd.button_ano['command'] = lambda id_dieta = id_dieta : self.controller.zmaz_dietu(id_dieta)
    
    def prever_zmazanie_prvku_diety(self, event, id_potravina, nazov):
        self.okno_potvrd_zmaz_prvku = Okna.OknoDialogPotvrdenia(self.root)
        self.okno_potvrd_zmaz_prvku.nadpis["text"] = "Naozaj chcete zmazat potravinu " + nazov + " ?"
        
        self.okno_potvrd_zmaz_prvku.button_ano['command'] = lambda id_potravina = id_potravina : self.controller.zmaz_prvok_diety(id_potravina)
    
    # ==================== Koniec Zmazanie diety a prvku diety =======================================


    # ==========================================================================
    # ==================                 =======================================
    # ================== Sprava potravin =======================================
    # ==================                 =======================================
    # ==========================================================================


    # ===================== Pridaj combo =======================================
    
    def add_sprava_combo(self, data, parent, func):
        self.sprava_vybrana_kategoria = tk.StringVar()
        self.sprava_combo = ttk.Combobox(parent, textvariable = self.sprava_vybrana_kategoria, font = ("Verdana", 12))
        self.sprava_combo['state'] = 'readonly'
        self.sprava_combo['values'] = data
        self.sprava_combo.current(0)
        self.sprava_combo.grid (row = 0, column = 0, padx = 10, pady = 5, ipady = 3, sticky = 'ew')
        self.sprava_combo.bind('<<ComboboxSelected>>', func)
    
    # ===================== Koniec Pridaj combo =======================================

    # ===================== Pridaj entry ===============================================

    def add_sprava_entry(self):
        self.sprava_zadany_retazec = tk.StringVar()
        self.sprava_entry = ttk.Entry(self.main_frame_sprava, textvariable = self.sprava_zadany_retazec, font = ("Verdana", 12))
        self.sprava_entry.focus()
        self.sprava_entry.grid(row = 0, column = 1, ipady = 3, pady = 5, sticky = 'ew')
        self.sprava_zadany_retazec.trace('w', callback = self.controller.sprava_zobraz_podla_retazca)
        self.sprava_entry.bind("<FocusIn>", self.controller.sprava_entry_focusin)
        
    # ===================== Koniec Pridaj entry ===============================================
    
    # ============ Canvas pre potraviny (zoznam potravin) ===========================================
    
        # -------------- zobraz canvas_potravin -----------------
    
    def add_canvas_potravin (self):
        self.canvas_potravin = tk.Canvas(self.main_frame_sprava)
        
        self.canvas_potravin.grid(row = 1, column = 0, columnspan = 3, sticky = 'nswe')
        
        # --------------------- scrollbar pre canvas potravin ---------------------------------
            
        grid_attr = {'row' : 1, 'column' : 3, 'sticky' : 'ns'}
            
        self.add_scrollbar(self.main_frame_sprava, self.canvas_potravin, **grid_attr)
            
        # ---------------------- end scrollbar pre canvas potravin -------------------------------
    
        # --------------- Zobraz potraviny na canvas potravin ------------------
    
    def sprava_zobraz_potraviny(self, data):
        with self.controller.lock:
            
            # riadok[0] -> id_potravina
            # riadok[1] -> id_kategoria_jedla
            # riadok[2] -> nazov
            # riadok[3] -> sacharidy
            # riadok[4] -> tuky
            # riadok[5] -> bielkoviny
            # riadok[6] -> ts
            
            if not self.view_for_the_first_time:
                self.destroy_canvas_potravin_objects()
            else:   
                self.view_for_the_first_time = False
            
            # ---------------------- Nastavenie vstupnych premennych --------------------------
            
            canvas_y_coor = 50
            
            self.canvas_potravin_entry_pre_nazov = {}
            self.stringvar_entry_nazov = {}
            
            self.canvas_potravin_entry_pre_sacharidy = {}
            self.stringvar_entry_sacharidy = {}
            
            self.canvas_potravin_entry_pre_tuky = {}
            self.stringvar_entry_tuky = {}
            
            self.canvas_potravin_entry_pre_bielkoviny = {}
            self.stringvar_entry_bielkoviny = {}
            
            self.canvas_potravin_combo = {}
            self.stringvar_combo = {}
            
            self.canvas_potravin_button_zmen = {}
            self.canvas_potravin_button_zmaz = {}
            
            # --------------------- Prvy riadok ktory je pre pridanie novej potraviny ---------
            
            # ----------------- entry nazov potraviny -------------------------------
               
            self.stringvar_entry_pridaj_nazov = tk.StringVar()
        
            self.canvas_potravin_entry_pre_pridaj_nazov = ttk.Entry(self.canvas_potravin,
                    width = 41,
                    textvariable = self.stringvar_entry_pridaj_nazov,
                    font = "Verdana 12"
            )
            
            self.canvas_potravin.create_window((20, canvas_y_coor), window = self.canvas_potravin_entry_pre_pridaj_nazov, anchor='nw')
            
            # ----------------- entry sacharidy -------------------------------
            
            self.canvas_potravin.create_text( (480, (canvas_y_coor + 2)), text = "S:", font = "Verdana 12", anchor="nw")
        
            self.stringvar_entry_pridaj_sacharidy = tk.StringVar()
        
            self.canvas_potravin_entry_pre_pridaj_sacharidy = ttk.Entry(self.canvas_potravin,
                    width = 5,
                    textvariable = self.stringvar_entry_pridaj_sacharidy,
                    font = "Verdana 12"
            )
        
            self.canvas_potravin.create_window((500, canvas_y_coor), window = self.canvas_potravin_entry_pre_pridaj_sacharidy, anchor='nw')
            
            # ----------------- entry tuky -------------------------------
            
            self.canvas_potravin.create_text( (580, (canvas_y_coor + 2)), text = "T:", font = "Verdana 12", anchor="nw")

            self.stringvar_entry_pridaj_tuky = tk.StringVar()
        
            self.canvas_potravin_entry_pre_pridaj_tuky = ttk.Entry(self.canvas_potravin,
                    width = 5,
                    textvariable = self.stringvar_entry_pridaj_tuky,
                    font = "Verdana 12"
            )
        
            self.canvas_potravin.create_window((600, canvas_y_coor), window = self.canvas_potravin_entry_pre_pridaj_tuky, anchor='nw')
            
            # ----------------- entry bielkoviny -------------------------------
            
            self.canvas_potravin.create_text( (680, (canvas_y_coor + 2)), text = "B:", font = "Verdana 12", anchor="nw")
           
            self.stringvar_entry_pridaj_bielkoviny = tk.StringVar()
        
            self.canvas_potravin_entry_pre_pridaj_bielkoviny = ttk.Entry(self.canvas_potravin,
                    width = 5,
                    textvariable = self.stringvar_entry_pridaj_bielkoviny,
                    font = "Verdana 12"
            )
        
            self.canvas_potravin.create_window((700, canvas_y_coor), window = self.canvas_potravin_entry_pre_pridaj_bielkoviny, anchor='nw')
            
            # ----------------- combo kategoria_potravin -------------------------------
            
            self.stringvar_combo_pridaj = tk.StringVar()
        
            self.canvas_potravin_combo_pridaj = ttk.Combobox(self.canvas_potravin,
                    values = self.controller.data_pre_combo(),
                    textvariable = self.stringvar_combo_pridaj,
                    state = "readonly",
                    font = "Verdana 12"
            )
            
            self.canvas_potravin.create_window((800, canvas_y_coor), window = self.canvas_potravin_combo_pridaj, anchor='nw')
            
            # ----------------- button Pridaj -------------------------------
           
            self.canvas_potravin_button_pridaj = tk.Button(self.canvas_potravin,
                    text = "Pridaj",
                    command = self.controller.sprava_pridaj_potravinu,
                    width = 8,
            )
            
            self.canvas_potravin_button_pridaj["font"] = font.Font(size = 12)
            self.canvas_potravin.create_window((1050, (canvas_y_coor - 2 )), window = self.canvas_potravin_button_pridaj, anchor='nw')
            
            # ---------------------- Ostatne riadky pre upravu potravin ----------------------
            
            for riadok in data:
                
                canvas_y_coor += 50
                self.canvas_potravin.configure(scrollregion = (0, 0, 900, canvas_y_coor + 50))
                
                # ----------------- entry nazov potraviny -------------------------------
                
                self.stringvar_entry_nazov[riadok[0]] = tk.StringVar()
            
                self.canvas_potravin_entry_pre_nazov[riadok[0]] = ttk.Entry(self.canvas_potravin,
                        width = 41,
                        textvariable = self.stringvar_entry_nazov[riadok[0]],
                        font = "Verdana 12"
                )
            
                self.canvas_potravin_entry_pre_nazov[riadok[0]].insert(0, riadok[2])
                self.canvas_potravin.create_window((20, canvas_y_coor), window = self.canvas_potravin_entry_pre_nazov[riadok[0]], anchor='nw')
                
                # ----------------- entry sacharidy -------------------------------
                
                self.canvas_potravin.create_text( (480, (canvas_y_coor + 2)), text = "S:", font = "Verdana 12", anchor="nw")
              
                self.stringvar_entry_sacharidy[riadok[0]] = tk.StringVar()
            
                self.canvas_potravin_entry_pre_sacharidy[riadok[0]] = ttk.Entry(self.canvas_potravin,
                        width = 5,
                        textvariable = self.stringvar_entry_sacharidy[riadok[0]],
                        font = "Verdana 12"
                )
            
                self.canvas_potravin_entry_pre_sacharidy[riadok[0]].insert(0, riadok[3])
                self.canvas_potravin.create_window((500, canvas_y_coor), window = self.canvas_potravin_entry_pre_sacharidy[riadok[0]], anchor='nw')
            
                # ----------------- entry tuky -------------------------------
                
                self.canvas_potravin.create_text( (580, (canvas_y_coor + 2)), text = "T:", font = "Verdana 12", anchor="nw")
                
                self.stringvar_entry_tuky[riadok[0]] = tk.StringVar()
            
                self.canvas_potravin_entry_pre_tuky[riadok[0]] = ttk.Entry(self.canvas_potravin,
                        width = 5,
                        textvariable = self.stringvar_entry_tuky[riadok[0]],
                        font = "Verdana 12"
                )
            
                self.canvas_potravin_entry_pre_tuky[riadok[0]].insert(0, riadok[4])
                self.canvas_potravin.create_window((600, canvas_y_coor), window = self.canvas_potravin_entry_pre_tuky[riadok[0]], anchor='nw')
            
                # ----------------- entry bielkoviny -------------------------------
                
                self.canvas_potravin.create_text( (680, (canvas_y_coor + 2)), text = "B:", font = "Verdana 12", anchor="nw")
          
                self.stringvar_entry_bielkoviny[riadok[0]] = tk.StringVar()
            
                self.canvas_potravin_entry_pre_bielkoviny[riadok[0]] = ttk.Entry(self.canvas_potravin,
                        width = 5,
                        textvariable = self.stringvar_entry_bielkoviny[riadok[0]],
                        font = "Verdana 12"
                )
            
                self.canvas_potravin_entry_pre_bielkoviny[riadok[0]].insert(0, riadok[5])
                self.canvas_potravin.create_window((700, canvas_y_coor), window = self.canvas_potravin_entry_pre_bielkoviny[riadok[0]], anchor='nw')
            
                # ----------------- combo kategoria_potravin -------------------------------
                
                self.stringvar_combo[riadok[0]] = tk.StringVar()
            
                self.canvas_potravin_combo[riadok[0]] = ttk.Combobox(self.canvas_potravin,
                        values = self.controller.data_pre_combo(),
                        textvariable = self.stringvar_combo[riadok[0]],
                        state = "readonly",
                        font = "Verdana 12"
                )
                
                self.canvas_potravin_combo[riadok[0]].set(self.controller.dict_val_kategoria[riadok[1]])
                self.canvas_potravin.create_window((800, canvas_y_coor), window = self.canvas_potravin_combo[riadok[0]], anchor='nw')
                
                # ----------------- button Zmeň -------------------------------
                
                self.canvas_potravin_button_zmen[riadok[0]] = tk.Button(self.canvas_potravin,
                        text = "Zmeň",
                        command = lambda id_potravina = riadok[0]:self.controller.zmen_hodnoty_potraviny(id_potravina),
                        width = 8,
                )
                
                self.canvas_potravin_button_zmen[riadok[0]]['font'] = font.Font(size = 12)
                self.canvas_potravin.create_window((1050, (canvas_y_coor - 2 )), window = self.canvas_potravin_button_zmen[riadok[0]], anchor='nw')
                
                # ----------------- button Zmaz -------------------------------
                
                self.canvas_potravin_button_zmaz[riadok[0]] = tk.Button(self.canvas_potravin,
                        text = "Zmaž",
                        command = lambda id_potravina = riadok[0]:self.prever_zmazanie_potraviny(id_potravina),
                        width = 8,
                )
                
                self.canvas_potravin_button_zmaz[riadok[0]]['font'] = font.Font(size = 12)
                self.canvas_potravin.create_window((1150, (canvas_y_coor - 2 )), window = self.canvas_potravin_button_zmaz[riadok[0]], anchor='nw')
                
                
                
    # ---------------------------- Destroy objects of canvas potravin ---------------------
    
    def destroy_canvas_potravin_objects(self):
        for objekt in self.canvas_potravin_entry_pre_nazov.values():
            objekt.destroy()
        
        for objekt in self.canvas_potravin_entry_pre_sacharidy.values():
            objekt.destroy()
        
        for objekt in self.canvas_potravin_entry_pre_tuky.values():
            objekt.destroy()
            
        for objekt in self.canvas_potravin_entry_pre_bielkoviny.values():
            objekt.destroy()
            
        for objekt in self.canvas_potravin_combo.values():
            objekt.destroy()
        
        for objekt in self.canvas_potravin_button_zmen.values():
            objekt.destroy()
            
        for objekt in self.canvas_potravin_button_zmaz.values():
            objekt.destroy()
            
        self.canvas_potravin_entry_pre_pridaj_nazov.destroy() 
        self.canvas_potravin_entry_pre_pridaj_sacharidy.destroy()
        self.canvas_potravin_entry_pre_pridaj_tuky.destroy()
        self.canvas_potravin_entry_pre_pridaj_bielkoviny.destroy()
        self.canvas_potravin_combo_pridaj.destroy()
        self.canvas_potravin_button_pridaj.destroy()
        self.canvas_potravin.delete('all')
        
    # ============ Koniec Canvas pre potraviny (zoznam potravin) ===========================================
    
    # ========================= Prever zmazanie potraviny =====================================
    
    def prever_zmazanie_potraviny(self, id_potravina):
        nazov_potraviny = self.controller.model.vrat_nazov_potraviny_z_id(id_potravina)[0][0]
        self.dialog_zmaz_potravinu = Okna.OknoDialogPotvrdenia(self.root)
        self.dialog_zmaz_potravinu.nadpis["text"] = "Naozaj chcete zmazať potravinu " + nazov_potraviny + " ?"
        self.dialog_zmaz_potravinu.button_ano['command'] = lambda id_potravina = id_potravina:self.controller.zmaz_potravinu(id_potravina)
    
    # ========================= Prever zmazanie potraviny =====================================


    # ========================================================================================
    # ==================                                  ====================================
    # ================== Rozdelenie potravin do jedal dna ====================================
    # ==================                                  ====================================
    # ========================================================================================


    # ============================ Zobrazenie hlavicky pre jedla dna =========================

    def zobraz_hlavicku_jedal(self):
        rozdelenie_nazov_diety = tk.Label(self.main_frame_rozdelenie,
                text = self.controller.global_nazov_diety,
                font = "Verdana 13 bold",
                background = "#ffffff"
                ).grid(row = 0, column = 0, columnspan = 10, sticky = 'nswe')
        
        tk.Label(self.main_frame_rozdelenie,
                text = "Poradie jedál dňa",
                font = "Verdana 13 bold",
                background = "#ffffff"
                ).grid(row = 1, column = 1, columnspan = 6, sticky = 'nswe')
                
        tk.Label(self.main_frame_rozdelenie,
                text = "1.",
                font = "Verdana 12",
                background = "#ffffff"
                ).grid(row = 2, column = 1, sticky = 'nswe')
        tk.Label(self.main_frame_rozdelenie,
                text = "2.",
                font = "Verdana 12",
                background = "#ffffff"
                ).grid(row = 2, column = 2, sticky = 'nswe')
        tk.Label(self.main_frame_rozdelenie,
                text = "3.",
                font = "Verdana 12",
                background = "#ffffff"
                ).grid(row = 2, column = 3, sticky = 'nswe')
        tk.Label(self.main_frame_rozdelenie,
                text = "4.",
                font = "Verdana 12",
                background = "#ffffff"
                ).grid(row = 2, column = 4, sticky = 'nswe')
        tk.Label(self.main_frame_rozdelenie,
                text = "5.",
                font = "Verdana 12",
                background = "#ffffff"
                ).grid(row = 2, column = 5, sticky = 'nswe')
        tk.Label(self.main_frame_rozdelenie,
                text = "6.",
                font = "Verdana 12",
                background = "#ffffff"
                ).grid(row = 2, column = 6, sticky = 'nswe')  
    
    # ============================ Koniec Zobrazenie hlavicky pre jedla dna ==================

    # ================== Canvas pre rozdelenie potravin do jedal (priradenie) =================

    def zobraz_canvas_priradenia(self):
        self.canvas_priradenia = tk.Canvas(self.main_frame_rozdelenie)
        
        self.canvas_priradenia.grid(row = 3, column = 0, columnspan = 7, sticky = 'nswe')
        
        # --------------------- scrollbar pre canvas priradenia ---------------------------------
            
        grid_attr = {'row' : 3, 'column' : 7, 'sticky' : 'ns'}
            
        self.add_scrollbar(self.main_frame_rozdelenie, self.canvas_priradenia, **grid_attr)
            
        # ---------------------- end scrollbar pre canvas priradenia ------------------------------
    
    # --------------------- Vsetky entry pre prerozdelenie potravin do jedal ------------------------------ 
    # --------------------- Vyplni nimi canvas priradenia -----------------------------------------
    
    def vypln_canvas_priradenia(self, data, data_prerozdelenia):
        # data:
        # riadok[0] -> id_potravina
        # riadok[1] -> nazov
        # riadok[2] -> mnozstvo v gramoch
        
        # -------------------------
        
        # data_prerozdelenia:
        # riadok [0] -> id_rozdelenie_do_jedal 
        # riadok [1] -> id_dieta 
        # riadok [2] -> id_potravina 
        # riadok [3] -> prve_jedlo 
        # riadok [4] -> druhe_jedlo 
        # riadok [5] -> tretie_jedlo 
        # riadok [6] -> stvrte_jedlo 
        # riadok [7] -> piate_jedlo 
        # riadok [8] -> sieste_jedlo 
        # riadok [9] -> ts 
        
        prerozdelenie_potraviny = {}
        for riadok in data_prerozdelenia:
            prerozdelenie_potraviny[riadok[2]] = {}
            for i in range(1, 7):
                prerozdelenie_potraviny[riadok[2]][i] = riadok[i + 2]
                
        canvas_y_coor = -40
        
        self.rozdelenie_nazov_potraviny_label = {}
        self.rozdelenie_zostatok_mnozstvo_label = {}
        
        self.rozdelenie_entry = {}
        self.rozdelenie_stringvar = {}
        
        self.celkove_mnozstvo_potraviny = {}
        
        decimal.getcontext().prec = 5
        
        for riadok in data:
        
            self.celkove_mnozstvo_potraviny[riadok[0]] = riadok[2]
            if riadok[2] == None or riadok[2] == '':
                self.celkove_mnozstvo_potraviny[riadok[0]] = 0
                
            self.rozdelenie_entry[riadok[0]] = {}
            self.rozdelenie_stringvar[riadok[0]] = {}
            
            canvas_y_coor += 50
            self.canvas_priradenia.configure(scrollregion = (0, 0, 900, canvas_y_coor + 50))
            
            # ------------------- nazov potraviny v diete ---------------------------
            
            self.rozdelenie_nazov_potraviny_label[riadok[0]] = tk.Label(self.canvas_priradenia, text = riadok[1], font = "Verdana 12", wraplength = 280)
            self.canvas_priradenia.create_window((20, canvas_y_coor), window = self.rozdelenie_nazov_potraviny_label[riadok[0]], anchor = 'nw')
    
            # ------------------ mnozstvo zostatok po prerozdeleni -------------------------------------
            zost_mnoz = riadok[2]
            if riadok[2] == None or riadok[2] == '':
                zost_mnoz = '0'
                
            if riadok[0] in prerozdelenie_potraviny.keys():
                zost_mnoz = decimal.Decimal(zost_mnoz) - sum(decimal.Decimal(prerozdelenie_potraviny[riadok[0]][i]) for i in range(1, 7))
            
            self.rozdelenie_zostatok_mnozstvo_label[riadok[0]] = tk.Label(self.canvas_priradenia, text = str(zost_mnoz) + ' g', font = "Verdana 12", wraplength = 300)
            self.canvas_priradenia.create_window((310, canvas_y_coor), window = self.rozdelenie_zostatok_mnozstvo_label[riadok[0]], anchor = 'nw')
            
            # ------------------ entry mnozstvo pre prve jedlo -------------------------------------
            
            self.rozdelenie_stringvar[riadok[0]][1] = tk.StringVar()
            
            self.rozdelenie_entry[riadok[0]][1] = tk.Entry(self.canvas_priradenia,
                                                    textvariable = self.rozdelenie_stringvar[riadok[0]][1],
                                                    width = 4,
                                                    font = "Verdana 12")
            self.canvas_priradenia.create_window((410, canvas_y_coor), window = self.rozdelenie_entry[riadok[0]][1], anchor = 'nw')
           
            if riadok[0] in prerozdelenie_potraviny.keys():
                self.rozdelenie_entry[riadok[0]][1].insert(0, prerozdelenie_potraviny[riadok[0]][1])
            
            self.rozdelenie_stringvar[riadok[0]][1].trace('w',
                lambda var, index, mode, id_potravina = riadok[0], jedlo = 1 : self.controller.prerozdel_potraviny_do_jedal(var, index, mode,id_potravina, jedlo))
            
            # ------------------ entry mnozstvo pre druhe jedlo -------------------------------------
            
            self.rozdelenie_stringvar[riadok[0]][2] = tk.StringVar()
            
            self.rozdelenie_entry[riadok[0]][2] = tk.Entry(self.canvas_priradenia,
                                                    textvariable = self.rozdelenie_stringvar[riadok[0]][2],
                                                    width = 4,
                                                    font = "Verdana 12")
            self.canvas_priradenia.create_window((485, canvas_y_coor), window = self.rozdelenie_entry[riadok[0]][2], anchor = 'nw')
            
            if riadok[0] in prerozdelenie_potraviny.keys():
                self.rozdelenie_entry[riadok[0]][2].insert(0, prerozdelenie_potraviny[riadok[0]][2])
            
            self.rozdelenie_stringvar[riadok[0]][2].trace('w',
                lambda var, index, mode, id_potravina = riadok[0], jedlo = 2 : self.controller.prerozdel_potraviny_do_jedal(var, index, mode, id_potravina, jedlo))
            
            # ------------------ entry mnozstvo pre tretie jedlo -------------------------------------
            
            self.rozdelenie_stringvar[riadok[0]][3] = tk.StringVar()
            
            self.rozdelenie_entry[riadok[0]][3] = tk.Entry(self.canvas_priradenia,
                                                    textvariable = self.rozdelenie_stringvar[riadok[0]][3],
                                                    width = 4,
                                                    font = "Verdana 12")
            self.canvas_priradenia.create_window((560, canvas_y_coor), window = self.rozdelenie_entry[riadok[0]][3], anchor = 'nw')
            
            if riadok[0] in prerozdelenie_potraviny.keys():
                self.rozdelenie_entry[riadok[0]][3].insert(0, prerozdelenie_potraviny[riadok[0]][3])
            
            self.rozdelenie_stringvar[riadok[0]][3].trace('w',
                lambda var, index, mode, id_potravina = riadok[0], jedlo = 3 : self.controller.prerozdel_potraviny_do_jedal(var, index, mode, id_potravina, jedlo))
            
            # ------------------ entry mnozstvo pre stvrte jedlo -------------------------------------
            
            self.rozdelenie_stringvar[riadok[0]][4] = tk.StringVar()
            
            self.rozdelenie_entry[riadok[0]][4] = tk.Entry(self.canvas_priradenia,
                                                    textvariable = self.rozdelenie_stringvar[riadok[0]][4],
                                                    width = 4,
                                                    font = "Verdana 12")
            self.canvas_priradenia.create_window((635, canvas_y_coor), window = self.rozdelenie_entry[riadok[0]][4], anchor = 'nw')
            
            if riadok[0] in prerozdelenie_potraviny.keys():
                self.rozdelenie_entry[riadok[0]][4].insert(0, prerozdelenie_potraviny[riadok[0]][4])
            
            self.rozdelenie_stringvar[riadok[0]][4].trace('w',
                lambda var, index, mode, id_potravina = riadok[0], jedlo = 4 : self.controller.prerozdel_potraviny_do_jedal(var, index, mode, id_potravina, jedlo))
            
            # ------------------ entry mnozstvo pre piate jedlo -------------------------------------
            
            self.rozdelenie_stringvar[riadok[0]][5] = tk.StringVar()
            
            self.rozdelenie_entry[riadok[0]][5] = tk.Entry(self.canvas_priradenia,
                                                    textvariable = self.rozdelenie_stringvar[riadok[0]][5],
                                                    width = 4,
                                                    font = "Verdana 12")
            self.canvas_priradenia.create_window((710, canvas_y_coor), window = self.rozdelenie_entry[riadok[0]][5], anchor = 'nw')
            
            if riadok[0] in prerozdelenie_potraviny.keys():
                self.rozdelenie_entry[riadok[0]][5].insert(0, prerozdelenie_potraviny[riadok[0]][5])
            
            self.rozdelenie_stringvar[riadok[0]][5].trace('w',
                lambda var, index, mode, id_potravina = riadok[0], jedlo = 5 : self.controller.prerozdel_potraviny_do_jedal(var, index, mode, id_potravina, jedlo))
            
            # ------------------ entry mnozstvo pre sieste jedlo -------------------------------------
            
            self.rozdelenie_stringvar[riadok[0]][6] = tk.StringVar()
            
            self.rozdelenie_entry[riadok[0]][6] = tk.Entry(self.canvas_priradenia,
                                                    textvariable = self.rozdelenie_stringvar[riadok[0]][6],
                                                    width = 4,
                                                    font = "Verdana 12")
            self.canvas_priradenia.create_window((785, canvas_y_coor), window = self.rozdelenie_entry[riadok[0]][6], anchor = 'nw')
            
            if riadok[0] in prerozdelenie_potraviny.keys():
                self.rozdelenie_entry[riadok[0]][6].insert(0, prerozdelenie_potraviny[riadok[0]][6])
            
            self.rozdelenie_stringvar[riadok[0]][6].trace('w',
                lambda var, index, mode, id_potravina = riadok[0], jedlo = 6 : self.controller.prerozdel_potraviny_do_jedal(var, index, mode, id_potravina, jedlo))
            
    # ================== Koniec Canvas pre rozdelenie potravin do jedal (priradenie) =================    
   
    # ================ Canvas pre vypis jednotlivych potravin do jedal dna =========================
    
    def zobraz_canvas_zoznam_jedal(self):
        self.canvas_zoznam_jedal = tk.Canvas(self.main_frame_rozdelenie)
        
        self.canvas_zoznam_jedal.grid(row = 1, column = 8, rowspan = 3, sticky = 'nswe')
        
        # --------------------- scrollbar pre canvas zoznam jedal ---------------------------------
            
        grid_attr = {'row' : 1, 'column' : 9, 'rowspan' : 3, 'sticky' : 'ns'}
            
        self.add_scrollbar(self.main_frame_rozdelenie, self.canvas_zoznam_jedal, **grid_attr)
            
        # ---------------------- end scrollbar pre canvas zoznam jedal ------------------------------
    
    def vypln_canvas_zoznam_jedal(self, data):
        
        # riadok [0] -> nazov potraviny 
        # riadok [1] -> prve_jedlo 
        # riadok [2] -> druhe_jedlo 
        # riadok [3] -> tretie_jedlo 
        # riadok [4] -> stvrte_jedlo 
        # riadok [5] -> piate_jedlo 
        # riadok [6] -> sieste_jedlo 
        # riadok [7] -> sacharidy
        # riadok [8] -> tuky 
        # riadok [9] -> bielkoviny 
        
        jedlo_nazov = {}
        jedlo_mnozstvo = {}
        sacharidy = {}
        tuky = {}
        bielkoviny = {}
        
        zaznamov = -1
        for i, riadok in enumerate(data):
            jedlo_nazov[i]= riadok[0]
            sacharidy[i]= riadok[7]
            tuky[i]= riadok[8]
            bielkoviny[i]= riadok[9]
            
            # ----------- jednotlive mnozstva pre prve az sieste jedlo dna --------------
            
            jedlo_mnozstvo[i] = {}
            jedlo_mnozstvo[i][1] = riadok[1]
            jedlo_mnozstvo[i][2] = riadok[2]
            jedlo_mnozstvo[i][3] = riadok[3]
            jedlo_mnozstvo[i][4] = riadok[4]
            jedlo_mnozstvo[i][5] = riadok[5]
            jedlo_mnozstvo[i][6] = riadok[6]
            
            zaznamov = i # celkovy pocet zaznamov, pocet prvkov diety (potravin diety)
        
        self.canvas_zoznam_jedal.delete('all')
        
        # --------------------- Generuj zoznam rozdelenia do jedal dna ----------------------------
        
        canvas_y_coor = -20
        for jedlo in range(1, 7):
            jedlo_dna = ''
            if jedlo == 1 and sum(float(jedlo_mnozstvo[i][1]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Prvé jedlo dňa (raňajky)"
            elif jedlo == 2 and sum(float(jedlo_mnozstvo[i][2]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Druhé jedlo dňa (desiata)"
            elif jedlo == 3 and sum(float(jedlo_mnozstvo[i][3]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Tretie jedlo dňa (obed)"
            elif jedlo == 4 and sum(float(jedlo_mnozstvo[i][4]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Štvrté jedlo dňa (olovrant)"
            elif jedlo == 5 and sum(float(jedlo_mnozstvo[i][5]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Piate jedlo dňa (večera)"
            elif jedlo == 6 and sum(float(jedlo_mnozstvo[i][6]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Šieste jedlo dňa (druhá večera)" 
            
            if jedlo_dna != '':
                canvas_y_coor += 30    
                self.canvas_zoznam_jedal.create_text( (20, canvas_y_coor),
                        text = jedlo_dna,
                        font = "Verdana 13 bold",
                        anchor="nw")
                canvas_y_coor += -5
            else:  
                canvas_y_coor += -30
            
            celk_mn_sach = {}
            celk_mn_tuk = {}
            celk_mn_bielk = {}
            celk_energia = {}
            
            celk_mn_sach[jedlo] = 0
            celk_mn_tuk[jedlo] = 0
            celk_mn_bielk[jedlo] = 0
            celk_energia[jedlo] = 0
            
            for i in range(0, zaznamov + 1):
                if jedlo_mnozstvo[i][jedlo] != '0':
                    canvas_y_coor += 30
                    self.canvas_zoznam_jedal.create_text( (20, canvas_y_coor),
                        text = jedlo_nazov[i],
                        font = "Verdana 12",
                        anchor="nw")
                    self.canvas_zoznam_jedal.create_text( (350, canvas_y_coor),
                        text = jedlo_mnozstvo[i][jedlo] + ' g',
                        font = "Verdana 12",
                        anchor="nw")
                    
                    mn_sach = round (float(sacharidy[i]) / 100 * float(jedlo_mnozstvo[i][jedlo]), 1)
                    mn_tuk = round (float(tuky[i]) / 100 * float(jedlo_mnozstvo[i][jedlo]), 1)
                    mn_bielk = round(float(bielkoviny[i]) / 100 * float(jedlo_mnozstvo[i][jedlo]), 1)
                    energia =  round(float(mn_sach) * 16.736 + float(mn_tuk) * 37.656 + float(mn_bielk) * 16.736)
                    
                    canvas_y_coor += 30
                    
                    self.canvas_zoznam_jedal.create_text( (20, canvas_y_coor),
                        text = "S: " + str(mn_sach) + ' g',
                        font = "Verdana 12",
                        anchor="nw")
                        
                    self.canvas_zoznam_jedal.create_text( (120, canvas_y_coor),
                        text = "T: " + str(mn_tuk) + ' g',
                        font = "Verdana 12",
                        anchor="nw")
                    
                    self.canvas_zoznam_jedal.create_text( (220, canvas_y_coor),
                        text = "B: " + str(mn_bielk) + ' g',
                        font = "Verdana 12",
                        anchor="nw")
                    
                    self.canvas_zoznam_jedal.create_text( (320, canvas_y_coor),
                        text = "E: " + str(energia) + ' kJ',
                        font = "Verdana 12",
                        anchor="nw")
                    
                    canvas_y_coor += 15
                    
                    celk_mn_sach[jedlo] += mn_sach
                    celk_mn_tuk[jedlo] += mn_tuk
                    celk_mn_bielk[jedlo] += mn_bielk
                    celk_energia[jedlo] += energia
                    
            canvas_y_coor += 30 
            
            celk_mn_sach[jedlo] = round(celk_mn_sach[jedlo], 1)
            celk_mn_tuk[jedlo] = round(celk_mn_tuk[jedlo], 1)
            celk_mn_bielk[jedlo] = round(celk_mn_bielk[jedlo], 1)
            celk_energia[jedlo] = round(celk_energia[jedlo], 1)
            
            if celk_energia[jedlo] != 0:
                self.canvas_zoznam_jedal.create_text( (20, canvas_y_coor),
                        text = "Celkové hodnoty:",
                        font = "Verdana 12",
                        anchor="nw")  
                        
                self.canvas_zoznam_jedal.create_text( (200, canvas_y_coor),
                        text = "S: " + str(celk_mn_sach[jedlo]) + ' g',
                        font = "Verdana 12",
                        anchor="nw")  
                        
                self.canvas_zoznam_jedal.create_text( (300, canvas_y_coor),
                        text = "T: " + str(celk_mn_tuk[jedlo]) + ' g',
                        font = "Verdana 12",
                        anchor="nw")  
                        
                self.canvas_zoznam_jedal.create_text( (400, canvas_y_coor),
                        text = "B: " + str(celk_mn_bielk[jedlo]) + ' g',
                        font = "Verdana 12",
                        anchor="nw")  
                        
                self.canvas_zoznam_jedal.create_text( (500, canvas_y_coor),
                        text = "E: " + str(celk_energia[jedlo]) + ' kJ',
                        font = "Verdana 12",
                        anchor="nw")  
                
                canvas_y_coor += 15 
        
        energia_v_diete, mn_sach_v_diete, mn_tuk_v_diete, mn_bielk_v_diete = self.controller.vypocitaj_celkove_hodnoty_diety()
        
        canvas_y_coor += 30
        if energia_v_diete != 0:
                self.canvas_zoznam_jedal.create_text( (20, canvas_y_coor),
                        text = "Celkové hodnoty diety:",
                        font = "Verdana 12 bold",
                        anchor="nw")  
                        
                self.canvas_zoznam_jedal.create_text( (250, canvas_y_coor),
                        text = "S: " + str(mn_sach_v_diete) + ' g',
                        font = "Verdana 12",
                        anchor="nw")  
                        
                self.canvas_zoznam_jedal.create_text( (350, canvas_y_coor),
                        text = "T: " + str(mn_tuk_v_diete) + ' g',
                        font = "Verdana 12",
                        anchor="nw")  
                        
                self.canvas_zoznam_jedal.create_text( (450, canvas_y_coor),
                        text = "B: " + str(mn_bielk_v_diete) + ' g',
                        font = "Verdana 12",
                        anchor="nw")  
                        
                self.canvas_zoznam_jedal.create_text( (550, canvas_y_coor),
                        text = "E: " + str(energia_v_diete) + ' kJ',
                        font = "Verdana 12",
                        anchor="nw")  
        
        self.canvas_zoznam_jedal.configure(scrollregion = (0, 0, 900, canvas_y_coor + 50))
    
    # ================ Koniec Canvas pre vypis jednotlivych potravin do jedal dna =========================    

    # ========================================================================================  
    # =======================                       ==========================================   
    # ======================= Vytvorenie pdf suboru ==========================================   
    # =======================                       ==========================================   
    # ======================================================================================== 
   
    # ============ otvorenie dialogu pre ulozenie suboru a vratenie cesty a mena suboru ======
   
    def daj_subor_pdf(self):
        cesta_a_subor_pdf = fd.asksaveasfilename(parent = self.root,
                            title = 'Zvoľte subor',
                            initialdir = os.getcwd(),
                            defaultextension = ".pdf",
                            filetypes = [('pdf súbory', '*.pdf')]
                            )
        return cesta_a_subor_pdf
    
    # ============== Koniec dialogu pre ulozenie suboru a vratenie cesty a mena suboru ==========
    
    # ============== Vytvor objekt pdf ==========================================================
    
    def vytvor_objekt_pdf(self):
        self.pdf = FPDF(unit = 'mm', format = 'A4')
        self.pdf.add_font('DejaVu-Bold', '', 'fonty/DejaVuSansCondensed-Bold.ttf', uni=True)
        self.pdf.add_font('DejaVu', '', 'fonty/DejaVuSansCondensed.ttf', uni=True)
        
    # ============== Vytvor objekt pdf ==========================================================
    
    # ============== Vytvorenie kratkeho vypisu diety do pdf suboru =============================
    
    def vytvor_kratky_pdf(self):
        self.pdf.add_page()
        
        self.pdf.set_font('DejaVu-Bold', '', 14)
        
        self.pdf.set_x(55)
        self.pdf.write(10, 'Názov diety: ' + self.controller.global_nazov_diety)
        
        # --------------------- Celkove hodnoty diety ------------------------
        
        celk_energia_kj, celk_sacharidy, celk_tuky, celk_bielkoviny = self.controller.vypocitaj_celkove_hodnoty_diety()
        odp_celk_sacharidy, odp_celk_tuky, odp_celk_bielkoviny = self.controller.vypocitaj_odporucane_hodnoty_diety()
        
        self.pdf.set_font('DejaVu', '', 12)
        
        x_coor1 = 65
        x_coor2 = 87
        
        self.pdf.set_xy(20, 20)
        self.pdf.write(10, 'Množstvo tuku:')
        self.pdf.set_xy(x_coor1, 20)
        self.pdf.write(10, str(celk_tuky) + ' g')
        self.pdf.set_xy(x_coor2, 20)
        self.pdf.write(10, '(' + str(odp_celk_tuky) + ' g)')
        
        self.pdf.set_xy(20, 30)
        self.pdf.write(10, 'Množstvo sacharidov:')
        self.pdf.set_xy(x_coor1, 30)
        self.pdf.write(10, str(celk_sacharidy) + ' g')
        self.pdf.set_xy(x_coor2, 30)
        self.pdf.write(10, '(' + str(odp_celk_sacharidy) + ' g)')
        
        self.pdf.set_xy(20, 40)
        self.pdf.write(10, 'Množstvo bielkovín:')
        self.pdf.set_xy(x_coor1, 40)
        self.pdf.write(10, str(celk_bielkoviny) + ' g')
        self.pdf.set_xy(x_coor2, 40)
        self.pdf.write(10, '(' + str(odp_celk_bielkoviny) + ' g)')
        
        self.pdf.set_xy(20, 50)
        self.pdf.write(10, 'Energia:')
        self.pdf.set_xy(x_coor1, 50)
        self.pdf.write(10, str(celk_energia_kj) + ' kJ')
        
        # ------------------------- Predpokladana strata tuku ----------------------------
        
        denna_spotreba_energie = self.hodnota_den_spotr_energ.get()
        den, tyzden, mesiac, rok = self.controller.vypocet_straty_tuku(denna_spotreba_energie, celk_energia_kj)
        
        x_coor1 = 110
        x_coor2 = 175
        
        self.pdf.set_xy(x_coor1, 20)
        self.pdf.write(10, 'Denná spotreba energie:')
        self.pdf.set_xy(x_coor2, 20)
        self.pdf.write(10, str(denna_spotreba_energie) + ' kJ')
        
        self.pdf.set_xy(x_coor1, 30)
        self.pdf.write(10, 'Strata tuku za deň:')
        self.pdf.set_xy(x_coor2, 30)
        self.pdf.write(10, str(den) + ' g')
        
        self.pdf.set_xy(x_coor1, 40)
        self.pdf.write(10, 'Strata tuku za týždeň:')
        self.pdf.set_xy(x_coor2, 40)
        self.pdf.write(10, str(tyzden) + ' g')
        
        self.pdf.set_xy(x_coor1, 50)
        self.pdf.write(10, 'Strata tuku za mesiac (30 dní):')
        self.pdf.set_xy(x_coor2, 50)
        self.pdf.write(10, str(mesiac) + ' g')
        
        self.pdf.set_xy(x_coor1, 60)
        self.pdf.write(10, 'Strata tuku za rok:')
        self.pdf.set_xy(x_coor2, 60)
        self.pdf.write(10, str(rok) + ' g')
        
        # ------------------------ Jednotlive prvky diety ----------------------------
            # ------ toto su dictionaries s klucami id_potravina
        energia_kj, sacharidy, tuky, bielkoviny, mnozstvo  = self.controller.vypocitaj_hodnoty_pre_prvky_diety()
        
        self.pdf.set_font('DejaVu-Bold', '', 12)
        
        self.pdf.set_xy(20, 70)
        self.pdf.write(10, 'Jednotlivé potraviny diety a ich hodnoty:')
        
        self.pdf.set_font('DejaVu', '', 12)
        
        x_coor1 = 20
        x_coor2 = 120
        y_coor = 70
        for id_potravina in energia_kj:
            nazov_potraviny = self.controller.model.vrat_nazov_potraviny_z_id(id_potravina)[0][0]
            energia_kj[id_potravina] = round(energia_kj[id_potravina])
            sacharidy[id_potravina] = round(sacharidy[id_potravina], 1)
            tuky[id_potravina] = round(tuky[id_potravina], 1)
            bielkoviny[id_potravina] = round(bielkoviny[id_potravina], 1)
        
            y_coor += 10
            self.pdf.set_xy(x_coor1, y_coor)
            self.pdf.write(10, nazov_potraviny)
            self.pdf.set_xy(x_coor2, y_coor)
            self.pdf.write(10, mnozstvo[id_potravina] + ' g')
            
            y_coor += 6
            self.pdf.set_xy(20, y_coor)
            self.pdf.write(10, 'S: ' + str(sacharidy[id_potravina]) + ' g')
            
            self.pdf.set_xy(50, y_coor)
            self.pdf.write(10, 'T: ' + str(tuky[id_potravina]) + ' g')
            
            self.pdf.set_xy(80, y_coor)
            self.pdf.write(10, 'B: ' + str(bielkoviny[id_potravina]) + ' g')
            
            self.pdf.set_xy(110, y_coor)
            self.pdf.write(10, 'E: ' + str(energia_kj[id_potravina]) + ' kJ')
            
    # ============== Koniec Vytvorenie kratkeho vypisu diety do pdf suboru =============================
    
    # ============== Vytvorenie celkoveho vypisu diety do pdf suboru =============================
    
    def vytvor_celkovy_pdf(self):
        self.vytvor_kratky_pdf()
        
        self.pdf.add_page()
        
        data = self.controller.model.vrat_rozdelenie(self.controller.global_id_diety)
        
        # riadok [0] -> nazov potraviny 
        # riadok [1] -> prve_jedlo 
        # riadok [2] -> druhe_jedlo 
        # riadok [3] -> tretie_jedlo 
        # riadok [4] -> stvrte_jedlo 
        # riadok [5] -> piate_jedlo 
        # riadok [6] -> sieste_jedlo 
        # riadok [7] -> sacharidy
        # riadok [8] -> tuky 
        # riadok [9] -> bielkoviny 
        
        jedlo_nazov = {}
        jedlo_mnozstvo = {}
        sacharidy = {}
        tuky = {}
        bielkoviny = {}
        
        zaznamov = -1
        for i, riadok in enumerate(data):
            jedlo_nazov[i]= riadok[0]
            sacharidy[i]= riadok[7]
            tuky[i]= riadok[8]
            bielkoviny[i]= riadok[9]
            
            # ----------- jednotlive mnozstva pre prve az sieste jedlo dna --------------
            
            jedlo_mnozstvo[i] = {}
            jedlo_mnozstvo[i][1] = riadok[1]
            jedlo_mnozstvo[i][2] = riadok[2]
            jedlo_mnozstvo[i][3] = riadok[3]
            jedlo_mnozstvo[i][4] = riadok[4]
            jedlo_mnozstvo[i][5] = riadok[5]
            jedlo_mnozstvo[i][6] = riadok[6]
            
            zaznamov = i # celkovy pocet zaznamov, pocet prvkov diety (potravin diety)
        
        dlzka_strany = 250
        
        y_coor =  10
        for jedlo in range(1, 7):
            jedlo_dna = ''
            if jedlo == 1 and sum(float(jedlo_mnozstvo[i][1]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Prvé jedlo dňa (raňajky)"
            elif jedlo == 2 and sum(float(jedlo_mnozstvo[i][2]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Druhé jedlo dňa (desiata)"
            elif jedlo == 3 and sum(float(jedlo_mnozstvo[i][3]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Tretie jedlo dňa (obed)"
            elif jedlo == 4 and sum(float(jedlo_mnozstvo[i][4]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Štvrté jedlo dňa (olovrant)"
            elif jedlo == 5 and sum(float(jedlo_mnozstvo[i][5]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Piate jedlo dňa (večera)"
            elif jedlo == 6 and sum(float(jedlo_mnozstvo[i][6]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Šieste jedlo dňa (druhá večera)" 
            
            if jedlo_dna != '':
                if y_coor > dlzka_strany:
                    self.pdf.add_page()
                    y_coor = 10
                    
                y_coor += 10 
                self.pdf.set_font('DejaVu-Bold', '', 12)
                
                self.pdf.set_xy(20, y_coor)
                self.pdf.write(10, jedlo_dna)
                
                y_coor += -2
            else:  
                y_coor += -10
            
            celk_mn_sach = {}
            celk_mn_tuk = {}
            celk_mn_bielk = {}
            celk_energia = {}
            
            celk_mn_sach[jedlo] = 0
            celk_mn_tuk[jedlo] = 0
            celk_mn_bielk[jedlo] = 0
            celk_energia[jedlo] = 0
            
            self.pdf.set_font('DejaVu', '', 12)
            
            for i in range(0, zaznamov + 1):
                if jedlo_mnozstvo[i][jedlo] != '0':
                    if y_coor > dlzka_strany:
                        self.pdf.add_page()
                        y_coor = 10
                    y_coor += 10
                    
                    self.pdf.set_xy(20, y_coor)
                    self.pdf.write(10, jedlo_nazov[i])
                    self.pdf.set_xy(100, y_coor)
                    self.pdf.write(10, jedlo_mnozstvo[i][jedlo] + ' g')
                    
                    mn_sach = round (float(sacharidy[i]) / 100 * float(jedlo_mnozstvo[i][jedlo]), 1)
                    mn_tuk = round (float(tuky[i]) / 100 * float(jedlo_mnozstvo[i][jedlo]), 1)
                    mn_bielk = round(float(bielkoviny[i]) / 100 * float(jedlo_mnozstvo[i][jedlo]), 1)
                    energia =  round(float(mn_sach) * 16.736 + float(mn_tuk) * 37.656 + float(mn_bielk) * 16.736)
                    
                    if y_coor > dlzka_strany:
                        self.pdf.add_page()
                        y_coor = 10
                    y_coor += 10
                    
                    self.pdf.set_xy(20, y_coor)
                    self.pdf.write(10, "S: " + str(mn_sach) + ' g')
                    
                    self.pdf.set_xy(50, y_coor)
                    self.pdf.write(10, "T: " + str(mn_tuk) + ' g')
                    
                    self.pdf.set_xy(80, y_coor)
                    self.pdf.write(10, "B: " + str(mn_bielk) + ' g')
                    
                    self.pdf.set_xy(110, y_coor)
                    self.pdf.write(10, "E: " + str(energia) + ' kJ')
                    
                    if y_coor > dlzka_strany:
                        self.pdf.add_page()
                        y_coor = 10
                    y_coor += 5
                    
                    celk_mn_sach[jedlo] += mn_sach
                    celk_mn_tuk[jedlo] += mn_tuk
                    celk_mn_bielk[jedlo] += mn_bielk
                    celk_energia[jedlo] += energia
                    
            if y_coor > dlzka_strany:
                self.pdf.add_page() 
                y_coor = 10
            y_coor += 10 
            
            celk_mn_sach[jedlo] = round(celk_mn_sach[jedlo], 1)
            celk_mn_tuk[jedlo] = round(celk_mn_tuk[jedlo], 1)
            celk_mn_bielk[jedlo] = round(celk_mn_bielk[jedlo], 1)
            celk_energia[jedlo] = round(celk_energia[jedlo], 1)
            
            if celk_energia[jedlo] != 0:
                self.pdf.set_xy(20, y_coor)
                self.pdf.write(10, "Celkové hodnoty:")
                
                self.pdf.set_xy(60, y_coor)
                self.pdf.write(10, "S: " + str(celk_mn_sach[jedlo]) + ' g')
                
                self.pdf.set_xy(90, y_coor)
                self.pdf.write(10, "T: " + str(celk_mn_tuk[jedlo]) + ' g')
                
                self.pdf.set_xy(110, y_coor)
                self.pdf.write(10, "B: " + str(celk_mn_bielk[jedlo]) + ' g')
                
                self.pdf.set_xy(140, y_coor)
                self.pdf.write(10, "E: " + str(celk_energia[jedlo]) + ' kJ')
                
                if y_coor > dlzka_strany:
                    self.pdf.add_page()
                    y_coor = 10
                y_coor += 5 
    # ============== Koniec Vytvorenie celkoveho vypisu diety do pdf suboru =============================
    
    # ================ Ulozenie a otvorenie suboru kratkeho alebo celkoveho pdf =================
    
    def uloz_a_otvor_subor_pdf(self, cesta_a_subor_pdf): 
        try:
            self.pdf.output(cesta_a_subor_pdf, 'F')
        except:
            subor = os.path.split(cesta_a_subor_pdf)[1]
            self.show_error("Nedá sa uložiť súbor >> " + subor + " << . Pravdepodobne je otvorený")
        else:
            os.popen(cesta_a_subor_pdf)
        
    # ================ Koniec Ulozenie a otvorenie suboru kratkeho alebo celkoveho pdf =================
    
    
    # ========================================================================================  
    # =======================                       ==========================================   
    # ======================= Vytvorenie txt suboru ==========================================   
    # =======================                       ==========================================   
    # ======================================================================================== 
    
    # ============ Otvorenie dialogu pre ulozenie suboru a vratenie cesty a mena suboru ======
   
    def daj_subor_txt(self):
        cesta_a_subor_txt = fd.asksaveasfilename(parent = self.root,
                            title = 'Zvoľte subor',
                            initialdir = os.getcwd(),
                            defaultextension = ".txt",
                            filetypes = [('textové súbory', '*.txt')]
                            )
        return cesta_a_subor_txt
    
    # ============ Koniec Otvorenie dialogu pre ulozenie suboru a vratenie cesty a mena suboru ======
   
    # =================== Otvorenie textoveho suboru pre zapis ==============================
    
    def otvor_txt_pre_zapis(self, cesta_a_subor_txt):
        self.txt = open(cesta_a_subor_txt, 'w')
    
    # =================== Koniec Otvorenie textoveho suboru pre zapis ==============================
    
    # ================= Vytvorenie kratkeho vypisu do textoveho suboru =========================
    
    def vytvor_kratky_txt(self):
        self.txt.write('Názov diety: ' + self.controller.global_nazov_diety + '\n')
        self.txt.write(50*'_' + '\n\n')
        
        # ------------------ Sumar diety a straty tuku ------------------------------
        
        celk_energia_kj, celk_sacharidy, celk_tuky, celk_bielkoviny = self.controller.vypocitaj_celkove_hodnoty_diety()
        odp_celk_sacharidy, odp_celk_tuky, odp_celk_bielkoviny = self.controller.vypocitaj_odporucane_hodnoty_diety()
        
        denna_spotreba_energie = self.hodnota_den_spotr_energ.get()
        den, tyzden, mesiac, rok = self.controller.vypocet_straty_tuku(denna_spotreba_energie, celk_energia_kj)
        
        self.txt.write('Množstvo tuku: \t\t\t' + str(celk_tuky) + ' g\t (' + str(odp_celk_tuky) + ' g)')
        self.txt.write('\t\t\t\tDenná spotreba energie: \t\t' + str(denna_spotreba_energie) + ' kJ \n')
        self.txt.write('Množstvo sacharidov: \t\t' + str(celk_sacharidy) + ' g\t (' + str(odp_celk_sacharidy) + ' g)')
        self.txt.write('\t\t\t\tStrata tuku za deň: \t\t\t' + str(den) + ' g\n')
        self.txt.write('Množstvo bielkovín: \t\t' + str(celk_bielkoviny) + ' g\t (' + str(odp_celk_bielkoviny) + ' g)')
        self.txt.write('\t\t\t\tStrata tuku za týždeň: \t\t\t' + str(tyzden) + ' g\n')
        self.txt.write('Energia: \t\t\t\t' + str(celk_energia_kj) + ' kJ')
        self.txt.write('\t\t\t\t\t\tStrata tuku za mesiac (30 dní): \t' + str(mesiac) + ' g\n')
        self.txt.write('\t\t\t\t\t\t\t\t\t\t\t\tStrata tuku za rok: \t\t\t' + str(rok) + ' g \n')
        self.txt.write(50*'_' + '\n\n')
        
        # ------------------------ Jednotlive prvky diety ----------------------------
            # ------ toto su dictionaries s klucami id_potravina
        energia_kj, sacharidy, tuky, bielkoviny, mnozstvo  = self.controller.vypocitaj_hodnoty_pre_prvky_diety()
        
        self.txt.write('Jednotlivé potraviny diety a ich hodnoty:\n')
        self.txt.write(50*'_' + '\n\n')
        
        for id_potravina in energia_kj:
            nazov_potraviny = self.controller.model.vrat_nazov_potraviny_z_id(id_potravina)[0][0]
            energia_kj[id_potravina] = round(energia_kj[id_potravina])
            sacharidy[id_potravina] = round(sacharidy[id_potravina], 1)
            tuky[id_potravina] = round(tuky[id_potravina], 1)
            bielkoviny[id_potravina] = round(bielkoviny[id_potravina], 1)
           
            self.txt.write(nazov_potraviny + 20*'.' + mnozstvo[id_potravina] + ' g\n')
            
            self.txt.write('S: ' + str(sacharidy[id_potravina]) + ' g')
            self.txt.write(2*'\t')
            self.txt.write('T: ' + str(tuky[id_potravina]) + ' g')
            self.txt.write(2*'\t')
            self.txt.write('B: ' + str(bielkoviny[id_potravina]) + ' g')
            self.txt.write(2*'\t')
            self.txt.write('E: ' + str(energia_kj[id_potravina]) + ' kJ\n\n')
            
    # ================= Koniec Vytvorenie kratkeho vypisu do textoveho suboru =========================
    
    # ================= Vytvorenie celkoveho vypisu do textoveho suboru =========================
    
    def vytvor_celkovy_txt(self):
        self.vytvor_kratky_txt()
        
        self.txt.write(100 * '-' + '\n')
        self.txt.write(100 * '-' + '\n\n\n')
        
        data = self.controller.model.vrat_rozdelenie(self.controller.global_id_diety)
        
        # riadok [0] -> nazov potraviny 
        # riadok [1] -> prve_jedlo 
        # riadok [2] -> druhe_jedlo 
        # riadok [3] -> tretie_jedlo 
        # riadok [4] -> stvrte_jedlo 
        # riadok [5] -> piate_jedlo 
        # riadok [6] -> sieste_jedlo 
        # riadok [7] -> sacharidy
        # riadok [8] -> tuky 
        # riadok [9] -> bielkoviny 
        
        jedlo_nazov = {}
        jedlo_mnozstvo = {}
        sacharidy = {}
        tuky = {}
        bielkoviny = {}
        
        zaznamov = -1
        for i, riadok in enumerate(data):
            jedlo_nazov[i]= riadok[0]
            sacharidy[i]= riadok[7]
            tuky[i]= riadok[8]
            bielkoviny[i]= riadok[9]
            
            # ----------- jednotlive mnozstva pre prve az sieste jedlo dna --------------
            
            jedlo_mnozstvo[i] = {}
            jedlo_mnozstvo[i][1] = riadok[1]
            jedlo_mnozstvo[i][2] = riadok[2]
            jedlo_mnozstvo[i][3] = riadok[3]
            jedlo_mnozstvo[i][4] = riadok[4]
            jedlo_mnozstvo[i][5] = riadok[5]
            jedlo_mnozstvo[i][6] = riadok[6]
            
            zaznamov = i # celkovy pocet zaznamov, pocet prvkov diety (potravin diety)
        
        dlzka_strany = 250
        
        y_coor =  10
        for jedlo in range(1, 7):
            jedlo_dna = ''
            if jedlo == 1 and sum(float(jedlo_mnozstvo[i][1]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Prvé jedlo dňa (raňajky)"
            elif jedlo == 2 and sum(float(jedlo_mnozstvo[i][2]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Druhé jedlo dňa (desiata)"
            elif jedlo == 3 and sum(float(jedlo_mnozstvo[i][3]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Tretie jedlo dňa (obed)"
            elif jedlo == 4 and sum(float(jedlo_mnozstvo[i][4]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Štvrté jedlo dňa (olovrant)"
            elif jedlo == 5 and sum(float(jedlo_mnozstvo[i][5]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Piate jedlo dňa (večera)"
            elif jedlo == 6 and sum(float(jedlo_mnozstvo[i][6]) for i in range(0, zaznamov + 1)) > 0:
                jedlo_dna = "Šieste jedlo dňa (druhá večera)" 
            
            if jedlo_dna != '':
                self.txt.write(jedlo_dna + '\n')
                self.txt.write(50 * '-' + '\n\n')
            
            celk_mn_sach = {}
            celk_mn_tuk = {}
            celk_mn_bielk = {}
            celk_energia = {}
            
            celk_mn_sach[jedlo] = 0
            celk_mn_tuk[jedlo] = 0
            celk_mn_bielk[jedlo] = 0
            celk_energia[jedlo] = 0
            
            for i in range(0, zaznamov + 1):
                if jedlo_mnozstvo[i][jedlo] != '0':
                    
                    self.txt.write(jedlo_nazov[i] + 20*'.')
                    self.txt.write(jedlo_mnozstvo[i][jedlo] + ' g \n')
                    
                    mn_sach = round (float(sacharidy[i]) / 100 * float(jedlo_mnozstvo[i][jedlo]), 1)
                    mn_tuk = round (float(tuky[i]) / 100 * float(jedlo_mnozstvo[i][jedlo]), 1)
                    mn_bielk = round(float(bielkoviny[i]) / 100 * float(jedlo_mnozstvo[i][jedlo]), 1)
                    energia =  round(float(mn_sach) * 16.736 + float(mn_tuk) * 37.656 + float(mn_bielk) * 16.736)
                    
                    self.txt.write("S: " + str(mn_sach) + ' g' + 2*'\t')
                    
                    self.txt.write("T: " + str(mn_tuk) + ' g' + 2*'\t')
                    
                    self.txt.write("B: " + str(mn_bielk) + ' g' + 2*'\t')
                    
                    self.txt.write("E: " + str(energia) + ' kJ \n\n')
                    
                    celk_mn_sach[jedlo] += mn_sach
                    celk_mn_tuk[jedlo] += mn_tuk
                    celk_mn_bielk[jedlo] += mn_bielk
                    celk_energia[jedlo] += energia
            
            celk_mn_sach[jedlo] = round(celk_mn_sach[jedlo], 1)
            celk_mn_tuk[jedlo] = round(celk_mn_tuk[jedlo], 1)
            celk_mn_bielk[jedlo] = round(celk_mn_bielk[jedlo], 1)
            celk_energia[jedlo] = round(celk_energia[jedlo], 1)
            
            if celk_energia[jedlo] != 0:
                
                self.txt.write("Celkové hodnoty:" + 3*'\t')
                
                self.txt.write("S: " + str(celk_mn_sach[jedlo]) + ' g' + 2*'\t')
                
                self.txt.write("T: " + str(celk_mn_tuk[jedlo]) + ' g' + 2*'\t')
                
                self.txt.write("B: " + str(celk_mn_bielk[jedlo]) + ' g' + 2*'\t')
                
                self.txt.write("E: " + str(celk_energia[jedlo]) + ' kJ\n\n\n')
               
    # ================= Koniec Vytvorenie celkoveho vypisu do textoveho suboru =========================
    
    
    # ================== Zatvorenie textoveho suboru ==============================================
    
    def zatvor_txt(self):
        self.txt.close()
    
    # ================== Koniec Zatvorenie textoveho suboru ==============================================
    
    # ================== Otvor textovy subor ====================================================
    
    def otvor_subor_txt(self, cesta_a_subor_txt):
        os.popen(cesta_a_subor_txt)
    
    # ================== Koniec Otvor textovy subor ====================================================
   
    # ========================================================================================  
    # =======================                 ================================================   
    # ======================= Spolocne metody ================================================   
    # =======================                 ================================================   
    # ======================================================================================== 
   
    # =================== Pridaj scrollbar ===================================
    
    def add_scrollbar(self ,parent, container, **grid_attr):
        scrollbar = ttk.Scrollbar(parent, orient=tk.VERTICAL, command = container.yview)
        container.configure(yscrollcommand = scrollbar.set)
        scrollbar.grid(**grid_attr)
       
    @staticmethod
    def show_error(msg):
        showerror(
            title = 'Chyba',
            message = msg
        )