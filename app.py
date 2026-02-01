import streamlit as st
from PIL import Image
import numpy as np
import random, urllib.parse, time

# Optional: DeepFace pentru analiză emoție facială
try:
    from deepface import DeepFace
    AI_READY = True
except ImportError:
    AI_READY = False

st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

# ===================== STYLE =====================
st.markdown("""
<style>
body { background:#0e1117; color:white; }
.card { background:#161b22; padding:20px; border-radius:18px; box-shadow:0 0 25px #000; margin-bottom:20px; }
.title { font-size:34px; font-weight:900; }
.subtitle { font-size:18px; color:#aaa; }
.emotion { font-size:28px; font-weight:800; color:#00ffcc; }
.song { font-size:22px; font-weight:700; color:#ff4b4b; }
.btn { display:block; padding:14px; border-radius:30px; text-align:center; font-weight:700; text-decoration:none; margin-top:12px; }
.btn-yt { background:#ff0000; color:white; }
.btn-sp { background:#1db954; color:white; }
.btn-fe { background:#5a5a5a; color:white; }
.timer { font-size:28px; font-weight:900; color:#ff4b4b; border:3px solid #ff4b4b; border-radius:15px; padding:12px; text-align:center; }
</style>
""", unsafe_allow_html=True)

# ===================== STATE =====================
if "last_scan" not in st.session_state:
    st.session_state.last_scan = 0
if "current_song" not in st.session_state:
    st.session_state.current_song = None

SCAN_INTERVAL = 120  # secunde pentru auto-scan

# ===================== MUSIC DB =====================
# Organizare: culori dominante / vestimentație → subcategorie muzicală
MUSIC_DB = {
    "red": ["AC/DC - Highway to Hell", "Metallica - Enter Sandman"],
    "blue": ["Adele - Someone Like You", "Sam Smith - Stay With Me"],
    "green": ["Pharrell Williams - Happy", "Bruno Mars - Uptown Funk"],
    "yellow": ["LMFAO - Party Rock Anthem", "Shakira - Waka Waka"],
    "neutral": ["Abba - Dancing Queen", "The Weeknd - Blinding Lights"]
}

# ===================== FUNCTIONS =====================
def dominant_color(img: Image.Image):
    """Returnează culoarea dominantă ca text simplu: red/blue/green/yellow/neutral"""
    small = img.resize((50,50))
    arr = np.array(small)
    avg = arr.mean(axis=(0,1))
    r,g,b = avg
    if r>150 and g<100 and b<100: return "red"
    if b>150 and r<100 and g<100: return "blue"
    if g>150 and r<100 and b<100: return "green"
    if r>150 and g>150 and b<100: return "yellow"
    return "neutral"

def face_emotion(img: Image.Image):
    """Returnează emoție dominantă folosind DeepFace sau random dacă nu e disponibil"""
    if not AI_READY:
        return "neutral"
    try:
        res = DeepFace.analyze(np.array(img), actions=["emotion"], enforce_detection=False)
        return res[0]["dominant_emotion"].lower()
    except:
        return "neutral"

def pick_song(img: Image.Image):
    """Alege piesa pe baza de culoare + 20% fata (emoție)"""
    color = dominant_color(img)
    face = face_emotion(img)

    # Scor ponderat 80% culoare + 20% fata
    pool = MUSIC_DB.get(color, MUSIC_DB["neutral"])
    if face in ["happy","neutral"]:
        pool += MUSIC_DB.get("green", [])
    elif face in ["sad","angry"]:
        pool += MUSIC_DB.get("blue", [])
    # Alegem random din pool
    return random.choice(pool)

# ===================== HEADER =====================
st.markdown('<div class="title">🎧 HERCULE AI — DJ ENGINE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Color + Face → Song Recommendation</div>', unsafe_allow_html=True)
st.divider()

# ===================== LAYOUT =====================
col1, col2, col3 = st.columns([1.2,1.4,1])

# ===================== LEFT — CAMERA =====================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    remaining = max(0, SCAN_INTERVAL - int(time.time() - st.session_state.last_scan))
    st.markdown(f'<div class="timer">⏱️ AUTO SCAN: {remaining:02d}s</div>', unsafe_allow_html=True)

    cam = st.camera_input("📸 Capture from camera")
    up = st.file_uploader("📁 Upload image", type=["jpg","jpeg","png"])
    source = cam if cam else up

    if source:
        img = Image.open(source).convert("RGB")
        st.image(img, caption="Input image", use_container_width=True)
        song = pick_song(img)
        st.session_state.current_song = song
        st.session_state.last_scan = time.time()

    st.markdown('</div>', unsafe_allow_html=True)

# ===================== CENTER — RESULT =====================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.session_state.current_song:
        st.markdown(f'🎵 Selected Song:<div class="song">{st.session_state.current_song}</div>', unsafe_allow_html=True)
    else:
        st.info("Waiting for scan...")
    st.markdown('</div>', unsafe_allow_html=True)

# ===================== RIGHT — PLAYERS =====================
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    if st.session_state.current_song:
        q = urllib.parse.quote(st.session_state.current_song)
        yt = f"https://www.youtube.com/results?search_query={q}"
        sp = f"https://open.spotify.com/search/{q}"
        fe = f"https://www.festify.us/search?q={q}"
        st.markdown(f'''
        <a class="btn btn-yt" href="{yt}" target="_blank">▶ Play on YouTube</a>
        <a class="btn btn-sp" href="{sp}" target="_blank">🎧 Play on Spotify</a>
        <a class="btn btn-fe" href="{fe}" target="_blank">🎉 Add to Festify Party</a>
        ''', unsafe_allow_html=True)
    else:
        st.info("No track yet")
    st.markdown('</div>', unsafe_allow_html=True)
