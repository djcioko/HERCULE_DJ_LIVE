import streamlit as st
import time, random, urllib.parse
import numpy as np
from PIL import Image
from deepface import DeepFace
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# ================= CONFIG =================
st.set_page_config("HERCULE AI DJ - SMART VIBE", layout="wide")

# ================= STYLE =================
st.markdown("""
<style>
.main { background:#0e1117; color:white; }
iframe { border-radius:20px; border:4px solid #1ed760; box-shadow: 0px 0px 20px #1ed760; }
.btn a {
 display:block; padding:12px; border-radius:25px;
 text-align:center; font-weight:bold; color:white;
 text-decoration:none; margin-bottom:10px;
}
.spotify { background:#1DB954; }
.festify { background:#f25c05; }
</style>
""", unsafe_allow_html=True)

# ================= SPOTIFY AUTH (Opțional) =================
# Dacă vrei adăugare automată, vei completa aceste date mâine
SPOTIFY_CLIENT_ID = "YOUR_ID"
SPOTIFY_CLIENT_SECRET = "YOUR_SECRET"
REDIRECT_URI = "http://localhost:8501"

sp = None # Dezactivat până la configurare

# ================= SESSION =================
if "last_time" not in st.session_state: st.session_state.last_time = time.time()
if "song" not in st.session_state: st.session_state.song = ""
if "query" not in st.session_state: st.session_state.query = ""

# ================= MUSIC DB (Lista ta de 100 integrată pe vibe-uri) =================
MUSIC = {
    "happy": ["Bruno Mars - Marry You", "Pharrell Williams - Happy", "Shakira - Waka Waka", "Andra - Iubirea Schimba Tot", "O-Zone - Dragostea Din Tei", "Voltaj - 20 de ani"],
    "angry": ["AC/DC - Thunderstruck", "AC/DC - Highway to Hell", "Metallica - Enter Sandman", "B.U.G. Mafia - Sa Cante Trompetele", "Eminem - Lose Yourself"],
    "sad": ["Adele - Someone Like You", "Cargo - Daca ploaia s-ar opri", "Holograf - Sa nu-mi iei niciodata dragostea", "Iris - De vei pleca"],
    "neutral": ["Daft Punk - Get Lucky", "ABBA - Dancing Queen", "Dan Spataru - Drumurile noastre", "Smiley - Oarecare", "Loredana - Zig Zagga", "3 Sud Est - Amintirile"],
    "surprise": ["The Weeknd - Blinding Lights", "Calvin Harris - Summer", "Zdob si Zdup - Moldoveni s-au nascut"]
}

FASHION_MAP = {"dark": "angry", "bright": "happy", "neutral": "neutral"}

# ================= AI LOGIC =================
def detect_emotion(img):
    try:
        res = DeepFace.analyze(np.array(img), actions=["emotion"], enforce_detection=False)
        return res[0]["dominant_emotion"]
    except: return "neutral"

def detect_fashion(img):
    avg = np.mean(np.array(img))
    if avg < 85: return "dark"
    if avg > 170: return "bright"
    return "neutral"

def choose_song(emotion, fashion):
    vibe = FASHION_MAP.get(fashion, emotion)
    piese_disponibile = MUSIC.get(vibe, MUSIC["neutral"])
    return random.choice(piese_disponibile)

# ================= TIMER LOGIC (120s) =================
elapsed = time.time() - st.session_state.last_time
timp_ramas = max(0, 120 - int(elapsed))

if timp_ramas <= 0:
    st.session_state.last_time = time.time()
    all_songs = sum(MUSIC.values(), [])
    piesa_noua = random.choice(all_songs)
    st.session_state.song = piesa_noua
    st.session_state.query = urllib.parse.quote(piesa_noua)
    st.rerun()

# ================= UI =================
st.title("🎧 HERCULE AI – SMART DJ")

c1, c2 = st.columns(2)

with c1:
    st.subheader("📸 Senzor Vizual & Fashion")
    st.progress(min(elapsed / 120, 1.0), text=f"Timp până la auto-schimbare: {timp_ramas}s")

    cam = st.camera_input("Poză live")
    up = st.file_uploader("Upload poză", type=["jpg","png","jpeg"])
    src = cam or up

    if src:
        img = Image.open(src).convert("RGB")
        st.image(img, width=350)

        emotion = detect_emotion(img)
        fashion = detect_fashion(img)
        song = choose_song(emotion, fashion)

        st.session_state.song = song
        st.session_state.query = urllib.parse.quote(song)
        st.session_state.last_time = time.time()

        st.markdown(f"### 🎭 Emoție: **{emotion}** | 👕 Fashion: **{fashion}**")
        st.markdown(f"### 🎵 Melodie: **{song}**")

        st.markdown(f"""
        <div class="btn spotify"><a href="https://open.spotify.com/search/{st.session_state.query}" target="_blank">🟢 CAUTĂ PE SPOTIFY</a></div>
        <div class="btn festify"><a href="https://festify.us/party/-OMkDNoyn7nohBDBnLWm" target="_blank">🔥 DESCHIDE FESTIFY</a></div>
        """, unsafe_allow_html=True)

with c2:
    st.subheader("📺 YouTube Player (Stabilitate Maximă)")
    if st.session_state.query:
        # Folosim metoda listType=search pentru stabilitate 100%
        yt = f"https://www.youtube.com/embed?listType=search&list={st.session_state.query}&autoplay=1"
        st.markdown(f'<iframe width="100%" height="400" src="{yt}" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)
        st.success(f"Rulează: {st.session_state.song}")

st.info("Sistemul detectează automat vibe-ul și schimbă muzica la 2 minute!")
