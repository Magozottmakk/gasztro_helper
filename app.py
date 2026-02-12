import streamlit as st
import google.generativeai as genai
import os

st.title("🔧 Diagnosztika")

# 1. Ellenőrizzük a Kulcsot
api_key = st.secrets.get("GOOGLE_API_KEY")
if not api_key:
    st.error("HIBA: Nincs beállítva az API kulcs a Secrets-ben!")
    st.stop()
else:
    st.success("✅ API Kulcs megtalálva.")
    genai.configure(api_key=api_key)

# 2. Ellenőrizzük a Verziót (EZ A LÉNYEG!)
try:
    version = genai.__version__
    st.write(f" telepített Google verzió: **{version}**")
    
    # Ha a verzió 0.7.0 alatti, akkor ez a baj!
    if version < "0.7.0":
        st.error("🚨 A VERZIÓ TÚL RÉGI! A Flash modellhez legalább 0.7.0 kell.")
        st.info("Megoldás: Frissítsd a requirements.txt fájlt és indítsd újra az Appot.")
    else:
        st.success("✅ A verzió megfelelő.")

except Exception as e:
    st.error(f"Nem sikerült verziót olvasni: {e}")

# 3. Listázzuk ki, mit lát a szerver
st.write("---")
st.write("🔍 Elérhető modellek listázása a kulcsoddal:")

if st.button("Modellek lekérdezése"):
    try:
        found_flash = False
        for m in genai.list_models():
            st.code(f"{m.name}")
            if "flash" in m.name:
                found_flash = True
        
        if found_flash:
            st.success("✅ A 'gemini-1.5-flash' elérhető! Használhatod a kódban.")
        else:
            st.error("❌ A rendszer nem látja a Flash modellt.")
            
    except Exception as e:
        st.error(f"Hiba a listázáskor: {e}")



