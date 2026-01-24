import mysql.connector


class Model():
    
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
    
    def mysql_connect(self):
        self.mydb = mysql.connector.connect(
            host = self.host,
            user = self.user,
            password = self.password,
            database = self.database
        )
        self.mycursor = self.mydb.cursor()
    
    def zoznam_kategorie_jedla(self):
        return self.dotaz("SELECT * FROM kategoria_jedla ORDER BY nazov_kategorie")
       
    def zoznam_vsetkych_potravin(self):
        return self.dotaz("SELECT * FROM potraviny ORDER BY nazov")
        
    def zoznam_potravin_podla_kategorie (self, id):
        return self.dotaz("SELECT * FROM potraviny WHERE id_kategoria_jedla = " + str(id) + " ORDER BY nazov")
    
    def zoznam_potravin_podla_retazca(self, retazec):
        return self.dotaz_premenna("SELECT * FROM potraviny WHERE nazov LIKE %s", ('%' + retazec + '%', ))
    
    def vrat_nazvy_diet(self):
        return self.dotaz('SELECT nazov_diety FROM dieta')
    
    def pridaj_dietu (self, nazov_diety):
        self.dotaz_premenna("INSERT INTO dieta (nazov_diety) VALUES (%s)", (nazov_diety, ))
    
    def vrat_id_diety(self, nazov_diety):
        return self.dotaz_premenna("SELECT id_dieta FROM dieta WHERE nazov_diety = %s", (nazov_diety, ))
   
    def vrat_nazov_diety(self, id_diety):
        return self.dotaz_premenna("SELECT nazov_diety FROM dieta WHERE id_dieta = %s", (id_diety, ))
    
    def pridaj_potravinu_do_diety(self, id_dieta, id_potravina):
        self.dotaz("INSERT INTO potraviny_diety (id_dieta, id_potravina) VALUES (" + str(id_dieta) + ", " + str(id_potravina) + ")")
    
    def vrat_potravinu(self, id_dieta, id_potravina):
        return self.dotaz(
            "SELECT potraviny.id_potravina as id_potravina, nazov, sacharidy, tuky, bielkoviny, mnozstvo \
            FROM potraviny_diety \
            LEFT JOIN dieta ON potraviny_diety.id_dieta = dieta.id_dieta \
            LEFT JOIN potraviny ON potraviny.id_potravina = potraviny_diety.id_potravina \
            WHERE dieta.id_dieta = " + str(id_dieta) + " AND potraviny.id_potravina = " + str(id_potravina)
        )
   
    def vrat_potraviny_diety (self, id_dieta):
        return self.dotaz(
            "SELECT potraviny.id_potravina as id_potravina, nazov, sacharidy, tuky, bielkoviny, mnozstvo \
            FROM potraviny_diety \
            LEFT JOIN dieta ON potraviny_diety.id_dieta = dieta.id_dieta \
            LEFT JOIN potraviny ON potraviny.id_potravina = potraviny_diety.id_potravina \
            WHERE dieta.id_dieta = " + str(id_dieta)
        )
    
    def uloz_mnozstvo(self, id_dieta, id_potravina, mnozstvo):
        self.dotaz_premenna("UPDATE potraviny_diety \
                    SET mnozstvo = %s \
                    WHERE id_dieta = " + str(id_dieta) + " AND id_potravina = " + str(id_potravina),
                    (mnozstvo, )
        )
    
    def vrat_diety_a_ich_sumar(self):
        return self.dotaz("SELECT dieta.id_dieta AS id_dieta, nazov_diety,\
                            ROUND(SUM(tuky /100 * mnozstvo), 1) AS celk_tuky,\
                            ROUND(SUM(sacharidy / 100 * mnozstvo), 1) AS celk_sacharidy,\
                            ROUND(SUM(bielkoviny / 100 * mnozstvo), 1) AS celk_bielkoviny, \
                            ROUND((SUM(tuky /100 * mnozstvo) * 37.656 + SUM(sacharidy / 100 * mnozstvo) * 16.736 + SUM(bielkoviny / 100 * mnozstvo) * 16.736), 0) AS celk_energia, \
                            dieta.ts AS ts \
                            FROM potraviny_diety \
                            RIGHT JOIN dieta ON potraviny_diety.id_dieta = dieta.id_dieta \
                            LEFT JOIN potraviny ON potraviny.id_potravina = potraviny_diety.id_potravina \
                            GROUP BY id_dieta \
                            ORDER BY nazov_diety"
                )
    
    def zmaz_dietu(self, id_dieta):
        self.dotaz("DELETE FROM dieta WHERE id_dieta = " + str(id_dieta))
        self.dotaz("DELETE FROM potraviny_diety WHERE id_dieta = " + str(id_dieta))
        self.dotaz("DELETE FROM rozdelenie_do_jedal WHERE id_dieta = " + str(id_dieta))
        
    def zmaz_prvok_diety(self, id_dieta, id_potravina):
        self.dotaz("DELETE FROM potraviny_diety WHERE id_dieta = " + str(id_dieta) + " AND id_potravina = " + str(id_potravina))
        self.dotaz("DELETE FROM rozdelenie_do_jedal WHERE id_dieta = " + str(id_dieta) + " AND id_potravina = " + str(id_potravina))
        
    def pridaj_potravinu_do_potravin(self, nazov_potraviny, sacharidy, tuky, bielkoviny, id_kategoria_jedla):
        self.dotaz_premenna("INSERT INTO potraviny \
                            (nazov, sacharidy, tuky, bielkoviny, id_kategoria_jedla) \
                            VALUES (%s, %s, %s, %s, %s)",
                            (nazov_potraviny, sacharidy, tuky, bielkoviny, id_kategoria_jedla))
    
    def vrat_potravinu_z_nazvu(self, nazov_potraviny):
        return self.dotaz_premenna("SELECT * FROM potraviny WHERE nazov = %s", (nazov_potraviny, ))
    
    def vrat_nazov_potraviny_z_id(self, id_potravina):
        return self.dotaz_premenna("SELECT nazov FROM potraviny WHERE id_potravina = %s", (id_potravina, ))
    
    def zmaz_potravinu(self, id_potravina):
        self.dotaz_premenna("DELETE FROM potraviny WHERE id_potravina = %s", (id_potravina, ))
    
    def zmen_potravinu_v_potravinach(self, id_potravina, nazov_potraviny, sacharidy, tuky, bielkoviny, id_kategoria_jedla):
        self.dotaz_premenna(
            "UPDATE potraviny SET \
             nazov = %s, \
             sacharidy = %s, \
             tuky = %s, \
             bielkoviny = %s, \
             id_kategoria_jedla = %s \
             WHERE id_potravina = %s",
             (nazov_potraviny, sacharidy, tuky, bielkoviny, id_kategoria_jedla, id_potravina)
        )
    
    def vrat_potravinu_z_id(self, id_potravina):
        return self.dotaz_premenna("SELECT * FROM potraviny WHERE id_potravina = %s", (id_potravina, ))
    
    def vrat_potraviny_diety_pre_priradenie (self, id_dieta):
        return self.dotaz(
            "SELECT potraviny.id_potravina, nazov, mnozstvo \
            FROM potraviny_diety \
            LEFT JOIN dieta ON potraviny_diety.id_dieta = dieta.id_dieta \
            LEFT JOIN potraviny ON potraviny.id_potravina = potraviny_diety.id_potravina \
            WHERE dieta.id_dieta = " + str(id_dieta)
        )
    
    def vrat_rozdelenie_do_jedal(self,id_dieta):
        return self.dotaz(
            "SELECT * FROM rozdelenie_do_jedal \
            WHERE id_dieta = " + str(id_dieta)
        )
    
    def vrat_zaznam(self, id_dieta, id_potravina):
        return self.dotaz(
            "SELECT * FROM rozdelenie_do_jedal \
            WHERE id_dieta = " + str(id_dieta) + " AND id_potravina = " + str(id_potravina)
        )
    
    def zmen_hodnoty_prerozdelenia(self, id_dieta, id_potravina, mnozstvo):
        self.dotaz(
            "UPDATE rozdelenie_do_jedal SET \
            prve_jedlo = " + str(mnozstvo[1]) + ", \
            druhe_jedlo = " + str(mnozstvo[2]) + ", \
            tretie_jedlo = " + str(mnozstvo[3]) + ", \
            stvrte_jedlo = " + str(mnozstvo[4]) + ", \
            piate_jedlo = " + str(mnozstvo[5]) + ", \
            sieste_jedlo = " + str(mnozstvo[6]) + " \
            WHERE id_dieta = " + str(id_dieta) + " AND id_potravina = " + str(id_potravina)
        )
    
    def pridaj_hodnoty_prerozdelenia(self, id_dieta, id_potravina, mnozstvo):
        self.dotaz_premenna(
            "INSERT INTO rozdelenie_do_jedal \
            (id_dieta, id_potravina, prve_jedlo, druhe_jedlo, tretie_jedlo, stvrte_jedlo, \
            piate_jedlo, sieste_jedlo) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (id_dieta, id_potravina, mnozstvo[1], mnozstvo[2], mnozstvo[3], mnozstvo[4], mnozstvo[5], mnozstvo[6])
        )
    
    def vrat_rozdelenie (self, id_dieta):
        return self.dotaz(
            "SELECT nazov, prve_jedlo, druhe_jedlo, tretie_jedlo, stvrte_jedlo, \
            piate_jedlo, sieste_jedlo, sacharidy, tuky, bielkoviny \
            FROM rozdelenie_do_jedal \
            LEFT JOIN potraviny on potraviny.id_potravina = rozdelenie_do_jedal.id_potravina \
            WHERE id_dieta = " + str(id_dieta) + " ORDER BY nazov"
        )
        
    def zmaz_prerozdelenie_prvku (self, id_dieta, id_potravina):
        self.dotaz("DELETE FROM rozdelenie_do_jedal WHERE id_dieta = " + str(id_dieta) + " AND id_potravina = " + str(id_potravina))
    
    def dotaz (self, dotaz):
        self.mysql_connect()
        self.mycursor.execute(dotaz)
        data = self.mycursor.fetchall()
        self.disconnect()
        return data
    
    def dotaz_premenna (self, dotaz, premenna):
        self.mysql_connect()
        self.mycursor.execute(dotaz, premenna)
        data = self.mycursor.fetchall()
        self.disconnect()
        return data
    
    def disconnect(self):
        self.mydb.close()