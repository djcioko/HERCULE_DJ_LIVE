import streamlit as st
import time, random, urllib.parse
import numpy as np
from PIL import Image

# Încercăm să importăm DeepFace, dacă nu e instalat, dăm un mesaj prietenos
try:
    from deepface import DeepFace
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# ================= CONFIG =================
st.set_page_config(page_title="HERCULE AI DJ - SMART", layout="wide")

st.markdown("""
<style>
.main { background:#0e1117; color:white; }
iframe { border-radius:20px; border:4px solid #1ed760; box-shadow: 0px 0px 20px #1ed760; }
.btn-spotify { background-color: #1DB954; color: white; padding: 12px; border-radius: 25px; text-align: center; font-weight: bold; display: block; text-decoration: none; margin-bottom: 10px; }
.btn-festify { background-color: #f25c05; color: white; padding: 12px; border-radius: 25px; text-align: center; font-weight: bold; display: block; text-decoration: none; }
</style>
""", unsafe_allow_html=True)

# ================= SESSION =================
if "last_time" not in st.session_state: st.session_state.last_time = time.time()
if "song" not in st.session_state: st.session_state.song = ""
if "query" not in st.session_state: st.session_state.query = ""

# ================= MUSIC DB (100+ piese pe categorii) =================
MUSIC = {
    "happy": ["Bruno Mars - Uptown Funk", "Pharrell Williams - Happy", "O-Zone - Dragostea Din Tei", "Andra - Iubirea Schimba Tot"],
    "angry": ["AC/DC - Thunderstruck", "Eminem - Lose Yourself", "Metallica - Enter Sandman", "B.U.G. Mafia - Cine e cu noi"],
    "sad": ["Adele - Someone Like You", "Cargo - Daca ploaia s-ar opri", "Holograf - Sa nu-mi iei niciodata dragostea"],
    "neutral": ["Daft Punk - Get Lucky", "ABBA - Dancing Queen", "Dan Spataru - Drumurile noastre", "Smiley - Oarecare"],
    "surprise": ["The Weeknd - Blinding Lights", "Zdob si Zdup - Moldoveni s-au nascut"]
}

# ================= LOGICA AI =================
def analyze_vibe(img):
    if not AI_AVAILABLE:
        return "neutral", "neutral" # Fallback dacă lipsește DeepFace
    try:
        res = DeepFace.analyze(np.array(img), actions=["emotion"], enforce_detection=False)
        emotion = res[0]["dominant_emotion"]
        # Detectăm haine (fashion) după luminozitate medie
        avg = np.mean(np.array(img))
        fashion = "dark" if avg < 85 else "bright" if avg > 170 else "neutral"
        return emotion, fashion
    except:
        return "neutral", "neutral"

# ================= TIMER (120s) =================
elapsed = time.time() - st.session_state.last_time
timp_ramas = max(0, 120 - int(elapsed))

if timp_ramas <= 0:
    st.session_state.last_time = time.time()
    piesa_auto = random.choice(sum(MUSIC.values(), []))
    st.session_state.song = piesa_auto
    st.session_state.query = urllib.parse.quote(piesa_auto)
    st.rerun()

# ================= UI =================
st.title("🎧 HERCULE AI – DJ Engine")

if not AI_AVAILABLE:
    st.warning("⚠️ DeepFace nu este instalat. Rulez pe modul Manual/Timer. Instalează 'deepface' pentru a activa recunoașterea feței.")

c1, c2 = st.columns(2)

with c1:
    st.subheader("📸 Senzor Vizual")
    st.progress(min(elapsed / 120, 1.0), text=f"Timp până la schimbare: {timp_ramas}s")

    cam = st.camera_input("Fă o poză")
    up = st.file_uploader("Upload", type=["jpg","png","jpeg"])
    src = cam or up

    if src:
        img = Image.open(src).convert("RGB")
        emotion, fashion = analyze_vibe(img)
        song = random.choice(MUSIC.get(emotion, MUSIC["neutral"]))
        
        st.session_state.song = song
        st.session_state.query = urllib.parse.quote(song)
        st.session_state.last_time = time.time()
        
        st.image(img, width=300)
        st.markdown(f"### 🎭 Vibe: **{emotion}** | 👕 Fashion: **{fashion}**")
        st.markdown(f"### 🎵 Melodie: **{song}**")

        # Butoane externe
        st.markdown(f"""
            <a href="https://open.spotify.com/search/{st.session_state.query}" target="_blank" class="btn-spotify">🟢 CAUTĂ PE SPOTIFY</a>
            <a href="https://festify.us/party/-OMkDNoyn7nohBDBnLWm" target="_blank" class="btn-festify">🔥 ADAUGĂ ÎN FESTIFY</a>
        """, unsafe_allow_html=True)

with c2:
    st.subheader("📺 YouTube Player")
    if st.session_state.query:
        yt = f"https://www.youtube.com/embed?listType=search&list={st.session_state.query}&autoplay=1"
        st.markdown(f'<iframe width="100%" height="400" src="{yt}" allow="autoplay; encrypted-media" allowfullscreen></iframe>', unsafe_allow_html=True)
        st.success(f"Rulează: {st.session_state.song}")
