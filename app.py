import streamlit as st
import random, time, urllib.parse

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
    st.session_state.emotion = "neutral"
if "song" not in st.session_state:
    st.session_state.song = ""
if "last_scan" not in st.session_state:
    st.session_state.last_scan = 0

SCAN_INTERVAL = 120

# ===================== MUSIC DB =====================
MUSIC_DB = {
    "happy": [
        "Bruno Mars - Uptown Funk",
        "Pharrell Williams - Happy",
        "Justin Timberlake - Can't Stop the Feeling",
        "Mark Ronson - Valerie"
    ],
    "sad": [
        "Adele - Someone Like You",
        "Sam Smith - Stay With Me",
        "Lewis Capaldi - Someone You Loved"
    ],
    "angry": [
        "AC/DC - Thunderstruck",
        "Metallica - Enter Sandman",
        "Eminem - Lose Yourself"
    ],
    "neutral": [
        "Abba - Dancing Queen",
        "Boney M - Rasputin",
        "The Weeknd - Blinding Lights",
        "Dua Lipa - Don't Start Now"
    ]
}

# ===================== HEADER =====================
st.markdown('<div class="title">🎧 HERCULE AI — DJ INTELLIGENCE ENGINE</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Emotion scan • Spotify • YouTube • Festify • Party mode</div>', unsafe_allow_html=True)
st.divider()

# ===================== LAYOUT =====================
col1, col2, col3 = st.columns([1.1, 1.2, 1])

# ===================== LEFT — CAMERA =====================
with col1:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    remaining = max(0, SCAN_INTERVAL - int(time.time() - st.session_state.last_scan))
    st.markdown(f'<div class="timer">⏱️ AUTO SCAN: {remaining:02d}s</div>', unsafe_allow_html=True)

    cam = st.camera_input("📸 Scan audience")
    up = st.file_uploader("📁 Upload photo", type=["jpg","jpeg","png"])
    source = cam or up

    if source:
        st.session_state.last_scan = time.time()
        st.session_state.emotion = random.choice(list(MUSIC_DB.keys()))
        st.session_state.song = random.choice(MUSIC_DB[st.session_state.emotion])

    st.markdown('</div>', unsafe_allow_html=True)

# ===================== CENTER — ANALYSIS =====================
with col2:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    if st.session_state.song:
        st.markdown(f'🎭 Emotion detected: <div class="emotion">{st.session_state.emotion.upper()}</div>', unsafe_allow_html=True)
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

# ===================== AUTO REFRESH =====================
time.sleep(1)
st.rerun()
