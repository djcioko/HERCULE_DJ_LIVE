import streamlit as st
import time, random, urllib.parse

st.set_page_config(page_title="HERCULE AI DJ", layout="wide")

st.markdown("""
<style>
.main { background:#0e1117; color:white; }
.timer-box {
  font-size: 36px; font-weight: 900; color: #ff4b4b;
  text-align: center; border: 3px solid #ff4b4b;
  border-radius: 15px; padding: 12px; margin-bottom: 20px;
}
.btn-play {
  background:#ff0000; color:white; padding:16px;
  border-radius:30px; text-align:center;
  font-weight:bold; display:block;
  text-decoration:none; margin-top:20px;
  font-size:18px;
}
.thumb {
  border-radius:20px;
  box-shadow:0 0 25px #000;
  width:100%;
}
</style>
""", unsafe_allow_html=True)

# ================= STATE =================
if "last_scan" not in st.session_state:
    st.session_state.last_scan = 0
if "song" not in st.session_state:
    st.session_state.song = ""
if "emotion" not in st.session_state:
    st.session_state.emotion = "neutral"

SCAN_INTERVAL = 120

# ================= MUSIC DB =================
MUSIC_DB = {
    "happy": ["Bruno Mars - Marry You", "Pharrell Williams - Happy", "Daft Punk - Get Lucky"],
    "angry": ["AC/DC - Thunderstruck", "Metallica - Enter Sandman", "Eminem - Lose Yourself"],
    "sad": ["Adele - Someone Like You", "Sam Smith - Stay With Me"],
    "neutral": ["Abba - Dancing Queen", "Boney M - Rasputin", "The Weeknd - Blinding Lights"]
}

# ================= UI =================
st.title("🎰 HERCULE AI — DJ VIBE ENGINE")

col1, col2 = st.columns([1, 1.2])

with col1:
    remaining = max(0, SCAN_INTERVAL - int(time.time() - st.session_state.last_scan))
    st.markdown(f'<div class="timer-box">⏱️ AUTO-SCAN ÎN: {remaining:02d}s</div>', unsafe_allow_html=True)

    cam = st.camera_input("📸 AI EYE ACTIVATED")
    up = st.file_uploader("📁 SAU ÎNCARCĂ POZĂ", type=["jpg", "jpeg", "png"])
    source = cam or up

    if source:
        st.session_state.last_scan = time.time()
        emotion = random.choice(list(MUSIC_DB.keys()))
        st.session_state.emotion = emotion
        st.session_state.song = random.choice(MUSIC_DB[emotion])

        st.markdown(f"### 🎭 Emoție: **{emotion.upper()}**")
        st.markdown(f"### 🎵 Melodie: **{st.session_state.song}**")

with col2:
    if st.session_state.song:
        query = urllib.parse.quote(st.session_state.song)
        yt_url = f"https://www.youtube.com/results?search_query={query}"

        st.markdown(f"""
        <img src="https://img.youtube.com/vi/VIDEOID/0.jpg" class="thumb">
        <a href="{yt_url}" target="_blank" class="btn-play">▶ DESCHIDE PE YOUTUBE</a>
        """, unsafe_allow_html=True)
    else:
        st.info("Aștept scanarea...")

time.sleep(1)
st.rerun()
