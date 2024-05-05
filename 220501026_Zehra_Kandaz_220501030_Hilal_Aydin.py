import pyodbc
from tkinter import *

class Gemi:
    def __init__(self, seri_no, ad, agirlik, yapim_yili):
        self.seri_no = seri_no
        self.ad = ad
        self.agirlik = agirlik
        self.yapim_yili = yapim_yili

class YolcuGemisi(Gemi):
    def __init__(self, seri_no, ad, agirlik, yapim_yili, yolcu_kapasitesi):
        super().__init__(seri_no, ad, agirlik, yapim_yili)
        self.yolcu_kapasitesi = yolcu_kapasitesi

class PetrolTankeri(Gemi):
    def __init__(self, seri_no, ad, agirlik, yapim_yili, petrol_kapasitesi):
        super().__init__(seri_no, ad, agirlik, yapim_yili)
        self.petrol_kapasitesi = petrol_kapasitesi

class KonteynerGemisi(Gemi):
    def __init__(self, seri_no, ad, agirlik, yapim_yili, konteyner_sayisi, max_agirlik):
        super().__init__(seri_no, ad, agirlik, yapim_yili)
        self.konteyner_sayisi = konteyner_sayisi
        self.max_agirlik = max_agirlik

class Sefer:
    def __init__(self, id, kalkis_tarihi, donus_tarihi, kalkis_limani):
        self.id = id
        self.kalkis_tarihi = kalkis_tarihi
        self.donus_tarihi = donus_tarihi
        self.kalkis_limani = kalkis_limani

class Liman:
    def __init__(self, ad, ulke, nufus, pasaport, demirleme_ucreti):
        self.ad = ad
        self.ulke = ulke
        self.nufus = nufus
        self.pasaport = pasaport
        self.demirleme_ucreti = demirleme_ucreti

class Calisan:
    def __init__(self, id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi):
        self.id = id
        self.ad = ad
        self.soyad = soyad
        self.adres = adres
        self.vatandaslik = vatandaslik
        self.dogum_tarihi = dogum_tarihi
        self.ise_giris_tarihi = ise_giris_tarihi

class Kaptan(Calisan):
    def __init__(self, id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans_no):
        super().__init__(id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi)
        self.lisans_no = lisans_no

class Murettebat(Calisan):
    def __init__(self, id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, gorev):
        super().__init__(id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi)
        self.gorev = gorev


#*********************************************************************************************************#

def veri_tabani_kontrol_et():
    conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Trusted_Connection=yes;")
    conn.autocommit = True

    cursor = conn.cursor()

    cursor.execute(f"SELECT database_id FROM sys.databases WHERE Name = 'GezginGemiDB'")
    veritabani_var_mi = cursor.fetchone()
        
    if veritabani_var_mi:
        print("GezginGemiDB adinda bir veritabani zaten var.")
    else:
        cursor.execute("CREATE DATABASE GezginGemiDB")
        print("GezginGemiDB adinda bir veritabani olusturuldu.")
        
    conn.close()
veri_tabani_kontrol_et()

def tablo_kontrol_et():
    conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
    conn.autocommit = True
    cursor = conn.cursor()
    tablolar = ['GEMI', 'YOLCU_GEMISI', 'PETROL_TANKERI', 'KONTEYNER_GEMISI', 'SEFER', 'LIMAN', 'KAPTAN', 'MURETTEBAT']
    for tablo in tablolar:
        cursor.execute(f"SELECT COUNT(*) FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = '{tablo}'")
        tablo_var_mi = cursor.fetchone()[0]
        if tablo_var_mi:
            print(f"{tablo} tablosu zaten var.")
        else:
            if tablo == 'GEMI':
                cursor.execute('''
                    CREATE TABLE GEMI (
                        SERI_NO VARCHAR(25) PRIMARY KEY,
                        AD VARCHAR(50) NOT NULL,
                        AGIRLIK DECIMAL(10,2) NOT NULL,
                        YAPIM_YILI INT NOT NULL,
                        GEMI_TURU VARCHAR(25) NOT NULL
                    );
                ''')
            elif tablo == 'YOLCU_GEMISI':
                cursor.execute('''
                    CREATE TABLE YOLCU_GEMISI (
                        SERI_NO VARCHAR(25) PRIMARY KEY,
                        YOLCU_KAPASITESI INT NOT NULL,
                        FOREIGN KEY (SERI_NO) REFERENCES GEMI (SERI_NO)
                    );
                ''')
            elif tablo == 'PETROL_TANKERI':
                cursor.execute('''
                    CREATE TABLE PETROL_TANKERI (
                        SERI_NO VARCHAR(25) PRIMARY KEY,
                        PETROL_KAPASITESI DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (SERI_NO) REFERENCES GEMI (SERI_NO)
                    );
                ''')
            elif tablo == 'KONTEYNER_GEMISI':
                cursor.execute('''
                    CREATE TABLE KONTEYNER_GEMISI (
                        SERI_NO VARCHAR(25) PRIMARY KEY,
                        KONTEYNER_SAYISI INT NOT NULL,
                        MAX_AGIRLIK DECIMAL(10,2) NOT NULL,
                        FOREIGN KEY (SERI_NO) REFERENCES GEMI (SERI_NO)
                    );
                ''')
            elif tablo == 'SEFER':
                cursor.execute('''
                    CREATE TABLE SEFER (
                        SEFER_ID VARCHAR(25) PRIMARY KEY,
                        KALKIS_TARIHI DATE NOT NULL,
                        DONUS_TARIHI DATE NOT NULL,
                        KALKIS_LIMANI VARCHAR(50) NOT NULL
                    );
                ''')
            elif tablo == 'LIMAN':
                cursor.execute('''
                    CREATE TABLE LIMAN (
                        LIMAN_ADI VARCHAR(50),
                        ULKE VARCHAR(50),
                        NUFUS INT NOT NULL,
                        PASAPORT BIT NOT NULL,
                        DEMIRLEME_UCRETI DECIMAL(10,2) NOT NULL,
                        PRIMARY KEY (LIMAN_ADI, ULKE)
                    );
                ''')
            elif tablo == 'KAPTAN':
                cursor.execute('''
                    CREATE TABLE KAPTAN (
                        KAPTAN_ID VARCHAR(25) PRIMARY KEY,
                        AD VARCHAR(50) NOT NULL,
                        SOYAD VARCHAR(50) NOT NULL,
                        ADRES VARCHAR(200) NOT NULL,
                        VATANDASLIK VARCHAR(50) NOT NULL,
                        DOGUM_TARIHI DATE NOT NULL,
                        ISE_GIRIS_TARIHI DATE NOT NULL,
                        LISANS_NO VARCHAR(25) NOT NULL
                    );
                ''')
            elif tablo == 'MURETTEBAT':
                cursor.execute('''
                    CREATE TABLE MURETTEBAT (
                        MURETTEBAT_ID VARCHAR(50) PRIMARY KEY,
                        AD VARCHAR(50) NOT NULL,
                        SOYAD VARCHAR(50) NOT NULL,
                        ADRES VARCHAR(200) NOT NULL,
                        VATANDASLIK VARCHAR(50) NOT NULL,
                        DOGUM_TARIHI DATE NOT NULL,
                        ISE_GIRIS_TARIHI DATE NOT NULL,
                        GOREV VARCHAR(50) NOT NULL
                    );
                ''')
            print(f"{tablo} tablosu oluşturuldu.")

    conn.close()
tablo_kontrol_et()

#*********************************************************************************************************#
gemiler = []
seferler = []
kaptanlar = []
murettebatlar = []
limanlar = []


def gemi_ekle():
    gemi_window = Tk()
    gemi_window.title("Gemi")
    gemi_window.config(background="gray")

    gemi_seri_no_label = Label(gemi_window, text="Seri No:", background="gray", fg="#ebedec", font="bold")
    gemi_seri_no_label.pack(pady=10)
    gemi_seri_no_entry = Entry(gemi_window)
    gemi_seri_no_entry.pack(padx=40, pady=10)

    gemi_ad_label = Label(gemi_window, text="Ad:", background="gray", fg="#ebedec", font="bold")
    gemi_ad_label.pack()
    gemi_ad_entry = Entry(gemi_window)
    gemi_ad_entry.pack(padx=40, pady=10)

    gemi_agirlik_label = Label(gemi_window, text="Agirlik:", background="gray", fg="#ebedec", font="bold")
    gemi_agirlik_label.pack()
    gemi_agirlik_entry = Entry(gemi_window)
    gemi_agirlik_entry.pack(padx=40, pady=10)

    gemi_yapim_yili_label = Label(gemi_window, text="Yapim Yili:", background="gray", fg="#ebedec", font="bold")
    gemi_yapim_yili_label.pack()
    gemi_yapim_yili_entry = Entry(gemi_window)
    gemi_yapim_yili_entry.pack(padx=40, pady=10)

    gemi_tur_label = Label(gemi_window, text="Gemi Turu:", background="gray", fg="#ebedec", font="bold")
    gemi_tur_label.pack(pady=10)

    def yolcu_gemisi_ekle():
        yolcu_gemisi_window = Tk()
        yolcu_gemisi_window.title("Yolcu Gemisi")
        yolcu_gemisi_window.config(background="gray")

        yolcu_kapasitesi_label = Label(yolcu_gemisi_window, text="Yolcu Kapasitesi:", background="gray", fg="#ebedec", font="bold")
        yolcu_kapasitesi_label.pack(pady=10)
        yolcu_kapasitesi_entry = Entry(yolcu_gemisi_window)
        yolcu_kapasitesi_entry.pack(padx=40, pady=10)

        def kaydet():
            yolcu_gemisi = YolcuGemisi(gemi_seri_no_entry.get(), gemi_ad_entry.get(), gemi_agirlik_entry.get(), gemi_yapim_yili_entry.get(), yolcu_kapasitesi_entry.get())
            gemiler.append(yolcu_gemisi)
            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                        "Server=DESKTOP-UPDJR59;"
                        "Database=GezginGemiDB;"
                        "Trusted_Connection=yes;")
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("INSERT INTO GEMI (SERI_NO, AD, AGIRLIK, YAPIM_YILI, GEMI_TURU) VALUES (?, ?, ?, ?, ?)",
                           (yolcu_gemisi.seri_no, yolcu_gemisi.ad, yolcu_gemisi.agirlik, yolcu_gemisi.yapim_yili, "yolcu gemisi"))
            cursor.execute("INSERT INTO YOLCU_GEMISI (SERI_NO, YOLCU_KAPASITESI) VALUES (?, ?)",
                            (yolcu_gemisi.seri_no, yolcu_gemisi.yolcu_kapasitesi))
            conn.commit()
            conn.close()

            yolcu_gemisi_window.destroy()
            gemi_window.destroy()
        kaydet_button = Button(yolcu_gemisi_window, text="kaydet", command=kaydet, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
        kaydet_button.pack(pady=10)
    
        yolcu_gemisi_window.mainloop()

    
    def petrol_tankeri_ekle():
        petrol_tankeri_window = Tk()
        petrol_tankeri_window.title("Petrol Tankeri")
        petrol_tankeri_window.config(background="gray")

        petrol_kapasitesi_label = Label(petrol_tankeri_window, text="Petrol Kapasitesi:", background="gray", fg="#ebedec", font="bold")
        petrol_kapasitesi_label.pack(pady=10)
        petrol_kapasitesi_entry = Entry(petrol_tankeri_window)
        petrol_kapasitesi_entry.pack(padx=40, pady=10)

        def kaydet():
            petrol_tankeri = PetrolTankeri(gemi_seri_no_entry.get(), gemi_ad_entry.get(), gemi_agirlik_entry.get(), gemi_yapim_yili_entry.get(), petrol_kapasitesi_entry.get())
            gemiler.append(petrol_tankeri)
            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                        "Server=DESKTOP-UPDJR59;"
                        "Database=GezginGemiDB;"
                        "Trusted_Connection=yes;")
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("INSERT INTO GEMI (SERI_NO, AD, AGIRLIK, YAPIM_YILI, GEMI_TURU) VALUES (?, ?, ?, ?, ?)",
                           (petrol_tankeri.seri_no, petrol_tankeri.ad, petrol_tankeri.agirlik, petrol_tankeri.yapim_yili), "petrol tankeri")
            cursor.execute("INSERT INTO PETROL_TANKERI (SERI_NO, PETROL_KAPASITESI) VALUES (?, ?)",
                            (petrol_tankeri.seri_no, petrol_tankeri.petrol_kapasitesi))
            conn.commit()
            conn.close()

            petrol_tankeri_window.destroy()
            gemi_window.destroy()
        kaydet_button = Button(petrol_tankeri_window, text="kaydet", command=kaydet, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
        kaydet_button.pack(pady=10)
    
        petrol_tankeri_window.mainloop()


    def konteyner_gemisi_ekle():
        konteyner_gemisi_window = Tk()
        konteyner_gemisi_window.title("Konteyner Gemisi")
        konteyner_gemisi_window.config(background="gray")

        konteyner_sayisi_kapasitesi_label = Label(konteyner_gemisi_window, text="Konteyner Sayisi Kapasitesi:", background="gray", fg="#ebedec", font="bold")
        konteyner_sayisi_kapasitesi_label.pack(pady=10)
        konteyner_sayisi_kapasitesi_entry = Entry(konteyner_gemisi_window)
        konteyner_sayisi_kapasitesi_entry.pack(padx=40, pady=10)

        max_agirlik_label = Label(konteyner_gemisi_window, text="Maksimum Agirlik:", background="gray", fg="#ebedec", font="bold")
        max_agirlik_label.pack()
        max_agirlik_entry = Entry(konteyner_gemisi_window)
        max_agirlik_entry.pack(padx=40, pady=10)

        def kaydet():
            konteyner_gemisi = KonteynerGemisi(gemi_seri_no_entry.get(), gemi_ad_entry.get(), gemi_agirlik_entry.get(), gemi_yapim_yili_entry.get(), konteyner_sayisi_kapasitesi_entry.get(), max_agirlik_entry.get())
            gemiler.append(konteyner_gemisi)
            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                        "Server=DESKTOP-UPDJR59;"
                        "Database=GezginGemiDB;"
                        "Trusted_Connection=yes;")
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute("INSERT INTO GEMI (SERI_NO, AD, AGIRLIK, YAPIM_YILI, GEMI_TURU) VALUES (?, ?, ?, ?)",
                           (konteyner_gemisi.seri_no, konteyner_gemisi.ad, konteyner_gemisi.agirlik, konteyner_gemisi.yapim_yili, "konteyner gemisi"))
            cursor.execute("INSERT INTO KONTEYNER_GEMISI (SERI_NO, KONTEYNER_SAYISI, MAX_AGIRLIK) VALUES (?, ?, ?)",
                            (konteyner_gemisi.seri_no, konteyner_gemisi.konteyner_sayisi, konteyner_gemisi.max_agirlik))
            conn.commit()
            conn.close()

            konteyner_gemisi_window.destroy()
            gemi_window.destroy()
        kaydet_button = Button(konteyner_gemisi_window, text="kaydet", command=kaydet, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
        kaydet_button.pack(pady=10)
    
        konteyner_gemisi_window.mainloop()

    yolcu_gemisi_button = Button(gemi_window, text="Yolcu Gemisi", command=yolcu_gemisi_ekle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    yolcu_gemisi_button.pack(pady=5)

    petrol_tankeri_button = Button(gemi_window, text="Petrol Tankeri", command=petrol_tankeri_ekle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    petrol_tankeri_button.pack()

    konteyner_gemisi_button = Button(gemi_window, text="Konteyner Gemisi", command=konteyner_gemisi_ekle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    konteyner_gemisi_button.pack(pady=5)

    gemi_window.mainloop()

def sefer_ekle():
    sefer_window = Tk()
    sefer_window.title("Sefer")
    sefer_window.config(background="gray")

    sefer_id_label = Label(sefer_window, text="ID:", background="gray", fg="#ebedec", font="bold")
    sefer_id_label.pack(pady=10)
    sefer_id_entry = Entry(sefer_window)
    sefer_id_entry.pack(padx=40, pady=10)

    sefer_kalkis_tarihi_label = Label(sefer_window, text="Kalkis Tarihi:", background="gray", fg="#ebedec", font="bold")
    sefer_kalkis_tarihi_label.pack()
    sefer_kalkis_tarihi_entry = Entry(sefer_window)
    sefer_kalkis_tarihi_entry.pack(padx=40, pady=10)

    sefer_donus_tarihi_label = Label(sefer_window, text="Donus Tarihi:", background="gray", fg="#ebedec", font="bold")
    sefer_donus_tarihi_label.pack()
    sefer_donus_tarihi_entry = Entry(sefer_window)
    sefer_donus_tarihi_entry.pack(padx=40, pady=10)

    sefer_kalkis_limani_label = Label(sefer_window, text="Kalkis Limani:", background="gray", fg="#ebedec", font="bold")
    sefer_kalkis_limani_label.pack()
    sefer_kalkis_limani_entry = Entry(sefer_window)
    sefer_kalkis_limani_entry.pack(padx=40, pady=10)

    def kaydet():
        sefer = Sefer(sefer_id_entry.get(), sefer_kalkis_tarihi_entry.get(), sefer_donus_tarihi_entry.get(), sefer_kalkis_limani_entry.get())
        seferler.append(sefer)
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("INSERT INTO SEFER (SEFER_ID, KALKIS_TARIHI, DONUS_TARIHI, KALKIS_LIMANI) VALUES (?, ?, ?, ?)",
                        (sefer.id, sefer.kalkis_tarihi, sefer.donus_tarihi, sefer.kalkis_limani))
        conn.commit()
        conn.close()

        sefer_window.destroy()

    kaydet_button = Button(sefer_window, text="kaydet", command=kaydet, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    kaydet_button.pack(pady=10)
    
    sefer_window.mainloop()

def kaptan_ekle():
        kaptan_window = Tk()
        kaptan_window.title("Kaptan")
        kaptan_window.config(background="gray")

        kaptan_id_label = Label(kaptan_window, text="ID:", background="gray", fg="#ebedec", font="bold")
        kaptan_id_label.pack(pady=10)
        kaptan_id_entry = Entry(kaptan_window)
        kaptan_id_entry.pack(padx=40, pady=10)

        kaptan_ad_label = Label(kaptan_window, text="Ad:", background="gray", fg="#ebedec", font="bold")
        kaptan_ad_label.pack()
        kaptan_ad_entry = Entry(kaptan_window)
        kaptan_ad_entry.pack(padx=40, pady=10)

        kaptan_soyad_label = Label(kaptan_window, text="Soyad:", background="gray", fg="#ebedec", font="bold")
        kaptan_soyad_label.pack()
        kaptan_soyad_entry = Entry(kaptan_window)
        kaptan_soyad_entry.pack(padx=40, pady=10)

        kaptan_adres_label = Label(kaptan_window, text="Adres:", background="gray", fg="#ebedec", font="bold")
        kaptan_adres_label.pack()
        kaptan_adres_entry = Entry(kaptan_window)
        kaptan_adres_entry.pack(padx=40, pady=10)

        kaptan_vatandaslik_label = Label(kaptan_window, text="Vatandaslik:", background="gray", fg="#ebedec", font="bold")
        kaptan_vatandaslik_label.pack()
        kaptan_vatandaslik_entry = Entry(kaptan_window)
        kaptan_vatandaslik_entry.pack(padx=40, pady=10)

        kaptan_dogum_tarihi_label = Label(kaptan_window, text="Dogum Tarihi:", background="gray", fg="#ebedec", font="bold")
        kaptan_dogum_tarihi_label.pack()
        kaptan_dogum_tarihi_entry = Entry(kaptan_window)
        kaptan_dogum_tarihi_entry.pack(padx=40, pady=10)

        kaptan_ise_giris_tarihi_label = Label(kaptan_window, text="Ise Giris Tarihi:", background="gray", fg="#ebedec", font="bold")
        kaptan_ise_giris_tarihi_label.pack()
        kaptan_ise_giris_tarihi_entry = Entry(kaptan_window)
        kaptan_ise_giris_tarihi_entry.pack(padx=40, pady=10)

        kaptan_lisans_no_label = Label(kaptan_window, text="Lisans No:", background="gray", fg="#ebedec", font="bold")
        kaptan_lisans_no_label.pack()
        kaptan_lisans_no_entry = Entry(kaptan_window)
        kaptan_lisans_no_entry.pack(padx=40, pady=10)

        def kaydet():
            kaptan = Kaptan(kaptan_id_entry.get(), kaptan_ad_entry.get(), kaptan_soyad_entry.get(), kaptan_adres_entry.get(), kaptan_vatandaslik_entry.get(), kaptan_dogum_tarihi_entry.get(), kaptan_ise_giris_tarihi_entry.get(), kaptan_lisans_no_entry.get())
            kaptanlar.append(kaptan)
            conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
            conn.autocommit = True
            cursor = conn.cursor()
            cursor.execute('''
            INSERT INTO KAPTAN (KAPTAN_ID, AD, SOYAD, ADRES, VATANDASLIK, DOGUM_TARIHI, ISE_GIRIS_TARIHI, LISANS_NO) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (kaptan.id, kaptan.ad, kaptan.soyad, kaptan.adres, kaptan.vatandaslik, kaptan.dogum_tarihi, kaptan.ise_giris_tarihi, kaptan.lisans_no))
            conn.commit()
            conn.close()

            kaptan_window.destroy()

        kaydet_button = Button(kaptan_window, text="kaydet", command=kaydet, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
        kaydet_button.pack(pady=10)
    
        kaptan_window.mainloop()

def murettebat_ekle():
    murettebat_window = Tk()
    murettebat_window.title("Murettebat")
    murettebat_window.config(background="gray")

    murettebat_id_label = Label(murettebat_window, text="ID:", background="gray", fg="#ebedec", font="bold")
    murettebat_id_label.pack(pady=10)
    murettebat_id_entry = Entry(murettebat_window)
    murettebat_id_entry.pack(padx=40, pady=10)

    murettebat_ad_label = Label(murettebat_window, text="Ad:", background="gray", fg="#ebedec", font="bold")
    murettebat_ad_label.pack()
    murettebat_ad_entry = Entry(murettebat_window)
    murettebat_ad_entry.pack(padx=40, pady=10)

    murettebat_soyad_label = Label(murettebat_window, text="Soyad:", background="gray", fg="#ebedec", font="bold")
    murettebat_soyad_label.pack()
    murettebat_soyad_entry = Entry(murettebat_window)
    murettebat_soyad_entry.pack(padx=40, pady=10)

    murettebat_adres_label = Label(murettebat_window, text="Adres:", background="gray", fg="#ebedec", font="bold")
    murettebat_adres_label.pack()
    murettebat_adres_entry = Entry(murettebat_window)
    murettebat_adres_entry.pack(padx=40, pady=10)

    murettebat_vatandaslik_label = Label(murettebat_window, text="Vatandaslik:", background="gray", fg="#ebedec", font="bold")
    murettebat_vatandaslik_label.pack()
    murettebat_vatandaslik_entry = Entry(murettebat_window)
    murettebat_vatandaslik_entry.pack(padx=40, pady=10)

    murettebat_dogum_tarihi_label = Label(murettebat_window, text="Dogum Tarihi:", background="gray", fg="#ebedec", font="bold")
    murettebat_dogum_tarihi_label.pack()
    murettebat_dogum_tarihi_entry = Entry(murettebat_window)
    murettebat_dogum_tarihi_entry.pack(padx=40, pady=10)

    murettebat_ise_giris_tarihi_label = Label(murettebat_window, text="Ise Giris Tarihi:", background="gray", fg="#ebedec", font="bold")
    murettebat_ise_giris_tarihi_label.pack()
    murettebat_ise_giris_tarihi_entry = Entry(murettebat_window)
    murettebat_ise_giris_tarihi_entry.pack(padx=40, pady=10)

    murettebat_gorev_label = Label(murettebat_window, text="Gorev:", background="gray", fg="#ebedec", font="bold")
    murettebat_gorev_label.pack()
    murettebat_gorev_entry = Entry(murettebat_window)
    murettebat_gorev_entry.pack(padx=40, pady=10)

    def kaydet():
        murettebat = Murettebat(murettebat_id_entry.get(), murettebat_ad_entry.get(), murettebat_soyad_entry.get(), murettebat_adres_entry.get(), murettebat_vatandaslik_entry.get(), murettebat_dogum_tarihi_entry.get(), murettebat_ise_giris_tarihi_entry.get(), murettebat_gorev_entry.get())
        murettebatlar.append(murettebat)
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("INSERT INTO MURETTEBAT (MURETTEBAT_ID, AD, SOYAD, ADRES, VATANDASLIK, DOGUM_TARIHI, ISE_GIRIS_TARIHI, GOREV) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                        (murettebat.id, murettebat.ad, murettebat.soyad, murettebat.adres, murettebat.vatandaslik, murettebat.dogum_tarihi, murettebat.ise_giris_tarihi, murettebat.gorev))
        conn.commit()
        conn.close()

        murettebat_window.destroy()

    kaydet_button = Button(murettebat_window, text="kaydet", command=kaydet, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    kaydet_button.pack(pady=10)
    
    murettebat_window.mainloop()

def liman_ekle():
    liman_window = Tk()
    liman_window.title("Liman")
    liman_window.config(background="gray")

    liman_ad_label = Label(liman_window, text="Ad:", background="gray", fg="#ebedec", font="bold")
    liman_ad_label.pack(pady=10)
    liman_ad_entry = Entry(liman_window)
    liman_ad_entry.pack(padx=40, pady=10)

    liman_ulke_label = Label(liman_window, text="Ulke:", background="gray", fg="#ebedec", font="bold")
    liman_ulke_label.pack()
    liman_ulke_entry = Entry(liman_window)
    liman_ulke_entry.pack(padx=40, pady=10)

    liman_nufus_label = Label(liman_window, text="Nufus:", background="gray", fg="#ebedec", font="bold")
    liman_nufus_label.pack()
    liman_nufus_entry = Entry(liman_window)
    liman_nufus_entry.pack(padx=40, pady=10)

    liman_pasaport_label = Label(liman_window, text="Pasaport Istiyor mu?:\n(evet: 1, hayir: 0)", background="gray", fg="#ebedec", font="bold")
    liman_pasaport_label.pack()
    liman_pasaport_entry = Entry(liman_window)
    liman_pasaport_entry.pack(padx=40, pady=10)

    liman_demirleme_ucreti_label = Label(liman_window, text="Demirleme Ucreti:", background="gray", fg="#ebedec", font="bold")
    liman_demirleme_ucreti_label.pack()
    liman_demirleme_ucreti_entry = Entry(liman_window)
    liman_demirleme_ucreti_entry.pack(padx=40, pady=10)

    def kaydet():
        liman = Liman(liman_ad_entry.get(), liman_ulke_entry.get(), liman_nufus_entry.get(), liman_pasaport_entry.get(), liman_demirleme_ucreti_entry.get())
        limanlar.append(liman)
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute("INSERT INTO LIMAN (LIMAN_ADI, ULKE, NUFUS, PASAPORT, DEMIRLEME_UCRETI) VALUES (?, ?, ?, ?, ?)",
                       (liman.ad, liman.ulke, liman.nufus, liman.pasaport, liman.demirleme_ucreti))
        conn.commit()
        conn.close()

        liman_window.destroy()

    kaydet_button = Button(liman_window, text="Kaydet", command=kaydet, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    kaydet_button.pack(pady=10)

    liman_window.mainloop()

#*********************************************************************************************************#
def gemi_sil():
    gemi_window = Tk()
    gemi_window.title("Gemi")
    gemi_window.config(background="gray")

    gemi_seri_no_label = Label(gemi_window, text="Seri No:", background="gray", fg="#ebedec", font="bold")
    gemi_seri_no_label.pack(pady=10)
    gemi_seri_no_entry = Entry(gemi_window)
    gemi_seri_no_entry.pack(padx=40, pady=10)

    def sil():
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM YOLCU_GEMISI WHERE SERI_NO={gemi_seri_no_entry.get()}")
        yolcu_gemisi_mi = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM KONTEYNER_GEMISI WHERE SERI_NO={gemi_seri_no_entry.get()}")
        konteyner_gemisi_mi = cursor.fetchone()[0]

        cursor.execute(f"SELECT COUNT(*) FROM PETROL_TANKERI WHERE SERI_NO={gemi_seri_no_entry.get()}")
        petrol_tankeri_mi = cursor.fetchone()[0]

        # Hangi tabloya ait olduğunu bul
        if yolcu_gemisi_mi > 0:
            tablo_adi = "YOLCU_GEMISI"
        elif konteyner_gemisi_mi > 0:
            tablo_adi = "KONTEYNER_GEMISI"
        elif petrol_tankeri_mi > 0:
            tablo_adi = "PETROL_TANKERI"

        cursor.execute(f"DELETE FROM {tablo_adi} WHERE SERI_NO={gemi_seri_no_entry.get()}")
        cursor.execute(f"DELETE FROM GEMI WHERE SERI_NO={gemi_seri_no_entry.get()}")

        conn.commit()
        conn.close()

        gemi_window.destroy()

        for gemi in gemiler:
            if gemi.seri_no == gemi_seri_no_entry.get():
                del gemi

    sil_button = Button(gemi_window, text="Sil", command=sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sil_button.pack(pady=10)

    gemi_window.mainloop()

def sefer_sil():
    sefer_window = Tk()
    sefer_window.title("Sefer")
    sefer_window.config(background="gray")

    sefer_id_label = Label(sefer_window, text="ID:", background="gray", fg="#ebedec", font="bold")
    sefer_id_label.pack(pady=10)
    sefer_id_entry = Entry(sefer_window)
    sefer_id_entry.pack(padx=40, pady=10)

    def sil():
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM SEFER WHERE SEFER_ID={sefer_id_entry.get()}")

        conn.commit()
        conn.close()

        sefer_window.destroy()

        for sefer in seferler:
            if sefer.id == sefer_id_entry.get():
                del sefer
    
    sil_button = Button(sefer_window, text="Sil", command=sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sil_button.pack(pady=10)

    sefer_window.mainloop()

def kaptan_sil():
    kaptan_window = Tk()
    kaptan_window.title("Kaptan")
    kaptan_window.config(background="gray")

    Kaptan_id_label = Label(kaptan_window, text="ID:", background="gray", fg="#ebedec", font="bold")
    Kaptan_id_label.pack(pady=10)
    kaptan_id_entry = Entry(kaptan_window)
    kaptan_id_entry.pack(padx=40, pady=10)

    def sil():
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM KAPTAN WHERE KAPTAN_ID={kaptan_id_entry.get()}")

        conn.commit()
        conn.close()

        kaptan_window.destroy()

        for kaptan in kaptanlar:
            if kaptan.id == kaptan_id_entry.get():
                del kaptan
    
    sil_button = Button(kaptan_window, text="Sil", command=sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sil_button.pack(pady=10)

    kaptan_window.mainloop()    

def murettebat_sil():
    murettebat_window = Tk()
    murettebat_window.title("Murettebat")
    murettebat_window.config(background="gray")

    murettebat_id_label = Label(murettebat_window, text="ID:", background="gray", fg="#ebedec", font="bold")
    murettebat_id_label.pack(pady=10)
    murettebat_id_entry = Entry(murettebat_window)
    murettebat_id_entry.pack(padx=40, pady=10)

    def sil():
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM MURETTEBAT WHERE MURETTEBAT_ID={murettebat_id_entry.get()}")

        conn.commit()
        conn.close()

        murettebat_window.destroy()

        for murettebat in murettebatlar:
            if murettebat.id == murettebat_id_entry.get():
                del murettebat
    
    sil_button = Button(murettebat_window, text="Sil", command=sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sil_button.pack(pady=10)

    murettebat_window.mainloop()  

def liman_sil():
    liman_window = Tk()
    liman_window.title("Liman")
    liman_window.config(background="gray")

    liman_ad_label = Label(liman_window, text="Ad:", background="gray", fg="#ebedec", font="bold")
    liman_ad_label.pack(pady=10)
    liman_ad_entry = Entry(liman_window)
    liman_ad_entry.pack(padx=40, pady=10)

    def sil():
        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM LIMAN WHERE LIMAN_ADI={liman_ad_entry.get()}")

        conn.commit()
        conn.close()

        liman_window.destroy()

        for liman in limanlar:
            if liman.ad == liman_ad_entry.get():
                del liman
    
    sil_button = Button(liman_window, text="Sil", command=sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sil_button.pack(pady=10)

    liman_window.mainloop()  

#*********************************************************************************************************#

def gemi_duzenle():
    duzenle_window = Tk()
    duzenle_window.title("Gemi")
    duzenle_window.config(background="gray")

    seri_no_label = Label(duzenle_window, text="Seri No:", background="gray", fg="#ebedec", font="bold")
    seri_no_label.pack(pady=10)
    seri_no_entry = Entry(duzenle_window)
    seri_no_entry.pack(padx=40, pady=10)

    duzenle_label = Label(duzenle_window, text="Duzenlenecek kisim:", background="gray", fg="#ebedec", font="bold")
    duzenle_label.pack()
    duzenle_entry = Entry(duzenle_window)
    duzenle_entry.pack(padx=40, pady=10)

    def sec():
        sec_window = Tk()
        sec_window.config(background="gray")

        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()

        if duzenle_entry.get() == "ad":
            gemi_yeni_ad_label = Label(sec_window, text="Yeni Ad:", background="gray", fg="#ebedec", font="bold")
            gemi_yeni_ad_label.pack(pady=10)
            gemi_yeni_ad_entry = Entry(sec_window)
            gemi_yeni_ad_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE GEMI SET AD='{gemi_yeni_ad_entry.get()}' WHERE SERI_NO='{seri_no_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()
        
        elif duzenle_entry.get() == "agirlik":
            gemi_yeni_agirlik_label = Label(sec_window, text="Yeni Agirlik:", background="gray", fg="#ebedec", font="bold")
            gemi_yeni_agirlik_label.pack(pady=10)
            gemi_yeni_agirlik_entry = Entry(sec_window)
            gemi_yeni_agirlik_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE GEMI SET AGIRLIK='{gemi_yeni_agirlik_entry.get()}' WHERE SERI_NO='{seri_no_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()        

        elif duzenle_entry.get() == "yapim yili":
            gemi_yeni_yapim_yili_label = Label(sec_window, text="Yeni Yapim Yili:", background="gray", fg="#ebedec", font="bold")
            gemi_yeni_yapim_yili_label.pack(pady=10)
            gemi_yeni_yapim_yili_entry = Entry(sec_window)
            gemi_yeni_yapim_yili_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE GEMI SET YAPIM_YILI='{gemi_yeni_yapim_yili_entry.get()}' WHERE SERI_NO='{seri_no_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()

        elif duzenle_entry.get() == "yolcu kapasitesi":
            gemi_yeni_yolcu_kapasitesi_label = Label(sec_window, text="Yeni Yolcu Kapasitesi:", background="gray", fg="#ebedec", font="bold")
            gemi_yeni_yolcu_kapasitesi_label.pack(pady=10)
            gemi_yeni_yolcu_kapasitesi_entry = Entry(sec_window)
            gemi_yeni_yolcu_kapasitesi_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE YOLCU_GEMISI SET YOLCU_KAPASITESI='{gemi_yeni_yolcu_kapasitesi_entry.get()}' WHERE SERI_NO='{seri_no_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()

        elif duzenle_entry.get() == "petrol kapasitesi":
            gemi_yeni_petrol_kapasitesi_label = Label(sec_window, text="Yeni Petrol Kapasitesi:", background="gray", fg="#ebedec", font="bold")
            gemi_yeni_petrol_kapasitesi_label.pack(pady=10)
            gemi_yeni_petrol_kapasitesi_entry = Entry(sec_window)
            gemi_yeni_petrol_kapasitesi_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE PETROL_TANKERI SET PETROL_KAPASITESI='{gemi_yeni_petrol_kapasitesi_entry.get()}' WHERE SERI_NO='{seri_no_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()

        elif duzenle_entry.get() == "konteyner sayisi":
            gemi_yeni_konteyner_sayisi_label = Label(sec_window, text="Yeni Konteyner Sayisi:", background="gray", fg="#ebedec", font="bold")
            gemi_yeni_konteyner_sayisi_label.pack(pady=10)
            gemi_yeni_konteyner_sayisi_entry = Entry(sec_window)
            gemi_yeni_konteyner_sayisi_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE KONTEYNER_GEMISI SET KONTEYNER_SAYISI='{gemi_yeni_konteyner_sayisi_entry.get()}' WHERE SERI_NO='{seri_no_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()                

        elif duzenle_entry.get() == "max agirlik":
            gemi_yeni_max_agirlik_label = Label(sec_window, text="Yeni Max Agirlik:", background="gray", fg="#ebedec", font="bold")
            gemi_yeni_max_agirlik_label.pack(pady=10)
            gemi_yeni_max_agirlik_entry = Entry(sec_window)
            gemi_yeni_max_agirlik_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE KONTEYNER_GEMISI SET MAX_AGIRLIK='{gemi_yeni_max_agirlik_entry.get()}' WHERE SERI_NO='{seri_no_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()

        kaydet_button = Button(sec_window, text="kaydet", command=duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
        kaydet_button.pack(pady=10)

    sec_button = Button(duzenle_window, text="Sec", command=sec, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sec_button.pack(pady=10)

def sefer_duzenle():
    duzenle_window = Tk()
    duzenle_window.title("Sefer")
    duzenle_window.config(background="gray")

    id_label = Label(duzenle_window, text="ID:", background="gray", fg="#ebedec", font="bold")
    id_label.pack(pady=10)
    id_entry = Entry(duzenle_window)
    id_entry.pack(padx=40, pady=10)

    duzenle_label = Label(duzenle_window, text="Duzenlenecek Kisim:", background="gray", fg="#ebedec", font="bold")
    duzenle_label.pack()
    duzenle_entry = Entry(duzenle_window)
    duzenle_entry.pack(padx=40, pady=10)

    def sec():
        sec_window = Tk()
        sec_window.config(background="gray")

        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()

        if duzenle_entry.get() == "kalkis tarihi":
            sefer_yeni_kalkis_tarihi_label = Label(sec_window, text="Yeni Kalkis Tarihi:", background="gray", fg="#ebedec", font="bold")
            sefer_yeni_kalkis_tarihi_label.pack(pady=10)
            sefer_yeni_kalkis_tarihi_entry = Entry(sec_window)
            sefer_yeni_kalkis_tarihi_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE SEFER SET KALKIS_TARIHI='{sefer_yeni_kalkis_tarihi_entry.get()}' WHERE SEFER_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()
        
        elif duzenle_entry.get() == "donus tarihi":
            sefer_yeni_donus_tarihi_label = Label(sec_window, text="Yeni Donus Tarihi:", background="gray", fg="#ebedec", font="bold")
            sefer_yeni_donus_tarihi_label.pack(pady=10)
            sefer_yeni_donus_tarihi_entry = Entry(sec_window)
            sefer_yeni_donus_tarihi_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE SEFER SET DONUS_TARIHI='{sefer_yeni_donus_tarihi_entry.get()}' WHERE SEFER_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()        

        elif duzenle_entry.get() == "kalkis limani":
            sefer_yeni_kalkis_limani_label = Label(sec_window, text="Yeni Kalkis Limani:", background="gray", fg="#ebedec", font="bold")
            sefer_yeni_kalkis_limani_label.pack(pady=10)
            sefer_yeni_kalkis_limani_entry = Entry(sec_window)
            sefer_yeni_kalkis_limani_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE SEFER SET KALKIS_LIMANI='{sefer_yeni_kalkis_limani_entry.get()}' WHERE SEFER_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                duzenle_window.destroy()
                sec_window.destroy()

        kaydet_button = Button(sec_window, text="kaydet", command=duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
        kaydet_button.pack(pady=10)

    sec_button = Button(duzenle_window, text="Sec", command=sec, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sec_button.pack(pady=10)

def kaptan_duzenle():
    duzenle_window = Tk()
    duzenle_window.title("Kaptan")
    duzenle_window.config(background="gray")

    id_label = Label(duzenle_window, text="ID:", background="gray", fg="#ebedec", font="bold")
    id_label.pack(pady=10)
    id_entry = Entry(duzenle_window)
    id_entry.pack(padx=40, pady=10)

    duzenle_label = Label(duzenle_window, text="Duzenlenecek Kisim:", background="gray", fg="#ebedec", font="bold")
    duzenle_label.pack()
    duzenle_entry = Entry(duzenle_window)
    duzenle_entry.pack(padx=40, pady=10)

    def sec():
        sec_window = Tk()
        sec_window.config(background="gray")

        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()

        if duzenle_entry.get() == "ad":
            kaptan_yeni_ad_label = Label(sec_window, text="Yeni Ad:", background="gray", fg="#ebedec", font="bold")
            kaptan_yeni_ad_label.pack(pady=10)
            kaptan_yeni_ad_entry = Entry(sec_window)
            kaptan_yeni_ad_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE KAPTAN SET AD='{kaptan_yeni_ad_entry.get()}' WHERE KAPTAN_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()
        
        elif duzenle_entry.get() == "soyad":
            kaptan_yeni_soyad_label = Label(sec_window, text="Yeni Soyad:", background="gray", fg="#ebedec", font="bold")
            kaptan_yeni_soyad_label.pack(pady=10)
            kaptan_yeni_soyad_entry = Entry(sec_window)
            kaptan_yeni_soyad_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE KAPTAN SET SOYAD='{kaptan_yeni_soyad_entry.get()}' WHERE KAPTAN_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()        

        elif duzenle_entry.get() == "adres":
            kaptan_yeni_adres_label = Label(sec_window, text="Yeni Adres:", background="gray", fg="#ebedec", font="bold")
            kaptan_yeni_adres_label.pack(pady=10)
            kaptan_yeni_adres_entry = Entry(sec_window)
            kaptan_yeni_adres_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE KAPTAN SET ADRES='{kaptan_yeni_adres_entry.get()}' WHERE KAPTAN_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        elif duzenle_entry.get() == "vatandaslik":
            kaptan_yeni_vatandaslik_label = Label(sec_window, text="Yeni Vatandaslik:", background="gray", fg="#ebedec", font="bold")
            kaptan_yeni_vatandaslik_label.pack(pady=10)
            kaptan_yeni_vatandaslik_entry = Entry(sec_window)
            kaptan_yeni_vatandaslik_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE KAPTAN SET VATANDASLIK='{kaptan_yeni_vatandaslik_entry.get()}' WHERE KAPTAN_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        elif duzenle_entry.get() == "dogum tarihi":
            kaptan_yeni_dogum_tarihi_label = Label(sec_window, text="Yeni Dogum Tarihi:", background="gray", fg="#ebedec", font="bold")
            kaptan_yeni_dogum_tarihi_label.pack(pady=10)
            kaptan_yeni_dogum_tarihi_entry = Entry(sec_window)
            kaptan_yeni_dogum_tarihi_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE KAPTAN SET DOGUM_TARIHI='{kaptan_yeni_dogum_tarihi_entry.get()}' WHERE KAPTAN_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        elif duzenle_entry.get() == "ise giris tarihi":
            kaptan_yeni_ise_giris_tarihi_label = Label(sec_window, text="Yeni Ise Giris Tarihi:", background="gray", fg="#ebedec", font="bold")
            kaptan_yeni_ise_giris_tarihi_label.pack(pady=10)
            kaptan_yeni_ise_giris_tarihi_entry = Entry(sec_window)
            kaptan_yeni_ise_giris_tarihi_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE KAPTAN SET ISE_GIRIS_TARIHI='{kaptan_yeni_ise_giris_tarihi_entry.get()}' WHERE KAPTAN_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        elif duzenle_entry.get() == "lisans no":
            kaptan_yeni_lisans_no_label = Label(sec_window, text="Yeni Lisans No:", background="gray", fg="#ebedec", font="bold")
            kaptan_yeni_lisans_no_label.pack(pady=10)
            kaptan_yeni_lisans_no_entry = Entry(sec_window)
            kaptan_yeni_lisans_no_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE KAPTAN SET LISANS_NO='{kaptan_yeni_lisans_no_entry.get()}' WHERE KAPTAN_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        kaydet_button = Button(sec_window, text="kaydet", command=duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
        kaydet_button.pack(pady=10)

    sec_button = Button(duzenle_window, text="Sec", command=sec, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sec_button.pack(pady=10)

def murettebat_duzenle():
    duzenle_window = Tk()
    duzenle_window.title("Murettebat")
    duzenle_window.config(background="gray")

    id_label = Label(duzenle_window, text="ID:", background="gray", fg="#ebedec", font="bold")
    id_label.pack(pady=10)
    id_entry = Entry(duzenle_window)
    id_entry.pack(padx=40, pady=10)

    duzenle_label = Label(duzenle_window, text="Duzenlenecek Kisim:", background="gray", fg="#ebedec", font="bold")
    duzenle_label.pack()
    duzenle_entry = Entry(duzenle_window)
    duzenle_entry.pack(padx=40, pady=10)

    def sec():
        sec_window = Tk()
        sec_window.config(background="gray")

        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()

        if duzenle_entry.get() == "ad":
            murettebat_yeni_ad_label = Label(sec_window, text="Yeni Ad:", background="gray", fg="#ebedec", font="bold")
            murettebat_yeni_ad_label.pack(pady=10)
            murettebat_yeni_ad_entry = Entry(sec_window)
            murettebat_yeni_ad_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE MURETTEBAT SET AD='{murettebat_yeni_ad_entry.get()}' WHERE MURETTEBAT_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()
        
        elif duzenle_entry.get() == "soyad":
            murettebat_yeni_soyad_label = Label(sec_window, text="Yeni Soyad:", background="gray", fg="#ebedec", font="bold")
            murettebat_yeni_soyad_label.pack(pady=10)
            murettebat_yeni_soyad_entry = Entry(sec_window)
            murettebat_yeni_soyad_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE MURETTEBAT SET SOYAD='{murettebat_yeni_soyad_entry.get()}' WHERE MURETTEBAT_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()        

        elif duzenle_entry.get() == "adres":
            murettebat_yeni_adres_label = Label(sec_window, text="Yeni Adres:", background="gray", fg="#ebedec", font="bold")
            murettebat_yeni_adres_label.pack(pady=10)
            murettebat_yeni_adres_entry = Entry(sec_window)
            murettebat_yeni_adres_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE MURETTEBAT SET ADRES='{murettebat_yeni_adres_entry.get()}' WHERE MURETTEBAT_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        elif duzenle_entry.get() == "vatandaslik":
            murettebat_yeni_vatandaslik_label = Label(sec_window, text="Yeni Vatandaslik:", background="gray", fg="#ebedec", font="bold")
            murettebat_yeni_vatandaslik_label.pack(pady=10)
            murettebat_yeni_vatandaslik_entry = Entry(sec_window)
            murettebat_yeni_vatandaslik_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE MURETTEBAT SET VATANDASLIK='{murettebat_yeni_vatandaslik_entry.get()}' WHERE MURETTEBAT_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        elif duzenle_entry.get() == "dogum tarihi":
            murettebat_yeni_dogum_tarihi_label = Label(sec_window, text="Yeni Dogum Tarihi:", background="gray", fg="#ebedec", font="bold")
            murettebat_yeni_dogum_tarihi_label.pack(pady=10)
            murettebat_yeni_dogum_tarihi_entry = Entry(sec_window)
            murettebat_yeni_dogum_tarihi_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE MURETTEBAT SET DOGUM_TARIHI='{murettebat_yeni_dogum_tarihi_entry.get()}' WHERE MURETTEBAT_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        elif duzenle_entry.get() == "ise giris tarihi":
            murettebat_yeni_ise_giris_tarihi_label = Label(sec_window, text="Yeni Ise Giris Tarihi:", background="gray", fg="#ebedec", font="bold")
            murettebat_yeni_ise_giris_tarihi_label.pack(pady=10)
            murettebat_yeni_ise_giris_tarihi_entry = Entry(sec_window)
            murettebat_yeni_ise_giris_tarihi_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE MURETTEBAT SET ISE_GIRIS_TARIHI='{murettebat_yeni_ise_giris_tarihi_entry.get()}' WHERE MURETTEBAT_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        elif duzenle_entry.get() == "gorev":
            murettebat_yeni_gorev_label = Label(sec_window, text="Yeni Gorev:", background="gray", fg="#ebedec", font="bold")
            murettebat_yeni_gorev_label.pack(pady=10)
            murettebat_yeni_gorev_entry = Entry(sec_window)
            murettebat_yeni_gorev_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE MURETTEBAT SET GOREV='{murettebat_yeni_gorev_entry.get()}' WHERE MURETTEBAT_ID='{id_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        kaydet_button = Button(sec_window, text="kaydet", command=duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
        kaydet_button.pack(pady=10)

    sec_button = Button(duzenle_window, text="Sec", command=sec, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sec_button.pack(pady=10)

def liman_duzenle():
    duzenle_window = Tk()
    duzenle_window.title("Liman")
    duzenle_window.config(background="gray")

    ad_label = Label(duzenle_window, text="Ad:", background="gray", fg="#ebedec", font="bold")
    ad_label.pack(pady=10)
    ad_entry = Entry(duzenle_window)
    ad_entry.pack(padx=40, pady=10)

    duzenle_label = Label(duzenle_window, text="Duzenlenecek Kisim:", background="gray", fg="#ebedec", font="bold")
    duzenle_label.pack()
    duzenle_entry = Entry(duzenle_window)
    duzenle_entry.pack(padx=40, pady=10)

    def sec():
        sec_window = Tk()
        sec_window.config(background="gray")

        conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                      "Server=DESKTOP-UPDJR59;"
                      "Database=GezginGemiDB;"
                      "Trusted_Connection=yes;")
        conn.autocommit = True
        cursor = conn.cursor()

        if duzenle_entry.get() == "ulke":
            liman_yeni_ulke_label = Label(sec_window, text="Yeni Ulke:", background="gray", fg="#ebedec", font="bold")
            liman_yeni_ulke_label.pack(pady=10)
            liman_yeni_ulke_entry = Entry(sec_window)
            liman_yeni_ulke_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE LIMAN SET ULKE='{liman_yeni_ulke_entry.get()}' WHERE LIMAN_ADI='{ad_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()
        
        elif duzenle_entry.get() == "nufus":
            liman_yeni_nufus_label = Label(sec_window, text="Yeni Nufus:", background="gray", fg="#ebedec", font="bold")
            liman_yeni_nufus_label.pack(pady=10)
            liman_yeni_nufus_entry = Entry(sec_window)
            liman_yeni_nufus_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE LIMAN SET NUFUS='{liman_yeni_nufus_entry.get()}' WHERE LIMAN_ADI='{ad_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()        

        elif duzenle_entry.get() == "pasaport":
            liman_yeni_pasaport_label = Label(sec_window, text="Yeni Pasaport:", background="gray", fg="#ebedec", font="bold")
            liman_yeni_pasaport_label.pack(pady=10)
            liman_yeni_pasaport_entry = Entry(sec_window)
            liman_yeni_pasaport_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE LIMAN SET PASAPORT='{liman_yeni_pasaport_entry.get()}' WHERE LIMAN_ADI='{ad_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        elif duzenle_entry.get() == "demirleme ucreti":
            liman_yeni_demirleme_ucreti_label = Label(sec_window, text="Yeni Demirleme Ucreti:", background="gray", fg="#ebedec", font="bold")
            liman_yeni_demirleme_ucreti_label.pack(pady=10)
            liman_yeni_demirleme_ucreti_entry = Entry(sec_window)
            liman_yeni_demirleme_ucreti_entry.pack(padx=40, pady=10)

            def duzenle():
                cursor.execute(f"UPDATE LIMAN SET DEMIRLEME_UCRETI='{liman_yeni_demirleme_ucreti_entry.get()}' WHERE LIMAN_ADI='{ad_entry.get()}'")
                conn.commit()
                conn.close()

                sec_window.destroy()
                duzenle_window.destroy()

        kaydet_button = Button(sec_window, text="kaydet", command=duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
        kaydet_button.pack(pady=10)

    sec_button = Button(duzenle_window, text="Sec", command=sec, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=15)
    sec_button.pack(pady=10)    
#*********************************************************************************************************#

def secim_ekrani_goster():
    secim_window = Tk()
    secim_window.title("Kayit Formu")
    secim_window.config(background="gray")

    ekle_frame = Frame(secim_window, borderwidth=5, relief="ridge")
    ekle_frame.pack(side="left", padx=30, pady=30)
    ekle_label = Label(ekle_frame, text="EKLE", font="bold")
    ekle_label.pack(pady=10)

    gemi_ekle_button = Button(ekle_frame, text="Gemi", command=gemi_ekle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    gemi_ekle_button.pack(pady=10)

    sefer_ekle_button = Button(ekle_frame, text="Sefer", command=sefer_ekle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    sefer_ekle_button.pack(pady=10)

    kaptan_ekle_button = Button(ekle_frame, text="Kaptan", command=kaptan_ekle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    kaptan_ekle_button.pack(pady=10)

    murettebat_ekle_button = Button(ekle_frame, text="Murettebat", command=murettebat_ekle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    murettebat_ekle_button.pack(pady=10)

    liman_ekle_button = Button(ekle_frame, text="Liman", command=liman_ekle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    liman_ekle_button.pack(pady=10)

#*********************************************************************************************************#

    sil_frame = Frame(secim_window, borderwidth=5, relief="ridge")
    sil_frame.pack(side="left", padx=30, pady=30)
    sil_label = Label(sil_frame, text="SIL", font="bold")
    sil_label.pack(pady=10)

    gemi_sil_button = Button(sil_frame, text="Gemi", command=gemi_sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    gemi_sil_button.pack(pady=10)

    sefer_sil_button = Button(sil_frame, text="Sefer", command=sefer_sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    sefer_sil_button.pack(pady=10)

    kaptan_sil_button = Button(sil_frame, text="Kaptan", command=kaptan_sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    kaptan_sil_button.pack(pady=10)

    murettebat_sil_button = Button(sil_frame, text="Murettebat", command=murettebat_sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    murettebat_sil_button.pack(pady=10)

    liman_sil_button = Button(sil_frame, text="Liman", command=liman_sil, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    liman_sil_button.pack(pady=10)

#*********************************************************************************************************#

    duzenle_frame = Frame(secim_window, borderwidth=5, relief="ridge")
    duzenle_frame.pack(side="left", padx=30, pady=30)
    duzenle_label = Label(duzenle_frame, text="DUZENLE", font="bold")
    duzenle_label.pack(pady=10)

    gemi_duzenle_button = Button(duzenle_frame, text="Gemi", command=gemi_duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    gemi_duzenle_button.pack(pady=10)

    sefer_duzenle_button = Button(duzenle_frame, text="Sefer", command=sefer_duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    sefer_duzenle_button.pack(pady=10)

    kaptan_duzenle_button = Button(duzenle_frame, text="Kaptan", command=kaptan_duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    kaptan_duzenle_button.pack(pady=10)

    murettebat_duzenle_button = Button(duzenle_frame, text="Murettebat", command=murettebat_duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    murettebat_duzenle_button.pack(pady=10)

    liman_duzenle_button = Button(duzenle_frame, text="Liman", command=liman_duzenle, background="#393b3a", activebackground="#393b3a", fg="#ebedec", activeforeground="#ebedec", width=10)
    liman_duzenle_button.pack(pady=10)

    secim_window.mainloop()
secim_ekrani_goster()
