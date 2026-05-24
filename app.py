import streamlit as cls_st  # Skrót cls_st zapobiega konfliktom nazw
import time
from PIL import Image

# 1. Konfiguracja strony
cls_st.set_page_config(
    page_title="Zielnik Łąkowy - Rozpoznawanie Ziół",
    page_icon="🌿",
    layout="centered"
)

# 2. Nagłówek i opis aplikacji
cls_st.title("🌿 Zielnik Łąkowy")
cls_st.subheader("Rozpoznawaj dzikie zioła i kwiaty za pomocą AI")
cls_st.write("Zrób zdjęcie rośliny na łące lub wgraj plik z galerii, aby dowiedzieć się, co to za gatunek.")

# 3. Wybór źródła obrazu przez użytkownika
opcja = cls_st.radio(
    "Wybierz sposób dodania zdjęcia:",
    ("Wgraj plik z urządzenia", "Zrób zdjęcie aparatem")
)

zdjecie_plik = None

if opcja == "Wgraj plik z urządzenia":
    zdjecie_plik = cls_st.file_uploader(
        "Wybierz zdjęcie (JPG, PNG)", 
        type=["jpg", "jpeg", "png"]
    )
else:
    zdjecie_plik = cls_st.camera_input("Skieruj aparat na roślinę")

# 4. Przetwarzanie i wyświetlanie wyniku
if zdjecie_plik is not None:
    # Otwarcie obrazu za pomocą biblioteki Pillow
    obraz = Image.open(zdjecie_plik)
    
    # Wyświetlenie podglądu zdjęcia w aplikacji
    cls_st.image(obraz, caption="Twoje zdjęcie", use_container_width=True)
    
    # Przycisk uruchamiający analizę
    if cls_st.button("Rozpoznaj roślinę", type="primary"):
        
        # Efekt ładowania (symulacja pracy modelu AI)
        with cls_st.spinner("Analizuję liście i kwiaty..."):
            time.sleep(2)  # Symulacja opóźnienia sieci/modelu
            
        # Sekcja z wynikami (na razie wpisana na sztywno)
        cls_st.success("🤖 Roślina została rozpoznana!")
        
        # Tworzenie kolumn na wyniki
        kol1, kol2 = cls_st.columns(2)
        
        with kol1:
            cls_st.metric(label="Nazwa gatunku", value="Rumianek pospolity")
            cls_st.metric(label="Pewność modelu", value="94.5%")
            
        with kol2:
            cls_st.markdown("**Krótki opis:**")
            cls_st.write(
                "Pospolita roślina jednoroczna z rodziny astrowatych. "
                "Ma silny, przyjemny aromat. Znana z właściwości "
                "przeciwzapalnych i łagodzących."
            )

