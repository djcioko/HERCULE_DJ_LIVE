import streamlit as st
import time, random, urllib.parse
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

# Încercăm importul AI-ului (DeepFace)
try:
    from deepface import DeepFace
    AI_READY = True
except ImportError:
    AI_READY = False

# ================= CONFIGURARE & DESIGN =================
st.set_page_config(page_title="HERCULE AI - THE BEAST DJ", layout="wide")

st.markdown("""
<style>
    .main { background:#0e1117; color:white; }
    iframe { border-radius:20px; border:4px solid #1ed760; box-shadow: 0px 0px 25px #1ed760; }
    .timer-box { font-size: 40px; font-weight: bold; color: #ff4b4b; text-align: center; border: 2px solid #ff4b4b; border-radius: 15px; padding: 10px; margin-bottom: 20px; }
    .btn-spotify { background-color: #1DB954; color: white; padding: 15px; border-radius: 30px; text-align: center; font-weight: bold; display: block; text-decoration: none; margin-bottom: 10px; font-size: 18px; }
    .btn-festify { background-color: #f25c05; color: white; padding: 15px; border-radius: 30px; text-align: center; font-weight: bold; display: block; text-decoration: none; font-size: 18px; }
</style>
""", unsafe_allow_html=True)

# ================= MEMORIE SESIUNE =================
if "last_time" not in st.session_state: st.session_state.last_time = time.time()
if "song" not in st.session_state: st.session_state.song = ""
if "query" not in st.session_state: st.session_state.query = ""
if "emotion" not in st.session_state: st.session_state.emotion = "Neutral"

# ================= BAZA DE DATE (exemplu scurt) =================
MUSIC_DB = {
    "happy": [
        "Bruno Mars - Marry You", "Pharrell Williams - Happy", "Daft Punk - Get Lucky", "Village People - Y.M.C.A."
    ],
    "neutral": [
        "Abba - Dancing Queen", "The Weeknd - Blinding Lights", "Dua Lipa - Levitating"
    ],
    "sad": [
        "Adele - Someone Like You", "Holograf - Sa nu-mi iei niciodata dragostea"
    ],
    "angry": [
        "AC/DC - Thunderstruck", "Metallica - Enter Sandman"
    ]
}

# ================= LOGICA AI =================
def get_vibe(img):
    if not AI_READY: return "neutral"
    try:
        res = DeepFace.analyze(np.array(img), actions=["emotion"], enforce_detection=False)
        return res[0]["dominant_emotion"]
    except:
        return "neutral"

# ================= TIMER & AUTO-CAPTURE =================
now = time.time()
elapsed = now - st.session_state.last_time
timp_ramas = max(0, 120 - int(elapsed))

if timp_ramas <= 0:
    components.html(
        """<script>window.parent.document.querySelectorAll('button[aria-label="Take Photo"]').forEach(btn => btn.click());</script>""",
        height=0
    )
    st.session_state.last_time = time.time()  # Reset timer

# ================= INTERFAȚA =================
st.title("🎰 HERCULE AI - THE ULTIMATE DJ ENGINE")

col1, col2 = st.columns([1, 1.2])

with col1:
    st.markdown(f'<div class="timer-box">⏱️ AUTO-SCAN: {timp_ramas:02d}s</div>', unsafe_allow_html=True)
    
    cam = st.camera_input("📸 AI EYE ACTIVATED")
    up = st.file_uploader("📁 SAU ÎNCARCĂ POZĂ", type=["jpg", "png", "jpeg"])
    
    source = cam or up

    if source:
        img = Image.open(source).convert("RGB")
        st.image(img, width=400)
        
        # Procesare AI
        emotion = get_vibe(img)
        st.session_state.emotion = emotion
        
        # Alegem piesa din categoria detectată
        vibe_category = emotion if emotion in MUSIC_DB el
