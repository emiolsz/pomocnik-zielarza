import streamlit as cls_st
from PIL import Image
import requests

# 1. Importowanie Twoich naukowych baz danych i słownika AI
from ziola import BAZA_ZIOL
from drzewa import BAZA_DRZEW
from grzyby import BAZA_GRZYBOW
from slownik import MAPOWANIE_AI  # Pobieranie słownika z wgranego pliku

# Adres darmowego modelu klasyfikacji przyrody w chmurze Hugging Face
API_URL = "https://huggingface.co"

def analizuj_zdjecie_przez_api(obraz_pil):
    import io
    bufor = io.BytesIO()
    obraz_pil.save(bufor, format="JPEG")
    dane_binarne = bufor.getvalue()
    
    try:
        odpowiedz = requests.post(API_URL, data=dane_binarne)
        if odpowiedz.status_code == 200:
            return odpowiedz.json()
    except Exception:
        pass
    return None

# 2. Konfiguracja strony internetowej
cls_st.set_page_config(
    page_title="Pomocnik zielarza",
    page_icon="🌿",
    layout="wide"  # Szeroki układ ekranu na dwie kolumny
)

# Nagłówek aplikacji
cls_st.title("🌿 Pomocnik zielarza")
cls_st.subheader("Naukowa baza wiedzy o ziołach, drzewach i grzybach")

opcja = cls_st.radio(
    "Wybierz sposób dodania zdjęcia:",
    ("Wgraj plik z urządzenia", "Zrób zdjęcie aparatem")
)

zdjecie_plik = None
if opcja == "Wgraj plik z urządzenia":
    zdjecie_plik = cls_st.file_uploader("Wybierz zdjęcie (JPG, PNG)", type=["jpg", "jpeg", "png"])
else:
    zdjecie_plik = cls_st.camera_input("Skieruj aparat na obiekt")

if zdjecie_plik is not None:
    obraz = Image.open(zdjecie_plik)
    cls_st.image(obraz, caption="Twoje zdjęcie", use_container_width=True)
    
    if cls_st.button("Uruchom analizę AI i przeszukaj atlasy", type="primary"):
        with cls_st.spinner("Oko AI analizuje kształty i kolory surowca..."):
            wyniki_ai = analizuj_zdjecie_przez_api(obraz)
            
        rozpoznany_gatunek = None
        
        # Przetwarzanie i dopasowywanie odpowiedzi z modelu AI
        if wyniki_ai and isinstance(wyniki_ai, list) and len(wyniki_ai) > 0:
            # Pobieramy pierwszy, najbardziej prawdopodobny wynik
            najlepszy_wynik = wyniki_ai[0]
            etykieta_ai = najlepszy_wynik['label'].lower()
            
            # Czyszczenie tekstu (wyciągamy główne słowo przed przecinkiem)
            glowna_etykieta = etykieta_ai.split(',')[0].strip()
            
            # Wyszukiwanie polskiej nazwy w zaimportowanym z słownika pliku
            if glowna_etykieta in MAPOWANIE_AI:
                rozpoznany_gatunek = MAPOWANIE_AI[glowna_etykieta]
            else:
                # Awaryjne przeszukiwanie tekstu w całych frazach
                for klucz, wartosc in MAPOWANIE_AI.items():
                    if klucz in etykieta_ai:
                        rozpoznany_gatunek = wartosc
                        break
        
        # 3. Wyświetlanie naukowej wiedzy i karty botanicznej obok siebie
        if rozpoznany_gatunek:
            dane_obiektu = None
            kategoria = ""
            
            if rozpoznany_gatunek in BAZA_ZIOL:
                dane_obiektu = BAZA_ZIOL[rozpoznany_gatunek]
                kategoria = "🌿 Kategoria: Zioła lecznicze"
            elif rozpoznany_gatunek in BAZA_DRZEW:
                dane_obiektu = BAZA_DRZEW[rozpoznany_gatunek]
                kategoria = "🌳 Kategoria: Drzewa i kora"
            elif rozpoznany_gatunek in BAZA_GRZYBOW:
                dane_obiektu = BAZA_GRZYBOW[rozpoznany_gatunek]
                kategoria = "🍄 Kategoria: Grzyby"

            if dane_obiektu:
                cls_st.success("🎯 Oko AI zidentyfikowało obiekt!")
                cls_st.info(kategoria)
                cls_st.markdown(f"## {rozpoznany_gatunek}")
                cls_st.markdown(f"*Nazwa łacińska:* ***{dane_obiektu['lacina']}***")
                
                # Tworzenie dwóch kolumn obok siebie
                kol1, kol2 = cls_st.columns(2)
                
                with kol1:
                    zakladka1, zakladka2 = cls_st.tabs(["📋 Pozyskiwanie i zbiór", "🧪 Przepis / Zastosowanie"])
                    with zakladka1:
                        cls_st.write(dane_obiektu["pozyskiwanie"])
                    with zakladka2:
                        cls_st.write(dane_obiektu["przepis"])
                        
                with kol2:
                    # Ładowanie karty botanicznej przypisanej do gatunku
                    if "karta" in dane_obiektu and dane_obiektu["karta"]:
                        try:
                            obraz_karty = Image.open(dane_obiektu["karta"])
                            cls_st.image(obraz_karty, caption=f"Karta botaniczna: {rozpoznany_gatunek}", use_container_width=True)
                        except Exception:
                            cls_st.warning(f"Nie znaleziono pliku '{dane_obiektu['karta']}' na GitHubie.")
        else:
            cls_st.warning("🤖 Model AI przetwarza obraz, ale ten obiekt nie został jeszcze powiązany z żadnym opisem botanicznym.")
