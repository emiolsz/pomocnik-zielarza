import streamlit as cls_st
import time
from PIL import Image

# 1. Importowanie baz danych z Twoich osobnych plików .py
from ziola import BAZA_ZIOL
from drzewa import BAZA_DRZEW
from grzyby import BAZA_GRZYBOW

# 2. Konfiguracja strony internetowej
cls_st.set_page_config(
    page_title="Wielki Atlas Natury - Zioła, Drzewa, Grzyby",
    page_icon="🌲",
    layout="centered"
)

# Nagłówek aplikacji
cls_st.title("🌲 Wielki Atlas Natury")
cls_st.subheader("Rozpoznawaj skarby lasu i łąki za pomocą AI")

# 3. Wybór sposobu dodania zdjęcia przez użytkownika
opcja = cls_st.radio(
    "Wybierz sposób dodania zdjęcia:",
    ("Wgraj plik z urządzenia", "Zrób zdjęcie aparatem")
)

zdjecie_plik = None
if opcja == "Wgraj plik z urządzenia":
    zdjecie_plik = cls_st.file_uploader("Wybierz zdjęcie (JPG, PNG)", type=["jpg", "jpeg", "png"])
else:
    zdjecie_plik = cls_st.camera_input("Skieruj aparat na obiekt")

# 4. Przetwarzanie i wyszukiwanie w bazach danych
if zdjecie_plik is not None:
    # Wyświetlenie zdjęcia użytkownika
    obraz = Image.open(zdjedzie_plik if 'zdjedzie_plik' in locals() else zdjecie_plik)
    cls_st.image(obraz, caption="Twoje zdjęcie", use_container_width=True)
    
    # --- TYMCZASOWE POLE DO TESTOWANIA BAZY ---
    # Ponieważ model AI dodamy na końcu, to pole pozwala Ci wpisać nazwę ręcznie,
    # aby sprawdzić, czy aplikacja prawidłowo czyta pliki ziola.py, drzewa.py i grzyby.py
    testowa_nazwa = cls_st.text_input(
        "Wpisz nazwę do przetestowania (np. Rumianek pospolity, Brzoza brodawkowata, Borowik szlachetny):",
        value="Rumianek pospolity"
    )
    
    if cls_st.button("Uruchom analizę i przeszukaj atlasy", type="primary"):
        with cls_st.spinner("Skanowanie struktury i przeszukiwanie baz danych..."):
            time.sleep(1.5)
            
        # Zmienna, do której zapiszemy znalezione informacje
        dane_obiektu = None
        kategoria = ""
        
        # Przeszukiwanie baz danych – sprawdzamy każdy plik po kolei
        if testowa_nazwa in BAZA_ZIOL:
            dane_obiektu = BAZA_ZIOL[testowa_nazwa]
            kategoria = "🌿 Kategoria: Zioła lecznicze"
        elif testowa_nazwa in BAZA_DRZEW:
            dane_obiektu = BAZA_DRZEW[testowa_nazwa]
            kategoria = "🌳 Kategoria: Drzewa i kora"
        elif testowa_nazwa in BAZA_GRZYBOW:
            dane_obiektu = BAZA_GRZYBOW[testowa_nazwa]
            kategoria = "🍄 Kategoria: Grzyby"

        # 5. Wyświetlanie wyników użytkownikowi
        if dane_obiektu:
            cls_st.success("🤖 Znaleziono dopasowanie w Atlasie!")
            cls_st.info(kategoria)
            
            # Główne dane: Nazwa polska i łacińska
            cls_st.markdown(f"## {testowa_nazwa}")
            cls_st.markdown(f"*Nazwa łacińska:* ***{dane_obiektu['lacina']}***")
            
            # Tworzenie czytelnych zakładek na opisy i przepisy
            zakladka1, zakladka2 = cls_st.tabs(["📋 Pozyskiwanie i zbiór", "🧪 Przepis / Zastosowanie"])
            
            with zakladka1:
                cls_st.write(dane_obiektu["pozyskiwanie"])
                
            with zakladka2:
                cls_st.write(dane_obiektu["przepis"])
        else:
            cls_st.error(f"❌ Nie znaleziono gatunku '{testowa_nazwa}' w żadnym z plików (ziola.py, drzewa.py, grzyby.py). Sprawdź pisownię!")


