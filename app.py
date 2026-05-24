import streamlit as cls_st
from PIL import Image
from transformers import pipeline

# 1. Importowanie naukowych baz danych
from ziola import BAZA_ZIOL
from drzewa import BAZA_DRZEW
from grzyby import BAZA_GRZYBOW
from slownik import MAPOWANIE_AI

# 2. Konfiguracja strony
cls_st.set_page_config(
    page_title="Pomocnik zielarza",
    page_icon="🌿",
    layout="wide"  # Zmieniamy na 'wide', aby grafika i tekst ładnie zmieściły się obok siebie
)

@cls_st.cache_resource
def zaladuj_model_ai():
    return pipeline("image-classification", model="microsoft/resnet-50")

detektor_ai = zaladuj_model_ai()

# 3. Interfejs aplikacji
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
            wyniki_ai = detektor_ai(obraz)
            etykieta_ai = wyniki_ai[0]['label'].lower()
            glowna_etykieta = etykieta_ai.split(',')[0].strip()
            
        rozpoznany_gatunek = None
        if glowna_etykieta in MAPOWANIE_AI:
            rozpoznany_gatunek = MAPOWANIE_AI[glowna_etykieta]
        else:
            for klucz, wartosc in MAPOWANIE_AI.items():
                if klucz in etykieta_ai:
                    rozpoznany_gatunek = wartosc
                    break

        # 4. Wyświetlanie naukowej wiedzy botanicznej wraz z kartą
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
                
                # --- PODZIAŁ NA KOLUMNY ---
                # kol1 (lewa) na teksty naukowe, kol2 (prawa) na Twoją kartę botaniczną
                kol1, kol2 = cls_st.columns([1, 1])
                
                with kol1:
                    zakladka1, zakladka2 = cls_st.tabs(["📋 Pozyskiwanie i zbiór", "🧪 Przepis / Zastosowanie"])
                    with zakladka1:
                        cls_st.write(dane_obiektu["pozyskiwanie"])
                    with zakladka2:
                        cls_st.write(dane_obiektu["przepis"])
                        
                with kol2:
                    # Automatyczne ładowanie pliku karty zdefiniowanego w bazie (.png)
                    if "karta" in dane_obiektu and dane_obiektu["karta"]:
                        try:
                            obraz_karty = Image.open(dane_obiektu["karta"])
                            cls_st.image(obraz_karty, caption=f"Karta botaniczna: {rozpoznany_gatunek}", use_container_width=True)
                        except Exception:
                            cls_st.warning(f"Nie znaleziono pliku '{dane_obiektu['karta']}' na GitHubie. Upewnij się, że wielkość liter w nazwie pliku jest identyczna!")
        else:
            cls_st.warning(f"🤖 Model AI zobaczył na zdjęciu: '{glowna_etykieta}', ale ten obiekt nie został jeszcze przypisany do żadnego opisu.")
