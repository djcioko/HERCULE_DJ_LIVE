import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Configurare bază
st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

# Verificăm dacă Secrets sunt încărcate corect
if "SPOTIPY_CLIENT_ID" not in st.secrets:
    st.error("Lipsesc setările din Secrets! Te rog să le adaugi în panoul Streamlit.")
    st.stop()

# Conectare Spotify
try:
    auth_manager = SpotifyOAuth(
        client_id=st.secrets["SPOTIPY_CLIENT_ID"],
        client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
        redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
        scope="user-modify-playback-state user-read-currently-playing playlist-modify-public"
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    p_id = st.secrets["PLAYLIST_ID"]
except Exception as e:
    st.error(f"Eroare de configurare: {e}")
    st.stop()

st.title("🎧 HERCULE AI DJ - LIVE VIBE")

# Interfața
col1, col2 = st.columns([2, 1])

with col1:
    img = st.camera_input("📸 Fă o poză să adaugi muzică!")
    if img:
        st.info("Analizăm vibe-ul... 🤖")
        # Căutăm o piesă random de party
        res = sp.search(q="Party Mix 2026", type='track', limit=10)
        track = random.choice(res['tracks']['items'])
        # Adăugăm în playlist
        sp.playlist_add_items(p_id, [track['uri']])
        st.success(f"✅ Adăugat în playlist: {track['name']}")

with col2:
    if st.button("▶️ START MUZICA"):
        try:
            sp.start_playback(context_uri=f"spotify:playlist:{p_id}")
            st.write("Vibe-ul a pornit!")
        except:
            st.warning("Deschide Spotify pe telefon!")
            
    if st.button("⏸️ PAUZA"):
        try: sp.pause_playback()
        except: pass

st.write("---")
st.markdown('<a href="https://p2p.mirotalk.com/join/hercule-dj-party" target="_blank"><button style="width:100%; height:50px; background-color:#1DB954; color:white; border:none; border-radius:5px; cursor:pointer;">DESCHIDE PROIECTOR</button></a>', unsafe_allow_html=True)
