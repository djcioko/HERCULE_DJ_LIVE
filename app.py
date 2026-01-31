import streamlit as st
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import random

# 1. Setări de bază
st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

# 2. Conectare la Spotify cu permisiuni de scriere
try:
    auth_manager = SpotifyOAuth(
        client_id=st.secrets["SPOTIPY_CLIENT_ID"],
        client_secret=st.secrets["SPOTIPY_CLIENT_SECRET"],
        redirect_uri=st.secrets["SPOTIPY_REDIRECT_URI"],
        scope="user-modify-playback-state user-read-currently-playing playlist-modify-public"
    )
    sp = spotipy.Spotify(auth_manager=auth_manager)
    
    # Preluăm ID-ul playlist-ului din Secrets
    PLAYLIST_ID = st.secrets["PLAYLIST_ID"]
    playlist_info = sp.playlist(PLAYLIST_ID)
    p_name = playlist_info['name']
except Exception as e:
    st.error("Eroare la conectare! Verifică SECRETS în Streamlit.")
    st.stop()

st.title(f"🎧 {p_name} - SMART MODE")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📸 Analiză Vibe Live")
    img_file = st.camera_input("Zâmbește pentru a adăuga muzică!")
    
    if img_file:
        st.info("🤖 AI DJ analizează poza...")
        vibe_tags = ["Party Remix", "Dance Hits", "Energy House"]
        search_query = random.choice(vibe_tags)
        
        try:
            # Căutăm o piesă și o adăugăm în playlist
            results = sp.search(q=search_query, type='track', limit=1)
            if results['tracks']['items']:
                track = results['tracks']['items'][0]
                sp.playlist_add_items(PLAYLIST_ID, [track['uri']])
                st.success(f"✅ Adăugat automat: {track['name']}")
                # Pornește automat playlist-ul să se audă piesa
                sp.start_playback(context_uri=f"spotify:playlist:{PLAYLIST_ID}")
        except:
            st.error("Nu am putut adăuga piesa. Verifică Spotify pe telefon!")

with col2:
    st.subheader("🎮 Control Muzică")
    
    if st.button("▶️ START PLAYLIST"):
        try:
            sp.start_playback(context_uri=f"spotify:playlist:{PLAYLIST_ID}")
            st.write("Muzica pornește!")
        except:
            st.warning("Deschide Spotify pe un dispozitiv!")

    if st.button("⏸️ PAUZĂ"):
        try:
            sp.pause_playback()
            st.write("Pauză.")
        except:
            pass

    st.write("---")
    st.write(f"**Playlist activ:** {p_name}")
    st.markdown('<a href="https://p2p.mirotalk.com/join/hercule-dj-party" target="_blank"><button style="width:100%; height:40px; background-color:#1DB954; color:white; border:none; border-radius:5px; cursor:pointer;">PROIECTOR FULL SCREEN</button></a>', unsafe_allow_html=True)
