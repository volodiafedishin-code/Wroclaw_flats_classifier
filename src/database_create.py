import sqlite3
import os
# 1. Połączenie z bazą (plik zostanie utworzony w pamięci Colab)
Base_dir = os.path.dirname(os.path.abspath(__file__))
BAZA_PATH=os.path.join(Base_dir,'..','data','uczelnie.db')
polaczenie = sqlite3.connect(BAZA_PATH)
kursor = polaczenie.cursor()

# 2. Tworzenie tabeli SQL
# Nazwa, Szerokość (lat), Długość (lng)
kursor.execute('''
    CREATE TABLE IF NOT EXISTS punkty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazwa TEXT NOT NULL,
        lat REAL NOT NULL,
        lng REAL NOT NULL
    )
''')

# 3. Dodawanie danych (PWr, UWr, EZN)
dane_uczelni = [
    # Universities — Public
    ('Politechnika Wrocławska', 51.1107, 17.0618),
    ('Uniwersytet Wrocławski', 51.1140, 17.0345),
    ('Uniwersytet Ekonomiczny we Wrocławiu', 51.0886, 17.0270),
    ('Uniwersytet Przyrodniczy', 51.1105, 17.0592),
    ('Uniwersytet Medyczny im. Piastów Śląskich', 51.1165, 17.0700),
    ('Akademia Sztuk Pięknych im. E. Gepperta', 51.1108, 17.0425),
    ('Akademia Wojsk Lądowych', 51.1396, 17.0528),
    ('Akademia Wychowania Fizycznego', 51.1171, 17.0981),
    ('Akademia Muzyczna im. K. Lipińskiego', 51.1145, 17.0224),
    ('Akademia Sztuk Teatralnych im. L. Schillera', 51.1075, 17.0381),
    ('Papieski Wydział Teologiczny', 51.1151, 17.0436),

    # Universities — Private
    ('Uniwersytet SWPS', 51.1448, 17.0636),
    ('Uniwersytet WSB Merito', 51.1154, 16.9942),
    ('Uniwersytet Dolnośląski', 51.1119, 16.9912),
    ('Wrocławska Akademia Biznesu', 51.0855, 17.0164),
    ('Międzynarodowa WSL i Transportu', 51.1258, 17.0588),
    ('Wyższa Szkoła Humanistyczna', 51.1272, 17.0525),
    ('Wyższa Szkoła Prawa', 51.1178, 17.0189),
    ('Coventry University Wroclaw', 51.0963, 17.0285),
    ('WSZiA Edukacja', 51.0930, 17.0380),
    ('Niepubliczna Wyższa Szkoła Medyczna', 51.1185, 17.0540),
    ('Ewangelikalna Wyższa Szkoła Teologiczna', 51.1145, 17.0405),
    ('Apeiron — WSBPiI Wydział Wrocław', 51.0875, 17.0223),
    ('Wyższa Szkoła Kształcenia Zawodowego', 51.1100, 17.0200),
    ('Horyzont — Wrocławska WSI Stosowanej', 51.1200, 17.0500),
    ('Wyższa Szkoła Sportu im. prof. R. Panfila', 51.1171, 17.0981),
    ('Szkoła Wyższa Rzemiosł Artystycznych', 51.1108, 17.0425),
    ('Varsovia — Uczelnia Biznesu i Nauk Stosowanych', 51.1100, 17.0400),
    ('WSIiZ Copernicus', 51.1147, 17.0263),

    # High Schools — Public
    ('I LO im. Danuty Siedzikówny "Inki"', 51.1189, 17.0461),
    ('II LO im. Piastów Śląskich (OMS)', 51.1121, 17.0566),
    ('III LO im. Adama Mickiewicza', 51.1171, 17.0248),
    ('IV LO im. Stefana Żeromskiego', 51.1026, 17.0483),
    ('V LO im. Jakuba Jasińskiego', 51.0945, 17.0232),
    ('VI LO im. Bolesława Prusa', 51.1315, 17.0254),
    ('VII LO im. K.K. Baczyńskiego', 51.0921, 17.0185),
    ('VIII LO im. Bolesława Krzywoustego', 51.0935, 17.0181),
    ('IX LO im. Juliusza Słowackiego', 51.1041, 17.0392),
    ('X LO im. Stefanii Sempołowskiej', 51.1278, 17.0289),
    ('XI LO im. Stanisława Konarskiego', 51.1132, 17.0864),
    ('XII LO im. Bolesława Chrobrego', 51.1075, 17.0211),
    ('XIII LO im. Aleksandra Fredry', 51.1051, 17.0465),
    ('XIV LO im. Polonii Belgijskiej', 51.1302, 17.0752),
    ('XV LO im. Piotra Wysockiego', 51.1122, 16.9634),
    ('XVI LO — Liceum Kreatywności', 51.1120, 17.0590),
    ('XVII LO im. Agnieszki Osieckiej', 51.1017, 17.0163),
    ('XVIII LO (Młodych Techników)', 51.1136, 17.0142),
    ('XIX LO — ZS Ochrony Środowiska', 51.1380, 16.9780),
    ('XX LO (ZSTiE Hauke-Bosaka)', 51.1053, 17.0465),
    ('XXII LO — Lotnicze Zakłady Naukowe', 51.1303, 17.0555),
    ('XXIII LO (ZS nr 1, Śródmieście)', 51.1100, 17.0170),
    ('XXIV LO ze Sportowymi', 51.0901, 17.0160),
    ('XXX LO — Liceum Sportowe (Nowodworska)', 51.1130, 16.9580),
    ('ALO PWr — Akademickie Liceum Politechniki Wrocł.', 51.1070, 17.0612),

    # High Schools — Private
    ('LO Urszulanek', 51.1133, 17.0388),
    ('LO Salezjanów', 51.0892, 17.0452),
    ('LO AMIGO — Społeczne Integracyjne LO', 51.0969, 17.0475),
    ('Ekola — LO', 51.0915, 17.0225),
    ('LO ALA — Autorskie Licea Artystyczne', 51.0920, 17.0498),
    ('LO Olimp TEB Eduкаcja', 51.0935, 17.0520),
    ('ASSA — Społeczne LO nr 1', 51.0940, 17.0480),
    ('Copernicus — Akademickie LO (WSIiZ)', 51.1147, 17.0263),
    ('KLO — Katolickie LO NMP Pośredniczki Łask', 51.1330, 17.1050),
    ('LO Omega dla Dorosłych', 51.1100, 17.0322),
    ('Główna Wojskowa Szkoła Średnia — LO', 51.1400, 17.0530),

    # Technical Schools
    ('Technikum nr 1 im. K. Atatürka (ZS nr 1)', 51.1100, 17.0170),
    ('Technikum nr 2 — Budowlane (ZSB)', 51.0930, 16.9915),
    ('Technikum nr 3 (ZS nr 18, Młodych Techników)', 51.1136, 17.0142),
    ('Technikum nr 8 — Ekonomiczne (ZSE-O)', 51.0901, 17.0160),
    ('Technikum nr 9 — Gastronomiczno-Hotelarskie', 51.0840, 17.0195),
    ('Technikum nr 10 — EZN (ul. Braniborska 57)', 51.1095, 17.0012),
    ('Technikum nr 11 — Elektroniczne (ZSE)', 51.1078, 17.0082),
    ('Technikum nr 12 — Logistyczne (ul. Dawida 9-11)', 51.0964, 17.0385),
    ('Technikum nr 13 — ZSEA (ul. Worcella 3)', 51.1078, 17.0082),
    ('Technikum nr 14 — Integracyjne (Nowodworska)', 51.1130, 16.9580),
    ('Technikum nr 15 — Grafika/Design (Skwierzyńska)', 51.0991, 17.0188),
    ('Technikum nr 16 — Hotelarsko-Gastr. (ZS nr 3)', 51.0898, 17.0375),
    ('Technikum nr 18 — Samochodowe (ul. Ślężna)', 51.0945, 17.0280),
    ('Technikum nr 19 — Handlowe (ZS nr 8, Reja)', 51.1120, 17.0590),
    ('Technikum nr 20 — ZSTiE (Hauke-Bosaka 21)', 51.1053, 17.0465),
    ('Technikum Ekonomiczne ZS nr 23 (ul. Dawida)', 51.0964, 17.0385),
    ('LZN — Lotnicze Zakłady Naukowe (Technikum)', 51.1303, 17.0555),

    # Post-Secondary Schools
    ('SP nr 2 — ZSEA Worcella (policealna ekonom.)', 51.1078, 17.0082),
    ('SP nr 4 — EZN Braniborska (policealna elektr.)', 51.1095, 17.0012),
    ('SP nr 11 — LZN Kiełczowska (policealna)', 51.1303, 17.0555),
    ('SP nr 12 — ZS Logistyczne Dawida (policealna)', 51.0964, 17.0385),
    ('Dolnośląska Szkoła Policealna Medyczna (Stawowa)', 51.1008, 17.0336),
]
# Wstawiamy dane tylko jeśli tabela jest pusta
kursor.executemany('INSERT INTO punkty (nazwa, lat, lng) VALUES (?, ?, ?)', dane_uczelni)

# 4. Zapisanie zmian i zamknięcie
polaczenie.commit()
polaczenie.close()

print("Baza danych 'uczelnie.db' została utworzona! 🎉")