import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# Configurare Pagină
st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

# Permisiuni pentru a citi, scrie în playlist și controla muzica
scope = "user-modify-playback-state user-read-currently-playing playlist-modify-public"

auth_manager = SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
    scope=scope
)
sp = spotipy.Spotify(auth_manager=auth_manager)

st.title("🎧 HERCULE AI DJ - AUTO VIBE MODE")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📸 Analiză Mulțime")
    img_file = st.camera_input("Zâmbește pentru a adăuga muzică!")

with col2:
    st.subheader("🎵 Status Playlist")
    if img_file:
        st.info("Analizăm vibe-ul... 🤖")
        
        # Logica AI: Alege un stil muzical random
        vibe_keywords = ["Party Hits", "Techno Vibe", "Dance 2026", "Club Remix"]
        chosen_vibe = random.choice(vibe_keywords)
        
        try:
            # 1. Căutăm o piesă nouă
            results = sp.search(q=chosen_vibe, type='track', limit=10)
            track = random.choice(results['tracks']['items'])
            track_uri = track['uri']
            
            # 2. ADAUGĂ AUTOMAT în playlist-ul HERCULE AI DJ VIBE
            p_id = st.secrets["PLAYLIST_ID"]
            sp.playlist_add_items(p_id, [track_uri])
            
            st.success(f"✅ Vibe '{chosen_vibe}' detectat!")
            st.write(f"🆕 Adăugat: **{track['name']}**")
            
            # 3. Pornește muzica
            sp.start_playback(context_uri=f"spotify:playlist:{p_id}")
            
        except Exception as e:
            st.error("Deschide Spotify pe telefon mai întâi!")

    st.write("---")
    st.markdown('<a href="https://p2p.mirotalk.com/join/hercule-dj-party" target="_blank"><button style="width:100%; height:50px; background-color:#1DB954; color:white; border:none; border-radius:5px; cursor:pointer; font-weight:bold;">DESCHIDE PROIECTOR</button></a>', unsafe_allow_html=True)
