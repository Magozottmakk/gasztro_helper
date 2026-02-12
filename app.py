import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- KONFIGURÁCIÓ ---
st.set_page_config(page_title="Gasztró-Spóroló", page_icon="🍳", layout="centered")

# API kulcs betöltése a titkos tárolóból
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("⚠️ Hiányzik az API kulcs! Kérlek állítsd be a Secrets menüben.")
    st.stop()

# --- DESIGN ---
st.title("🍳 Gasztró-Spóroló AI")
st.markdown("""
Üdv! Ez az alkalmazás segít, hogy **ne dobj ki ételt**, és **spórolj a bevásárláson**.
Tölts fel egy képet a hűtődről vagy a kamrádról!
""")

# --- BEMENETEK ---
col1, col2 = st.columns(2)

with col1:
    uploaded_file = st.file_uploader("📸 Fotó feltöltése", type=["jpg", "jpeg", "png"])

with col2:
    ingredients_text = st.text_area("📝 Vagy írd be, mid van:", height=100, placeholder="Pl. fél doboz tejföl, fonnyadt répa, 3 tojás...")

# --- LOGIKA ---
if st.button("Mit főzzek? 🧑‍🍳", type="primary"):
    
    if not uploaded_file and not ingredients_text:
        st.warning("Kérlek, tölts fel egy képet vagy írj be valamit!")
    else:
        with st.spinner('Az AI séf gondolkodik és az akciós újságokat bújják...'):
            try:
                # Modell kiválasztása - A Flash gyors és olcsó
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # A rendszerutasítás (System Prompt)
                prompt = """
                Te egy magyar "Gasztró-Spóroló" szakértő vagy.
                
                FELADAT:
                1. Azonosítsd a bemenet (kép vagy szöveg) alapján az alapanyagokat.
                2. Készíts két listát:
                   A) "🟢 PAZARLÁSMENTES": Amit MOST el tud készíteni a felhasználó (max só, bors, olaj, liszt kellhet pluszban).
                   B) "🟡 OKOS BEVÁSÁRLÓS": Egy finomabb recept, amihez 1-2 extra dolog kell.
                
                3. A "B" verziónál ÍRD KI, hogy a hiányzó alapanyag (pl. gomba, tejszín) általában melyik boltban szokott lenni jó áron Magyarországon (Lidl, Aldi, Penny, Tesco tapasztalatok alapján).
                
                Formázd a választ szépen, áttekinthetően, emojikkal!
                """
                
                # Bemenetek összegyűjtése
                inputs = [prompt]
                if ingredients_text:
                    inputs.append(f"Ezek vannak nálam: {ingredients_text}")
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    inputs.append(image)

                # Generálás
                response = model.generate_content(inputs)
                
                # Eredmény kiírása
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hiba történt: {e}")


