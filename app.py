import streamlit as st
import google.generativeai as genai
from PIL import Image

# ---------------------------------------------------------
# IDE MÁSOLD BE A KULCSODAT AZ IDÉZŐJELEK KÖZÉ!
# Példa: my_api_key = "AIzaSyD......"
my_api_key = "IDE_MÁSOLD_A_HOSSZÚ_AIZA_KULCSODAT"
# ---------------------------------------------------------

st.set_page_config(page_title="Gasztró-Spóroló", page_icon="🍳")
st.title("🍳 Gasztró-Spóroló (Direkt Teszt)")

# Kulcs beállítása közvetlenül
try:
    genai.configure(api_key=my_api_key)
except Exception as e:
    st.error(f"Baj van a kulccsal: {e}")

# Képfeltöltés
uploaded_file = st.file_uploader("📸 Fotó feltöltése", type=["jpg", "jpeg", "png"])
ingredients_text = st.text_input("Vagy írd be, mid van:")

if st.button("Mehet! 🚀"):
    # Ellenőrizzük, hogy kicserélted-e a szöveget
    if "IDE_MÁSOLD" in my_api_key:
        st.error("⚠️ ELFELEJTETTED BEÍRNI A KULCSOT A KÓDBA! (app.py 8. sor)")
    else:
        with st.spinner('Kapcsolódás a Google szerverekhez...'):
            try:
                # 1. Próbáljuk a legújabb modellt
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                # Egyszerű teszt üzenet
                prompt = "Szia! Mondj egy receptet ebből: "
                
                inputs = [prompt]
                if ingredients_text: inputs.append(ingredients_text)
                if uploaded_file: inputs.append(Image.open(uploaded_file))
                
                response = model.generate_content(inputs)
                st.success("MŰKÖDIK! 🎉")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"HIBA TÖRTÉNT: {e}")
                st.write("Javaslat: Ellenőrizd, hogy a kulcsod az AI Studio-ból van-e (nem Google Cloud Console), és hogy átállítottad-e a Pythont 3.10-re!")





