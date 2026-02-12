import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- BEÁLLÍTÁSOK ---
# IDE MÁSOLD BE AZ ÚJ KULCSOT (Az idézőjelek maradjanak!)
my_api_key = "AIzaSyCHOIsYHBmhXVbUQ6ew7s44-OWeUsxdpNs"

st.set_page_config(page_title="Gasztró-Spóroló", page_icon="🍳")

# --- KULCS ELLENŐRZÉSE ÉS AKTIVÁLÁSA ---
try:
    if "AIza" not in my_api_key:
        st.error("⚠️ Hiba: Még nem másoltad be a kulcsot a kód 6. sorába!")
        st.stop()
    
    genai.configure(api_key=my_api_key)

except Exception as e:
    st.error(f"Hiba a kulcs beállításánál: {e}")
    st.stop()

# --- FELÜLET ---
st.title("🍳 Gasztró-Spóroló")
st.write("Szia! Küldj egy képet vagy írd be, mid van, és segítek főzni!")

col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader("📸 Kép feltöltése", type=["jpg", "jpeg", "png"])
with col2:
    ingredients_text = st.text_area("📝 Vagy írd be itt:", height=100)

# --- A LÉNYEG (JAVÍTVA) ---
if st.button("Mehet! 🚀", type="primary"):
    with st.spinner('A séf gondolkodik... (Ez eltarthat pár másodpercig)'):
        try:
            # Itt volt a hiba legutóbb - most javítva:
            # Ez létrehozza az AI objektumot (NEM string!)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # Bemenet összeállítása
            prompt = "Te egy kreatív szakács vagy. Adj receptötleteket ezekből az alapanyagokból. Legyen egy egyszerű (csak ezekből) és egy bevásárlós (extra hozzávalókkal)."
            inputs = [prompt]
            
            if ingredients_text:
                inputs.append(f"Alapanyagok: {ingredients_text}")
            if uploaded_file:
                img = Image.open(uploaded_file)
                inputs.append(img)
                
            if len(inputs) == 1:
                st.warning("Kérlek adj meg legalább egy alapanyagot vagy képet!")
            else:
                # Generálás indítása
                response = model.generate_content(inputs)
                
                st.success("Kész! Íme az ötletek:")
                st.markdown("---")
                st.markdown(response.text)
                
        except Exception as e:
            # Ha még mindig 404 van, itt kiírjuk szépen
            err_msg = str(e)
            if "404" in err_msg:
                st.error("🚨 HIBA: 404 (Nem található)")
                st.warning("""
                Ez azt jelenti, hogy a KULCS nem jó projekthez tartozik.
                Biztos, hogy a 'Create API key in NEW PROJECT' opciót választottad a Google AI Studio-ban?
                """)
            else:
                st.error(f"Váratlan hiba történt: {err_msg}")










