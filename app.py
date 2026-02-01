import streamlit as st
import random, time, urllib.parse
from PIL import Image

st.set_page_config(page_title="HERCULE AI DJ SYSTEM", layout="wide")

# ===================== STYLE =====================
st.markdown("""
<style>
body { background:#0e1117; color:white; }
.card {
  background:#161b22; padding:20px; border-radius:18px;
  box-shadow:0 0 25px #000; margin-bottom:20px;
}
.title { font-size:34px; font-weight:900; }
.subtitle { font-size:18px; color:#aaa; }
.emotion { font-size:28px; font-weight:800; color:#00ffcc; }
.song { font-size:22px; font-weight:700; color:#ff4b4b; }
.btn {
  display:block; padding:14px; border-radius:30px;
  text-align:center; font-weight:700;
  text-decoration:none; margin-top:12px;
}
.btn-yt { background:#ff0000; color:white; }
.btn-sp { background:#1db954; color:white; }
.btn-fe { background:#5a5a5a; color:white; }
.timer {
  font-size:28px; font-weight:900; color:#ff4b4b;
  border:3px solid #ff4b4b; border-radius:15px;
  padding:12px; text-align:center;
}
</style>
""", unsafe_allow_html=True)

# ===================== STATE =====================
if "emotion" not in st.session_state:
    st.session_state.emotion = None
if "song" not in st.session_state:
    st.session_state.song = None
if "last_scan" not in st.session_state:
    st.session_state.last_scan = 0
if "used_songs" not in st.session_state:
    st.session_state.used_songs = set()

SCAN_INTERVAL = 120

# ===================== MUSIC DB =====================
MUSIC_DB = {
    "happy": [
        "Bruno Mars - Uptown Funk",
        "Pharrell Williams - Happy",
        "Justin Timberlake - Can't Stop the Feeling",
        "Mark Ronson - Valerie",
        "Andra - Inevitabil va fi bine",
        "Smiley - Oarecare"
    ],
    "sad": [
        "Adele - Someone Like You",
        "Sam Smith - Stay With Me",
        "Lewis Capaldi - Someone You Loved",
        "Cargo - Daca ploaia s-ar opri"
    ],
    "angry": [
        "AC/DC - Thunderstruck",
        "Metallica - Enter Sandman",
        "Eminem - Lose Yourself",
        "Parazitii - In focuri"
    ],
    "neutral": [
        "Abba - Dancing Queen",
        "Boney M - Rasputin",
        "The Weeknd - Blinding Lights",
        "Dua Lipa - Don't Start Now",
        "Zdob si Zdub - Moldovenii s-au nascut",
        "Phoenix - Andrii Popa"
    ]
}

# ===================== FUNCTIONS =====================
def pick_song(emotion):
    pool = MUSIC_DB.get(emotion, MUSIC_DB["neutral"])
    unused = [s for s in pool if s not in st.session_state.used_songs]
    if not unused:
        st.session_state.used_songs.clear()
        unused = pool
    song = random.choice(unused)
    st.session_state.used_songs.add(song)
    return song

# ===================== HEADER =====================
st.markdown('<div class="title">🎧 HERCULE AI — DJ INTELLIGENCE ENGINE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Camera • Upload • Spotify • YouTube • Festify • Party Mode</div>', unsafe_allow_html=True)
st.divider()

# ===================== LAYOUT =====================
col1, col2, col3 = st.columns([1.2, 1.4, 1])

# ===================== LEFT — CAMERA =====================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    remaining = max(0, SCAN_INTERVAL - int(time.time() - st.session_state.last_scan))
    st.markdown(f'<div class="timer">⏱️ AUTO SCAN: {remaining:02d}s</div>', unsafe_allow_html=True)

    cam = st.camera_input("📸 Capture from camera")
    up = st.file_uploader("📁 Upload image", type=["jpg","jpeg","png"])

    source = cam if cam is not None else up

    if source:
        img = Image.open(source).convert("RGB")
        st.image(img, caption="Input image", use_container_width=True)

        # === TEMP AI (random emotion) — stabil în browser online ===
        emotion = random.choice(list(MUSIC_DB.keys()))
        st.session_state.emotion = emotion
        st.session_state.song = pick_song(emotion)
        st.session_state.last_scan = time.time()

    st.markdown('</div>', unsafe_allow_html=True)

# ===================== CENTER — RESULT =====================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.session_state.song:
        st.markdown(f'🎭 Emotion detected:<div class="emotion">{st.session_state.emotion.upper()}</div>', unsafe_allow_html=True)
        st.markdown(f'🎵 Recommended track:<div class="song">{st.session_state.song}</div>', unsafe_allow_html=True)
    else:
        st.info("Waiting for scan...")

    st.markdown('</div>', unsafe_allow_html=True)

# ===================== RIGHT — PLAYERS =====================
with col3:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.session_state.song:
        q = urllib.parse.quote(st.session_state.song)
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

# ===================== AUTO REFRESH TIMER =====================
time.sleep(1)
st.rerun()
