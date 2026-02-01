import streamlit as st
import time, random, urllib.parse
from PIL import Image
import numpy as np

# ========== CONFIG ==========
st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

st.markdown("""
<style>
.main { background:#0e1117; color:white; }
iframe { border-radius:20px; border:4px solid #1ed760; box-shadow: 0 0 25px #1ed760; }
.timer-box {
  font-size: 36px; font-weight: 900; color: #ff4b4b;
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

# ========== STATE ==========
if "last_scan" not in st.session_state:
    st.session_state.last_scan = 0
if "song" not in st.session_state:
    st.session_state.song = ""
if "emotion" not in st.session_state:
    st.session_state.emotion = "neutral"
if "yt_query" not in st.session_state:
    st.session_state.yt_query = ""

SCAN_INTERVAL = 120

# ========== MUSIC DB ==========
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

# ========== UI ==========
st.title("🎰 HERCULE AI — DJ VIBE ENGINE")

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

        if st.session_state.get("img_hash") != img_hash:
            st.session_state.img_hash = img_hash
            st.session_state.last_scan = time.time()

            emotion = random.choice(list(MUSIC_DB.keys()))
            st.session_state.emotion = emotion
            st.session_state.song = random.choice(MUSIC_DB[emotion])
            st.session_state.yt_query = urllib.parse.quote(st.session_state.song)

        st.image(img, width=360)
        st.markdown(f"### 🎭 Emoție: **{st.session_state.emotion.upper()}**")
        st.markdown(f"### 🎵 Melodie: **{st.session_state.song}**")

        if st.session_state.song:
            q = urllib.parse.quote(st.session_state.song)
            st.markdown(f"""
            <a href="https://open.spotify.com/search/{q}" target="_blank" class="btn-spotify">🟢 DESCHIDE ÎN SPOTIFY</a>
            <a href="https://festify.us/party/-OMkDNoyn7nohBDBnLWm" target="_blank" class="btn-festify">🔥 DESCHIDE FESTIFY PARTY</a>
            """, unsafe_allow_html=True)

with col2:
    st.subheader("📺 YouTube Player LIVE")
    if st.session_state.yt_query:
        yt_url = f"https://www.youtube.com/embed?listType=search&list={st.session_state.yt_query}"
        st.markdown(
            f'<iframe width="100%" height="460" src="{yt_url}" frameborder="0" allow="autoplay; encrypted-media; fullscreen" allowfullscreen></iframe>',
            unsafe_allow_html=True
        )
    else:
        st.info("Aștept scanarea pentru video...")

# Refresh soft pentru timer
time.sleep(1)
st.rerun()
