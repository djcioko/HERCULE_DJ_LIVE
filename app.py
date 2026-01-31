import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

# Permisiuni extinse pentru control și scriere
scope = "user-modify-playback-state user-read-currently-playing playlist-modify-public playlist-read-private"

auth_manager = SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
    scope=scope
)
sp = spotipy.Spotify(auth_manager=auth_manager)

# Preluăm ID-ul playlist-ului din Secrets
PLAYLIST_ID = st.secrets["PLAYLIST_ID"]

# Încercăm să luăm numele playlist-ului ca să-l afișăm
try:
    playlist_info = sp.playlist(PLAYLIST_ID)
    playlist_name = playlist_info['name']
except:
    playlist_name = "HERCULE AI DJ VIBE"

st.title(f"🎧 {playlist_name} - SMART MODE")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📸 Analiză Vibe")
    img_file = st.camera_input("Fă o poză pentru a adăuga muzică!")
    
    if img_file:
        st.warning("🤖 AI analizează chipul și vibe-ul...")
        # Simulare analiză: alege un stil
        vibe_list = ["Energy", "Dance", "Techno", "Club"]
        chosen = random.choice(vibe_list)
        
        # Căutăm și adăugăm piesa
        results = sp.search(q=chosen, type='track', limit=1)
        if results['tracks']['items']:
            track_uri = results['tracks']['items'][0]['uri']
            track_name = results['tracks']['items'][0]['name']
            
            # ADAUGĂ ÎN PLAYLIST
            sp.playlist_add_items(PLAYLIST_ID, [track_uri])
            st.success(f"✅ AI-ul a simțit vibe-ul '{chosen}' și a adăugat: {track_name}")

with col2:
    st.subheader("🎮 Control Muzică")
    
    if st.button("▶️ PORNEȘTE PLAYLIST"):
        try:
            sp.start_playback(context_uri=f"spotify:playlist:{PLAYLIST_ID}")
            st.write("Muzica a pornit!")
        except:
            st.error("Deschide Spotify pe telefon/PC!")

    if st.button("⏸️ PAUZĂ"):
        try:
            sp.pause_playback()
        except:
            pass

    st.write("---")
    st.markdown(f"**Playlist activ:** {playlist_name}")
    st.info("Fiecare poză adaugă o piesă nouă în lista de mai sus! [cite: 2026-01-31]")
