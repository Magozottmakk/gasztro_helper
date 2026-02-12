import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. Konfiguráció (A Secrets-ből olvassa ki a kulcsot)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Hiányzik a GOOGLE_API_KEY a Secrets beállításokból!")

# 2. Az oldal kinézete
st.set_page_config(page_title="Gasztró-Spóroló", page_icon="🍳")
st.title("🍳 Gasztró-Spóroló AI")
st.write("Tölts fel egy képet a hűtőd tartalmáról, vagy írd be, mid van!")

# 3. Bemenet: Kép vagy Szöveg
uploaded_file = st.file_uploader("Fotó feltöltése az alapanyagokról...", type=["jpg", "jpeg", "png"])
ingredients_text = st.text_input("Vagy írd be ide az alapanyagokat:", placeholder="Pl. 3 tojás, fél doboz tejföl...")

# 4. A "Mágia" Gomb
if st.button("Receptek keresése 🚀"):
    if not uploaded_file and not ingredients_text:
        st.error("Kérlek, adj meg legalább egy képet vagy írd be az alapanyagokat!")
    else:
        with st.spinner('Az AI séf gondolkodik és az akciós újságokat bújják...'):
            try:
                # Modell betöltése (Google Search bekapcsolva!)
                # A 'gemini-2.0-flash' a leggyorsabb és legolcsóbb erre
                model = genai.GenerativeModel('gemini-2.0-flash') 
                
                # A Prompt összeállítása (ugyanaz, amit a Gemben használtál)
                system_prompt = """
                Te egy Gasztró-Spóroló asszisztens vagy. 
                1. Azonosítsd az alapanyagokat.
                2. Adj egy receptet, amihez NEM kell más.
                3. Adj egy receptet, amihez kell más, és írd ki, hogy a hiányzó elem (pl. gomba) általában hol kapható olcsón Magyarországon.
                Használj formázást, emojikat.
                """
                
                inputs = [system_prompt]
                
                if ingredients_text:
                    inputs.append(f"Ezek vannak nálam: {ingredients_text}")
                
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    inputs.append(image)

                # Válasz generálása
                response = model.generate_content(inputs)
                
                # Eredmény kiírása
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Hiba történt: {e}")
                st.info("Ellenőrizd, hogy az API kulcsod helyes-e!")

# 5. Lábléc
st.markdown("---")
st.caption("Powered by Google Gemini API | Az árak tájékoztató jellegűek.")