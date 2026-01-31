import streamlit as st
import os
import json

# Setări pagină DJ
st.set_page_config(page_title="Hercule AI DJ", layout="wide")

# Sistemul de MEMORIE (Persistență) [cite: 2026-01-15]
STATE_FILE = "state.json"

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"party_active": False, "history": []}

def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

state = load_state()

st.title("🎧 HERCULE AI DJ - CONTROL CENTER")

# --- SECȚIUNEA PARTY (MIROTALK) ---
st.subheader("📺 Proiector & Webcam")
mirotalk_url = "https://p2p.mirotalk.com/join/hercule-dj-party" # Poți schimba numele camerei aici

if st.button("🚀 LANSEAZĂ PARTY MODE (FULL SCREEN)"):
    state["party_active"] = True
    save_state(state) [cite: 2026-01-15]
    # Deschide Mirotalk într-un tab nou
    st.write(f'<a href="{mirotalk_url}" target="_blank">Click aici pentru a deschide Camera pe tot ecranul!</a>', unsafe_allow_html=True)
    st.info("După ce se deschide, apasă F11 în noul tab pentru Full Screen pe proiector.")

# --- SECȚIUNEA MEMORIE ---
st.write("---")
st.subheader("📁 Istoric fișiere/evenimente")
# Această listă va fi reținută chiar dacă restartezi aplicația [cite: 2026-01-15]
if state["history"]:
    for event in state["history"]:
        st.write(f"✅ {event}")
else:
    st.write("Niciun eveniment memorat momentan.")

# Buton de urgență pentru oprire
if st.button("Oprește tot și șterge memoria"):
    save_state({"party_active": False, "history": []}) [cite: 2026-01-15]
    st.rerun()
    