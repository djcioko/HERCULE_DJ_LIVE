import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

# 1. Autentificare cu permisiuni de scriere (Playlist Modify)
auth_manager = SpotifyOAuth(
    client_id=st.secrets["SPOTIPY_CLIENT_ID"],
    client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
    redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
    scope="user-modify-playback-state user-read-currently-playing playlist-modify-public"
)
sp = spotipy.Spotify(auth_manager=auth_manager)
PLAYLIST_ID = st.secrets["PLAYLIST_ID"]

st.title("🎧 HERCULE AI DJ - AUTO-ANALYZER")

col1, col2 = st.columns([2, 1])

with col1:
    img_file = st.camera_input("📸 Fă poza pentru analiză automată")

    # Aici se întâmplă magia: dacă img_file nu e None, execută imediat
    if img_file is not None:
        st.info("🤖 AI DJ: Analizez chipurile și vibe-ul mulțimii...")
        
        # Generăm un cuvânt cheie bazat pe "analiză" (simulată)
        vibe_options = ["High Energy Party", "Electronic Dance", "Club Hits 2026", "Top Viral Party"]
        chosen_vibe = random.choice(vibe_options)
        
        # CĂUTARE AUTOMATĂ
        results = sp.search(q=chosen_vibe, type='track', limit=10)
        tracks = results['tracks']['items']
        
        if tracks:
            new_track = random.choice(tracks) # Alegem una din cele 10 găsite
            
            # ADĂUGARE AUTOMATĂ ÎN PLAYLIST
            try:
                sp.playlist_add_items(PLAYLIST_ID, [new_track['uri']])
                st.success(f"✅ ANALIZĂ COMPLETĂ! Am adăugat: **{new_track['name']}**")
                
                # Forțăm Spotify să cânte noul playlist actualizat
                sp.start_playback(context_uri=f"spotify:playlist:{PLAYLIST_ID}")
            except Exception as e:
                st.error("Eroare la adăugare. Verifică dacă playlist-ul e public!")
        else:
            st.error("Nu am găsit melodii pentru acest vibe. Încearcă o altă poză!")

with col2:
    st.subheader("🎮 Control Live")
    if st.button("🔄 RESET CAMERĂ (LIVE)"):
        st.rerun() # Te scoate din poza făcută și te întoarce la video live
        
    if st.button("⏸️ PAUZĂ"):
        sp.pause_playback()
    
    st.write("---")
    st.write("🎵 **Recent adăugate de AI:**")
    # Afișăm ultimele piese din playlist
    recent = sp.playlist_items(PLAYLIST_ID, limit=5)
    for item in recent['items']:
        st.write(f"· {item['track']['name']}")
