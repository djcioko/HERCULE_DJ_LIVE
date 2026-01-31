import streamlit as st
importspotipy
from spotipy.oauth2 import SpotifyOAuth

# Configurare Pagina
st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

# Conectare la Spotify folosind SECRETS setate de tine
auth_manager = SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
    scope="user-modify-playback-state user-read-currently-playing"
)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🎧 HERCULE AI DJ - SPOTIFY MODE")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📺 Flux Video Live")
    st.camera_input("Zâmbește pentru AI DJ!")

with col2:
    st.subheader("🎵 Control Muzică")
    
    # Buton Play
    if st.button("▶️ PORNEȘTE MUZICA"):
        try:
            sp.start_playback()
            st.success("Vibe-ul a început!")
        except:
            st.error("Deschide Spotify pe telefon/PC mai întâi!")

    # Buton Pause
    if st.button("⏸️ PAUZĂ"):
        try:
            sp.pause_playback()
            st.warning("Muzica s-a oprit.")
        except:
            st.info("Nu rulează nicio piesă acum.")
    
    st.write("---")
    st.markdown('<a href="https://p2p.mirotalk.com/join/hercule-dj-party" target="_blank"><button style="width:100%; height:50px; background-color:#1DB954; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">DESCHIDE PROIECTOR</button></a>', unsafe_allow_html=True)
