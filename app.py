import streamlit as st
import time, random, urllib.parse
import numpy as np
from PIL import Image
import streamlit.components.v1 as components

# ================= AI OPTIONAL =================
try:
    from deepface import DeepFace
    AI_READY = True
except:
    AI_READY = False

# ================= CONFIG =================
st.set_page_config(page_title="HERCULE AI - THE BEAST DJ", layout="wide")

st.markdown("""
<style>
.main { background:#0e1117; color:white; }
iframe { border-radius:20px; border:4px solid #1ed760; box-shadow: 0 0 25px #1ed760; }
.timer-box {
  font-size: 38px; font-weight: 900; color: #ff4b4b;
  text-align: center; border: 3px solid #ff4b4b;
  border-radius: 15px; padding: 12px; margin-bottom: 20px;
}
.btn-spotify {
  background:#1DB954; color:white; padding:14px;
  border-radius:30px; text-align:center;
  font-weight:bold; display:block;
  text-decoration:none; margin-bottom:10px;
}
.btn-festify {
  background:#f25c05; color:white; padding:14px;
  border-radius:30px; text-align:center;
  font-weight:bold; display:block;
}
</style>
""", unsafe_allow_html=True)

# ================= STATE =================
if "last_scan" not in st.session_state:
    st.session_state.last_scan = 0

if "song" not in st.session_state:
    st.session_state.song = ""

if "query" not in st.session_state:
    st.session_state.query = ""

if "emotion" not in st.session_state:
    st.session_state.emotion = "neutral"

if "img_hash" not in st.session_state:
    st.session_state.img_hash = None

SCAN_INTERVAL = 120  # secunde

# ================= MUSIC DB =================
MUSIC_DB = {
    "happy": [
        "Bruno Mars - Marry You", "Pharrell Williams - Happy", "Daft Punk - Get Lucky",
        "Village People - Y.M.C.A.", "Taylor Swift - Shake It Off", "Michel Telo - Ai se eu te pego",
        "Shakira - Waka Waka", "LMFAO - Party Rock Anthem", "Andra - Iubirea Schimba Tot",
        "O-Zone - Dragostea Din Tei", "Connect-R - Vara nu dorm", "Smiley - Oarecare",
        "Loredana - Zig Zagga", "HI-Q - Gasca mea", "3 Sud Est - Amintirile",
        "N&D - Vino la mine", "Alex Velea - Minim doi"
    ],
    "angry": [
        "AC/DC - Thunderstruck", "AC/DC - Highway to Hell", "Metallica - Enter Sandman",
        "Metallica - Nothing Else Matters", "Eminem - Lose Yourself",
        "B.U.G. Mafia - Sa Cante Trompetele", "B.U.G. Mafia - Cine e cu noi",
        "Parazitii - In focuri", "Guns N' Roses - Sweet Child O' Mine",
        "Nirvana - Smells Like Teen Spirit", "Rage Against The Machine - Killing In The Name"
    ],
    "sad": [
        "Adele - Someone Like You", "Cargo - Daca ploaia s-ar opri",
        "Iris - De vei pleca", "Holograf - Sa nu-mi iei niciodata dragostea",
        "Sam Smith - Stay With Me", "Billie Eilish - Lovely",
        "Ducu Bertzi - M-am indragostit numai de ea"
    ],
    "neutral": [
        "Dan Spataru - Drumurile noastre", "Mirabela Dauer - Ioane, Ioane",
        "Gica Petrescu - I-a mai toarna un paharel", "Abba - Dancing Queen",
        "Boney M - Rasputin", "Zdob si Zdup - Moldoveni s-au nascut",
        "Phoenix - Andrii Popa", "Vama - Perfect fara tine",
        "The Weeknd - Blinding Lights", "Dua Lipa - Levitating"
    ]
}

# ================= AI ENGINE =================
def detect_emotion(img):
    if not AI_READY:
        return "neutral"
    try:
        res = DeepFace.analyze(np.array(img), actions=["emotion"], enforce_detection=False)
        return res[0]["dominant_emotion"]
    except:
        return "neutral"

# ================= UI =================
st.title("🎰 HERCULE AI — THE ULTIMATE DJ ENGINE")

col1, col2 = st.columns([1, 1.25])

with col1:
    remaining = max(0, SCAN_INTERVAL - int(time.time() - st.session_state.last_scan))
    st.markdown(f'<div class="timer-box">⏱️ AUTO-SCAN ÎN: {remaining:02d}s</div>', unsafe_allow_html=True)

    cam = st.camera_input("📸 AI EYE ACTIVATED")
    up = st.file_uploader("📁 SAU ÎNCARCĂ POZĂ", type=["jpg", "jpeg", "png"])

    source = cam or up

    if source:
        img = Image.open(source).convert("RGB")

        img_hash = hash(img.tobytes())
        if img_hash != st.session_state.img_hash:
            st.session_state.img_hash = img_hash
            st.session_state.last_scan = time.time()

            emotion = detect_emotion(img)
            st.session_state.emotion = emotion

            vibe = emotion if emotion in MUSIC_DB else "neutral"
            piesa = random.choice(MUSIC_DB[vibe])

            st.session_state.song = piesa
            st.session_state.query = urllib.parse.quote(piesa)

        st.image(img, width=360)
        st.markdown(f"### 🎭 Emoție detectată: **{st.session_state.emotion.upper()}**")
        st.markdown(f"### 🎵 Melodie: **{st.session_state.song}**")

        st.markdown(f"""
        <a href="https://open.spotify.com/search/{st.session_state.query}" target="_blank" class="btn-spotify">🟢 DESCHIDE ÎN SPOTIFY</a>
        <a href="https://festify.us/party/-OMkDNoyn7nohBDBnLWm" target="_blank" class="btn-festify">🔥 DESCHIDE FESTIFY PARTY</a>
        """, unsafe_allow_html=True)

with col2:
    st.subheader("📺 YouTube Player (Auto Mode)")
    if st.session_state.query:
        yt_url = f"https://www.youtube.com/embed?listType=search&list={st.session_state.query}&autoplay=1"
        st.markdown(
            f'<iframe width="100%" height="460" src="{yt_url}" frameborder="0" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>',
            unsafe_allow_html=True
        )
        st.success(f"▶ SE REDĂ: {st.session_state.song}")
    else:
        st.info("Aștept scanarea vizuală...")

# ================= TIMER REFRESH CLEAN =================
time.sleep(1)
st.rerun()
