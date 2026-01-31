import streamlit as st

# Configurare interfață
st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

st.title("🎧 HERCULE AI DJ - LIVE CONTROL")

# Structura pe coloane
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📺 Flux Video Live")
    # Activează camera web direct în aplicație
    st.camera_input("Zâmbește pentru AI DJ!")

with col2:
    st.subheader("🎵 Control Party")
    if st.button("🚀 ACTIVEAZĂ AI DJ MODE"):
        st.success("AI-ul analizează vibe-ul publicului...")
    
    st.write("---")
    st.info("Apasă butonul de mai jos pentru proiector (Full Screen):")
    
    # Buton pentru Mirotalk (fără erori de sintaxă)
    st.markdown("""
        <a href="https://p2p.mirotalk.com/join/hercule-dj-party" target="_blank">
            <button style="width:100%; height:50px; background-color:#1DB954; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">
                DESCHIDE PROIECTOR (MIROTALK)
            </button>
        </a>
    """, unsafe_allow_html=True)
