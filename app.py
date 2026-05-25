import streamlit as st
from PIL import Image
import requests
import io

# =========================================================
# IMPORT TWOICH BAZ DANYCH
# =========================================================

from ziola import BAZA_ZIOL
from drzewa import BAZA_DRZEW
from grzyby import BAZA_GRZYBOW
from slownik import MAPOWANIE_AI

# =========================================================
# KONFIGURACJA HUGGING FACE
# =========================================================

# Wklej tutaj swój token Hugging Face
HF_TOKEN = "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"

# Lepszy model do rozpoznawania obrazów
API_URL = "https://api-inference.huggingface.co/models/google/vit-base-patch16-224"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# =========================================================
# FUNKCJA ANALIZY AI
# =========================================================

def analizuj_zdjecie_przez_api(obraz_pil):

    bufor = io.BytesIO()

    # Konwersja do RGB
    obraz_rgb = obraz_pil.convert("RGB")

    # Zapis do bufora
    obraz_rgb.save(bufor, format="JPEG")

    dane_binarne = bufor.getvalue()

    try:

        odpowiedz = requests.post(
            API_URL,
            headers=headers,
            data=dane_binarne,
            timeout=30
        )

        st.write("Status API:", odpowiedz.status_code)

        if odpowiedz.status_code == 200:

            wynik = odpowiedz.json()

            st.write("Odpowiedź AI:")
            st.write(wynik)

            return wynik

        else:

            st.error("Błąd API")
            st.write(odpowiedz.text)

    except Exception as e:

        st.error(f"Błąd połączenia: {e}")

    return None


# =========================================================
# KONFIGURACJA STRONY
# =========================================================

st.set_page_config(
    page_title="Pomocnik zielarza",
    page_icon="🌿",
    layout="wide"
)

# =========================================================
# NAGŁÓWEK
# =========================================================

st.title("🌿 Pomocnik zielarza")
st.subheader("Rozpoznawanie ziół, drzew i grzybów przez AI")

# =========================================================
# WYBÓR SPOSOBU DODANIA ZDJĘCIA
# =========================================================

opcja = st.radio(
    "Wybierz sposób dodania zdjęcia:",
    (
        "Wgraj plik z urządzenia",
        "Zrób zdjęcie aparatem"
    )
)

zdjecie_plik = None

if opcja == "Wgraj plik z urządzenia":

    zdjecie_plik = st.file_uploader(
        "Wybierz zdjęcie",
        type=["jpg", "jpeg", "png"]
    )

else:

    zdjecie_plik = st.camera_input(
        "Zrób zdjęcie"
    )

# =========================================================
# ANALIZA
# =========================================================

if zdjecie_plik is not None:

    obraz = Image.open(zdjecie_plik)

    st.image(
        obraz,
        caption="Twoje zdjęcie",
        use_container_width=True
    )

    if st.button(
        "🔍 Uruchom analizę AI",
        type="primary"
    ):

        with st.spinner("AI analizuje obraz..."):

            wyniki_ai = analizuj_zdjecie_przez_api(obraz)

        rozpoznany_gatunek = None

        # =====================================================
        # ODCZYT WYNIKÓW AI
        # =====================================================

        if (
            wyniki_ai
            and isinstance(wyniki_ai, list)
            and len(wyniki_ai) > 0
        ):

            najlepszy_wynik = wyniki_ai[0]

            if "label" in najlepszy_wynik:

                etykieta_ai = najlepszy_wynik["label"].lower()

                st.success(f"AI rozpoznało: {etykieta_ai}")

                # Usunięcie przecinków
                glowna_etykieta = (
                    etykieta_ai
                    .split(",")[0]
                    .strip()
                )

                # =================================================
                # DOPASOWANIE DO SŁOWNIKA
                # =================================================

                if glowna_etykieta in MAPOWANIE_AI:

                    rozpoznany_gatunek = MAPOWANIE_AI[
                        glowna_etykieta
                    ]

                else:

                    # awaryjne wyszukiwanie
                    for klucz, wartosc in MAPOWANIE_AI.items():

                        if klucz in etykieta_ai:

                            rozpoznany_gatunek = wartosc
                            break

        # =====================================================
        # WYSZUKIWANIE W BAZACH
        # =====================================================

        if rozpoznany_gatunek:

            dane_obiektu = None
            kategoria = ""

            # =============================================
            # ZIOŁA
            # =============================================

            if rozpoznany_gatunek in BAZA_ZIOL:

                dane_obiektu = BAZA_ZIOL[
                    rozpoznany_gatunek
                ]

                kategoria = "🌿 Zioła"

            # =============================================
            # DRZEWA
            # =============================================

            elif rozpoznany_gatunek in BAZA_DRZEW:

                dane_obiektu = BAZA_DRZEW[
                    rozpoznany_gatunek
                ]

                kategoria = "🌳 Drzewa"

            # =============================================
            # GRZYBY
            # =============================================

            elif rozpoznany_gatunek in BAZA_GRZYBOW:

                dane_obiektu = BAZA_GRZYBOW[
                    rozpoznany_gatunek
                ]

                kategoria = "🍄 Grzyby"

            # =============================================
            # WYŚWIETLENIE DANYCH
            # =============================================

            if dane_obiektu:

                st.success("🎯 Obiekt znaleziony w atlasie!")

                st.info(kategoria)

                st.markdown(
                    f"## {rozpoznany_gatunek}"
                )

                st.markdown(
                    f"### Łacina: {dane_obiektu['lacina']}"
                )

                kol1, kol2 = st.columns(2)

                # =========================================
                # LEWA KOLUMNA
                # =========================================

                with kol1:

                    tab1, tab2 = st.tabs(
                        [
                            "📋 Pozyskiwanie",
                            "🧪 Zastosowanie"
                        ]
                    )

                    with tab1:

                        st.write(
                            dane_obiektu["pozyskiwanie"]
                        )

                    with tab2:

                        st.write(
                            dane_obiektu["przepis"]
                        )

                # =========================================
                # PRAWA KOLUMNA
                # =========================================

                with kol2:

                    if (
                        "karta" in dane_obiektu
                        and dane_obiektu["karta"]
                    ):

                        try:

                            obraz_karty = Image.open(
                                dane_obiektu["karta"]
                            )

                            st.image(
                                obraz_karty,
                                caption=f"Karta botaniczna: {rozpoznany_gatunek}",
                                use_container_width=True
                            )

                        except Exception as e:

                            st.warning(
                                f"Nie znaleziono pliku karty: {e}"
                            )

            else:

                st.warning(
                    "AI rozpoznało obiekt, ale nie ma go jeszcze w bazie atlasu."
                )

        else:

            st.error(
                "AI nie potrafiło dopasować obiektu do słownika."
            )

            st.info(
                "Dodaj więcej nazw do MAPOWANIE_AI w pliku slownik.py"
            )
