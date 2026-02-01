<!DOCTYPE html>
<html lang="ro">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>MV STUDIO PRO - STABLE FIX</title>

<script src="https://cdn.tailwindcss.com"></script>
<script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js"></script>
<script src="https://www.gstatic.com/firebasejs/8.10.0/firebase-database.js"></script>

<style>
:root { --main:#ffaa00; --msg-size:26px; }
html,body{margin:0;width:100%;height:100%;background:#000;color:#fff;font-family:sans-serif;overflow:hidden}

#viewport{position:relative;width:100%;height:calc(100% - 250px);background:#000;border-bottom:2px solid #333}

#bg-v,#bg-i,#bg-s{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;display:none;z-index:1}

#cam-box{position:absolute;z-index:10;display:none;cursor:move}
#v-src{width:420px;object-fit:contain;border-radius:12px;box-shadow:0 0 15px #000}

#circle-box{
  position:absolute;
  z-index:15;
  cursor:move;
  width:300px;
  height:300px;
  display:flex;
  align-items:center;
  justify-content:center;
}
#radial-canvas{
  position:absolute;
  inset:0;
  pointer-events:none;
}
#inner-circle{
  width:150px;
  height:150px;
  border-radius:50%;
  border:2px solid var(--main);
  background:rgba(0,0,0,.25);
  overflow:hidden;
  display:flex;
  align-items:center;
  justify-content:center;
  z-index:2;
}
#inner-img{width:100%;height:100%;object-fit:cover;display:none}

#branding{
  position:absolute;
  z-index:20;
  cursor:move;
  font-weight:900;
  text-transform:uppercase;
  text-shadow:2px 2px 10px #000;
  outline:none;
  user-select:none;
}

#msg-box{
  position:absolute;
  z-index:999;
  background:rgba(0,0,0,.85);
  border-left:8px solid var(--main);
  padding:20px;
  border-radius:0 15px 15px 0;
  min-width:320px;
  cursor:move;
  display:none;
  top:100px;
  left:50px;
}

#controls{
  position:absolute;
  bottom:0;left:0;right:0;height:250px;
  background:#111;
  display:grid;
  grid-template-columns:repeat(5,1fr);
  gap:10px;
  padding:15px;
}
.panel{background:#1a1a1a;padding:10px;border-radius:8px;border:1px solid #333;display:flex;flex-direction:column;gap:5px}
.panel h3{font-size:10px;color:var(--main);text-transform:uppercase;font-weight:bold;text-align:center;border-bottom:1px solid #333;margin-bottom:4px}

.btn{width:100%;padding:7px;font-weight:bold;border-radius:4px;text-transform:uppercase;font-size:9px;cursor:pointer;border:none}
.st-off{background:#ff0000;color:#fff}
.st-on{background:#00ff00;color:#000}
.btn-blue{background:#2563eb;color:#fff}

input[type=file]{font-size:9px;background:#000;color:#666;width:100%}
input[type=range]{accent-color:var(--main)}
label{font-size:9px;color:#888}
</style>
</head>

<body>

<div id="viewport">
  <video id="bg-v" autoplay loop muted></video>
  <img id="bg-i">
  <img id="bg-s">

  <div id="cam-box" style="top:60px;right:60px;">
    <video id="v-src" autoplay playsinline muted></video>
  </div>

  <div id="circle-box" style="top:20%;left:35%;">
    <canvas id="radial-canvas"></canvas>
    <div id="inner-circle">
      <img id="inner-img">
    </div>
  </div>

  <div id="branding" contenteditable="true" style="bottom:150px;left:50px;font-size:40px;">
    CLICK PT TEXT
  </div>

  <div id="msg-box">
    <span id="msg-user" style="color:var(--main);font-weight:bold;">INVITAT</span><br>
    <span id="msg-txt" style="font-size:var(--msg-size);">Mesaj...</span>
  </div>
</div>

<div id="controls">
  <div class="panel">
    <h3>1. MEDIA UPLOAD</h3>
    <label>Video:</label><input type="file" accept="video/*" onchange="Media.loadFile(this,'bg-v')">
    <label>Foto:</label><input type="file" accept="image/*" onchange="Media.loadFile(this,'bg-i')">
    <label>Folder Slide:</label><input type="file" webkitdirectory directory multiple onchange="Slides.loadFolder(this)">
  </div>

  <div class="panel">
    <h3>2. CONTROL FUNDAL</h3>
    <button id="btn-v" class="btn st-off" onclick="Media.toggleLayer('bg-v','btn-v')">VIDEO: OFF</button>
    <button id="btn-i" class="btn st-off" onclick="Media.toggleLayer('bg-i','btn-i')">FOTO: OFF</button>
    <button id="btn-s" class="btn st-off" onclick="Media.toggleLayer('bg-s','btn-s')">SLIDE: OFF</button>
    <label>Viteza Slide:</label><input type="range" min="1" max="15" value="3" id="s-spd">
  </div>

  <div class="panel">
    <h3>3. WEBCAM & AI CUT</h3>
    <button class="btn btn-blue" onclick="Camera.start()">START CAMERA</button>
    <button id="btn-cam" class="btn st-off" onclick="Camera.toggle()">AI CUT / CAM: OFF</button>
    <label>Marime:</label><input type="range" min="200" max="1500" value="420" oninput="vSrc.style.width=this.value+'px'">
    <label>Opacitate:</label><input type="range" min="0" max="1" step="0.1" value="1" oninput="camBox.style.opacity=this.value">
  </div>

  <div class="panel">
    <h3>4. CERC VUMETRU</h3>
    <button id="btn-png" class="btn st-off" onclick="Circle.toggleLogo()">LOGO CERC: OFF</button>
    <input type="file" accept="image/*" onchange="Circle.loadLogo(this)">
    <label>Marime Cerc:</label><input type="range" min="0.5" max="2" step="0.1" value="1" id="v-scale">
  </div>

  <div class="panel">
    <h3>5. TEXT & FIREBASE</h3>
    <label>Marime Text Ecran:</label>
    <input type="range" min="20" max="150" value="40" oninput="branding.style.fontSize=this.value+'px'">
    <hr class="border-gray-700 my-1">
    <label>Marime Mesaj:</label>
    <input type="range" min="15" max="80" value="26" oninput="document.documentElement.style.setProperty('--msg-size',this.value+'px')">
    <label>Timp Afisare:</label>
    <input type="range" min="2" max="30" value="8" id="m-time">
  </div>
</div>

<script>
/* =====================
   GLOBALS
===================== */
const bgV = document.getElementById('bg-v');
const bgI = document.getElementById('bg-i');
const bgS = document.getElementById('bg-s');
const camBox = document.getElementById('cam-box');
const vSrc = document.getElementById('v-src');
const branding = document.getElementById('branding');
const circleBox = document.getElementById('circle-box');
const radialCanvas = document.getElementById('radial-canvas');
const ctx = radialCanvas.getContext('2d');

let slideTimer = null;
let msgTimer = null;

/* =====================
   FIREBASE
===================== */
firebase.initializeApp({
  databaseURL: "https://felicitari-nunta-default-rtdb.firebaseio.com"
});
const db = firebase.database().ref('test_dj');

/* =====================
   MEDIA
===================== */
const Media = {
  loadFile(input, id) {
    const f = input.files[0];
    if (!f) return;
    const url = URL.createObjectURL(f);
    const el = document.getElementById(id);
    el.src = url;
    if (el.tagName === 'VIDEO') el.play();
  },

  toggleLayer(id, btnId) {
    const el = document.getElementById(id);
    const btn = document.getElementById(btnId);
    const on = el.style.display === 'block';

    ['bg-v','bg-i','bg-s'].forEach(x => document.getElementById(x).style.display='none');
    ['btn-v','btn-i','btn-s'].forEach(x=>{
      const b=document.getElementById(x);
      b.className='btn st-off';
      b.innerText=b.innerText.split(':')[0]+': OFF';
    });
    if (slideTimer) clearTimeout(slideTimer);

    if (!on) {
      el.style.display='block';
      btn.className='btn st-on';
      btn.innerText=btn.innerText.split(':')[0]+': ON';
      if (id==='bg-s') Slides.start();
    }
  }
};

/* =====================
   SLIDES
===================== */
const Slides = {
  files: [],
  idx: 0,

  loadFolder(input) {
    this.files = Array.from(input.files)
      .filter(f => f.type.startsWith('image/'))
      .map(f => URL.createObjectURL(f));
    this.idx = 0;
  },

  start() {
    if (!this.files.length) return;
    bgS.src = this.files[this.idx];
    this.idx = (this.idx + 1) % this.files.length;
    slideTimer = setTimeout(() => this.start(), document.getElementById('s-spd').value * 1000);
  }
};

/* =====================
   CAMERA + VU
===================== */
const Camera = {
  stream: null,
  audioCtx: null,
  analyser: null,
  data: null,
  running: false,

  async start() {
    if (this.stream) return;
    try {
      this.stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
      vSrc.srcObject = this.stream;

      this.audioCtx = new AudioContext();
      const src = this.audioCtx.createMediaStreamSource(this.stream);
      this.analyser = this.audioCtx.createAnalyser();
      this.analyser.fftSize = 256;
      src.connect(this.analyser);
      this.data = new Uint8Array(this.analyser.frequencyBinCount);

      Circle.resizeCanvas();
      this.running = true;
      this.draw();
      Firebase.listen();
    } catch (e) {
      alert("Camera error: " + e);
    }
  },

  toggle() {
    const btn = document.getElementById('btn-cam');
    if (camBox.style.display === 'block') {
      camBox.style.display = 'none';
      btn.className = 'btn st-off';
      btn.innerText = 'AI CUT / CAM: OFF';
    } else {
      camBox.style.display = 'block';
      btn.className = 'btn st-on';
      btn.innerText = 'AI CUT / CAM: ON';
    }
  },

  draw() {
    if (!this.running) return;
    requestAnimationFrame(() => this.draw());

    this.analyser.getByteFrequencyData(this.data);
    ctx.clearRect(0, 0, radialCanvas.width, radialCanvas.height);

    let sum = 0;
    for (let i = 0; i < 20; i++) sum += this.data[i];
    const base = document.getElementById('v-scale').value;
    circleBox.style.transform = `scale(${base * (1 + (sum / 20 / 255) * 0.15)})`;

    const cx = radialCanvas.width / 2;
    const cy = radialCanvas.height / 2;

    ctx.strokeStyle = '#ffaa00';
    ctx.lineWidth = 4;

    for (let i = 0; i < 60; i++) {
      const a = i * 6 * Math.PI / 180;
      const l = this.data[i] * 0.45;
      ctx.beginPath();
      ctx.moveTo(cx + Math.cos(a) * 85, cy + Math.sin(a) * 85);
      ctx.lineTo(cx + Math.cos(a) * (85 + l), cy + Math.sin(a) * (85 + l));
      ctx.stroke();
    }
  }
};

/* =====================
   CIRCLE LOGO
===================== */
const Circle = {
  loadLogo(input) {
    const img = document.getElementById('inner-img');
    if (!input.files[0]) return;
    img.src = URL.createObjectURL(input.files[0]);
    img.style.display = 'block';
  },

  toggleLogo() {
    const img = document.getElementById('inner-img');
    const btn = document.getElementById('btn-png');
    if (img.style.display === 'block') {
      img.style.display = 'none';
      btn.className = 'btn st-off';
      btn.innerText = 'LOGO CERC: OFF';
    } else {
      img.style.display = 'block';
      btn.className = 'btn st-on';
      btn.innerText = 'LOGO CERC: ON';
    }
  },

  resizeCanvas() {
    const size = 300;
    const dpr = window.devicePixelRatio || 1;
    radialCanvas.width = size * dpr;
    radialCanvas.height = size * dpr;
    radialCanvas.style.width = size + 'px';
    radialCanvas.style.height = size + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
  }
};

/* =====================
   FIREBASE LISTENER
===================== */
const Firebase = {
  listening: false,

  listen() {
    if (this.listening) return;
    this.listening = true;

    db.limitToLast(1).on('child_added', snap => {
      const d = snap.val() || {};
      const box = document.getElementById('msg-box');
      document.getElementById('msg-user').innerText = d.author || 'INVITAT';
      document.getElementById('msg-txt').innerText = '"' + (d.text || '') + '"';
      box.style.display = 'block';
      if (msgTimer) clearTimeout(msgTimer);
      msgTimer = setTimeout(() => box.style.display = 'none',
        document.getElementById('m-time').value * 1000
      );
    });
  }
};

/* =====================
   DRAG ENGINE - FIXED
===================== */
function makeDraggable(el) {
  let startX, startY, elX, elY;

  el.addEventListener('mousedown', e => {
    if (['INPUT','BUTTON','TEXTAREA'].includes(e.target.tagName) || e.target.isContentEditable) return;
    e.preventDefault();
    startX = e.clientX;
    startY = e.clientY;
    elX = el.offsetLeft;
    elY = el.offsetTop;

    document.addEventListener('mousemove', move);
    document.addEventListener('mouseup', stop);
  });

  function move(e) {
    el.style.left = elX + (e.clientX - startX) + 'px';
    el.style.top = elY + (e.clientY - startY) + 'px';
  }

  function stop() {
    document.removeEventListener('mousemove', move);
    document.removeEventListener('mouseup', stop);
  }
}

['msg-box','circle-box','cam-box','branding'].forEach(id =>
  makeDraggable(document.getElementById(id))
);

window.addEventListener('resize', Circle.resizeCanvas);
Circle.resizeCanvas();
</script>

</body>
</html>
