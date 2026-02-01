<!DOCTYPE html>
<html lang="ro">
<head>
  <meta charset="UTF-8">
  <title>MV STUDIO PRO – STABLE FIX</title>
  <style>
    body {
      margin: 0;
      background: #0b0b0b;
      color: white;
      font-family: Arial, sans-serif;
      overflow: hidden;
    }

    #stage {
      position: relative;
      width: 100vw;
      height: 100vh;
      background: radial-gradient(circle at center, #151515, #050505);
    }

    /* CAMERA CERC */
    #camera-wrapper {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 280px;
      height: 280px;
      transform: translate(-50%, -50%);
      border-radius: 50%;
      overflow: hidden;
      border: 4px solid #00ffcc;
      box-shadow: 0 0 25px #00ffcc88;
      background: black;
    }

    #camera {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    /* VUMETRU */
    #vumeter-container {
      position: absolute;
      top: 50%;
      left: 50%;
      width: 340px;
      height: 340px;
      transform: translate(-50%, -50%);
      pointer-events: none;
    }

    canvas {
      width: 100%;
      height: 100%;
    }

    /* TEXT DRAG */
    .draggable {
      position: absolute;
      cursor: move;
      font-size: 28px;
      font-weight: bold;
      color: #00ffcc;
      text-shadow: 0 0 10px black;
      user-select: none;
    }

    #controls {
      position: fixed;
      bottom: 10px;
      left: 50%;
      transform: translateX(-50%);
      background: #111;
      padding: 10px 16px;
      border-radius: 12px;
      display: flex;
      gap: 10px;
      box-shadow: 0 0 20px #000;
    }

    button {
      background: #00ffcc;
      border: none;
      padding: 6px 12px;
      border-radius: 6px;
      cursor: pointer;
      font-weight: bold;
    }

    input {
      padding: 6px;
      border-radius: 6px;
      border: none;
    }
  </style>
</head>
<body>

<div id="stage">

  <!-- CAMERA -->
  <div id="camera-wrapper">
    <video id="camera" autoplay muted playsinline></video>
  </div>

  <!-- VUMETRU -->
  <div id="vumeter-container">
    <canvas id="vumeter"></canvas>
  </div>

  <!-- TEXT PERSONALIZAT -->
  <div id="customText" class="draggable" style="top: 20%; left: 20%;">
    MV STUDIO PRO LIVE
  </div>

</div>

<!-- CONTROLS -->
<div id="controls">
  <input id="textInput" placeholder="Text nou..." />
  <button onclick="updateText()">Set Text</button>
  <button onclick="toggleCamera()">Camera ON/OFF</button>
</div>

<script>
/* ================= CAMERA ================= */
const video = document.getElementById("camera");
let stream = null;

async function startCamera() {
  stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
  video.srcObject = stream;
}

function stopCamera() {
  if (!stream) return;
  stream.getTracks().forEach(t => t.stop());
  stream = null;
}

function toggleCamera() {
  stream ? stopCamera() : startCamera();
}

startCamera();

/* ================= AUDIO / VUMETRU ================= */
const canvas = document.getElementById("vumeter");
const ctx = canvas.getContext("2d");

function resizeCanvas() {
  canvas.width = canvas.offsetWidth;
  canvas.height = canvas.offsetHeight;
}
resizeCanvas();
window.addEventListener("resize", resizeCanvas);

let audioCtx, analyser, dataArray;

navigator.mediaDevices.getUserMedia({ audio: true }).then(stream => {
  audioCtx = new AudioContext();
  const source = audioCtx.createMediaStreamSource(stream);
  analyser = audioCtx.createAnalyser();
  analyser.fftSize = 256;
  dataArray = new Uint8Array(analyser.frequencyBinCount);
  source.connect(analyser);
  drawVumeter();
});

function drawVumeter() {
  requestAnimationFrame(drawVumeter);
  analyser.getByteFrequencyData(dataArray);

  ctx.clearRect(0, 0, canvas.width, canvas.height);

  const bars = 64;
  const radius = canvas.width / 2 - 10;
  const center = canvas.width / 2;

  for (let i = 0; i < bars; i++) {
    const value = dataArray[i] / 255;
    const barHeight = radius * value;
    const angle = (i / bars) * Math.PI * 2;

    const x1 = center + Math.cos(angle) * radius;
    const y1 = center + Math.sin(angle) * radius;
    const x2 = center + Math.cos(angle) * (radius + barHeight);
    const y2 = center + Math.sin(angle) * (radius + barHeight);

    ctx.strokeStyle = `hsl(${i * 6}, 100%, 50%)`;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(x1, y1);
    ctx.lineTo(x2, y2);
    ctx.stroke();
  }
}

/* ================= DRAG TEXT ================= */
const textEl = document.getElementById("customText");
let dragging = false;
let offsetX, offsetY;

textEl.addEventListener("mousedown", e => {
  dragging = true;
  offsetX = e.clientX - textEl.offsetLeft;
  offsetY = e.clientY - textEl.offsetTop;
});

document.addEventListener("mousemove", e => {
  if (!dragging) return;
  textEl.style.left = (e.clientX - offsetX) + "px";
  textEl.style.top = (e.clientY - offsetY) + "px";
});

document.addEventListener("mouseup", () => dragging = false);

/* ================= TEXT UPDATE ================= */
function updateText() {
  const val = document.getElementById("textInput").value;
  if (val.trim()) textEl.textContent = val;
}
</script>

</body>
</html>
