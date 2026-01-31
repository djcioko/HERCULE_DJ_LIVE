import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

# Conectare Spotify
auth_manager = SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
    scope="user-modify-playback-state user-read-currently-playing playlist-modify-public"
)
sp = spotipy.Spotify(auth_manager=auth_manager)
PLAYLIST_ID = st.secrets["PLAYLIST_ID"]

st.title("🎧 HERCULE AI DJ - AUTO MODE")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📸 Flux Cameră")
    # Camera input
    img_file = st.camera_input("Fă o poză mulțimii!")

    if img_file:
        st.warning("🤖 Analizăm imaginea...")
        
        # LOGICA DE CĂUTARE REPARATĂ
        vibe_tags = ["Party Remix 2026", "Techno Vibe", "Club Dance House"]
        query = random.choice(vibe_tags)
        
        # Căutăm piesa
        search_res = sp.search(q=query, type='track', limit=5)
        
        if search_res['tracks']['items']:
            # Luăm o piesă random din primele 5 găsite pentru varietate
            track = random.choice(search_res['tracks']['items'])
            track_uri = track['uri']
            track_name = track['name']
            artist = track['artists'][0]['name']

            # ADAUGĂM ÎN PLAYLIST
            try:
                sp.playlist_add_items(PLAYLIST_ID, [track_uri])
                st.success(f"✅ Găsit & Adăugat: {track_name} - {artist}")
                
                # Pornește automat piesa nouă
                sp.start_playback(context_uri=f"spotify:playlist:{PLAYLIST_ID}")
                
                # Buton pentru a reveni la camera live
                if st.button("🔄 REVENIRE LA CAMERA LIVE"):
                    st.rerun() # Această comandă forțează aplicația să repornească camera
            except Exception as e:
                st.error(f"Eroare la adăugare: {e}")
        else:
            st.error("AI-ul nu a găsit nicio melodie potrivită. Încearcă iar!")

with col2:
    st.subheader("🎮 Panou Control")
    if st.button("▶️ PLAY"):
        sp.start_playback(context_uri=f"spotify:playlist:{PLAYLIST_ID}")
    
    if st.button("⏸️ PAUZĂ"):
        sp.pause_playback()
    
    st.write("---")
    # Afișăm ultimele piese din playlist ca să vezi că funcționează
    st.write("🎵 **Ultimele adăugate în HERCULE VIBE:**")
    tracks = sp.playlist_items(PLAYLIST_ID, limit=3)
    for item in tracks['items']:
        st.write(f"- {item['track']['name']}")
