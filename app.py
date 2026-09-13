from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

k1 = "AQ.Ab8RN6JnrZf"
k2 = "Ryk5O8V3_2cWg6"
k3 = "A7Qkl5fPk6pdNg1tnxgyWNkWg"
API_KEY = k1 + k2 + k3

URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.6-flash:generateContent?key={API_KEY}"

HTML_CODE = """
<!DOCTYPE html>
<html lang="bn">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>MAYA AI ASSISTANT</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        :root {
            --bg-color: #030106;
            --primary: #ff007f;
            --secondary: #00f0ff;
            --box-bg: rgba(12, 3, 18, 0.95);
        }
        html, body {
            width: 100%; height: 100%;
            background-color: var(--bg-color); color: var(--primary);
            overflow: hidden; position: relative;
            transition: 0.3s background-color;
        }
        #matrixCanvas {
            position: absolute; top: 0; left: 0;
            width: 100%; height: 100%; z-index: 1; opacity: 0.35;
        }
        .hud-wrapper {
            position: relative; z-index: 2; width: 100%; height: 100%;
            display: flex; flex-direction: column; justify-content: space-between;
            padding: 12px 14px 18px 14px;
        }

        /* Top Cyber Header */
        .top-cyber-panel {
            display: flex; justify-content: space-between; align-items: center;
            border-bottom: 2px solid rgba(255, 0, 127, 0.5); padding-bottom: 6px;
        }
        .brand-title {
            font-size: 24px; font-weight: 900; letter-spacing: 4px; color: #fff;
            text-shadow: 0 0 10px var(--primary), 0 0 25px var(--primary);
        }
        .nav-controls {
            display: flex; gap: 8px; align-items: center;
        }
        .mode-select {
            background: rgba(25, 5, 30, 0.95); color: var(--secondary);
            border: 2px solid var(--primary); padding: 6px 8px; border-radius: 12px;
            font-size: 13px; font-weight: bold; outline: none;
        }
        .gear-btn {
            background: rgba(25, 5, 30, 0.95); border: 2px solid var(--secondary);
            color: var(--secondary); border-radius: 50%; width: 36px; height: 36px;
            font-size: 18px; cursor: pointer; display: flex; justify-content: center; align-items: center;
            outline: none;
        }

        /* Reactor Core */
        .reactor-container {
            display: flex; justify-content: center; align-items: center;
            position: relative; height: 170px; margin: auto 0;
        }
        .ring-1 {
            position: absolute; width: 160px; height: 160px; border-radius: 50%;
            border: 2px dashed var(--primary); animation: rotateClock 10s linear infinite;
        }
        .ring-2 {
            position: absolute; width: 130px; height: 130px; border-radius: 50%;
            border: 2px dotted var(--secondary); animation: rotateCounter 6s linear infinite;
        }
        .inner-core {
            width: 80px; height: 80px; border-radius: 50%;
            background: radial-gradient(circle, #ffffff 0%, var(--primary) 60%, #55002b 100%);
            box-shadow: 0 0 35px var(--primary), 0 0 70px #ff0055, inset 0 0 20px #fff;
            animation: coreBreath 2s infinite ease-in-out; transition: 0.3s;
        }
        .speaking-core {
            animation: speakReaction 0.25s infinite alternate ease-in-out !important;
            box-shadow: 0 0 60px #ff0055, 0 0 120px #ff00aa, 0 0 150px #fff !important;
        }
        @keyframes rotateClock { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
        @keyframes rotateCounter { from { transform: rotate(360deg); } to { transform: rotate(0deg); } }
        @keyframes coreBreath { 0%, 100% { transform: scale(0.92); } 50% { transform: scale(1.08); } }
        @keyframes speakReaction { 0% { transform: scale(1.0); } 100% { transform: scale(1.25); } }

        /* Preview Thumbnail */
        #imgPreviewBox {
            display: none; align-items: center; gap: 10px;
            background: rgba(0, 240, 255, 0.1); border: 1px dashed var(--secondary);
            padding: 6px 12px; border-radius: 10px; font-size: 13px; color: var(--secondary);
        }
        #imgThumb { width: 32px; height: 32px; border-radius: 6px; object-fit: cover; }

        /* Terminal Console */
        .bottom-section { width: 100%; display: flex; flex-direction: column; gap: 10px; }
        .terminal-box {
            background: var(--box-bg); border: 2px solid var(--primary);
            border-left: 5px solid var(--secondary); border-radius: 12px; padding: 10px 14px;
            box-shadow: 0 0 25px rgba(255, 0, 127, 0.3); text-align: left;
            max-height: 125px; overflow-y: auto;
        }
        .terminal-header {
            font-size: 12px; font-weight: bold; color: var(--secondary);
            display: flex; justify-content: space-between; margin-bottom: 4px;
        }
        #chatOutput { font-size: 17px; font-weight: 500; color: #ffffff; line-height: 1.5; min-height: 44px; }

        /* Controls */
        .cyber-controls {
            display: flex; gap: 6px; align-items: center; width: 100%;
            background: rgba(18, 5, 25, 0.95); padding: 5px; border-radius: 35px;
            border: 2px solid rgba(255, 0, 127, 0.5);
        }
        .plus-btn {
            width: 44px; height: 44px; border-radius: 50%; border: 2px solid var(--secondary);
            background: rgba(0, 240, 255, 0.15); color: var(--secondary); font-size: 24px;
            font-weight: 900; display: flex; justify-content: center; align-items: center;
            cursor: pointer; flex-shrink: 0;
        }
        .cyber-input {
            flex: 1; padding: 12px 14px; border-radius: 25px;
            background: rgba(28, 8, 35, 0.95); border: 1px solid var(--primary);
            color: #fff; outline: none; font-size: 15px;
        }
        .cyber-btn {
            width: 44px; height: 44px; border-radius: 50%; border: 2px solid var(--secondary);
            background: linear-gradient(135deg, var(--primary), #77003c); color: #fff;
            font-size: 18px; display: flex; justify-content: center; align-items: center;
            cursor: pointer; outline: none; flex-shrink: 0;
        }

        /* সেটিংস প্যানেল ও মেনুবার মডাল */
        #settingsOverlay {
            display: none; position: absolute; top: 0; left: 0;
            width: 100%; height: 100%; background: rgba(0, 0, 0, 0.85);
            z-index: 100; justify-content: center; align-items: center;
        }
        .settings-card {
            background: #0d0413; border: 2px solid var(--secondary);
            width: 90%; max-width: 380px; border-radius: 16px;
            padding: 20px; box-shadow: 0 0 35px rgba(0, 240, 255, 0.4);
            color: #fff;
        }
        .settings-card h2 {
            font-size: 20px; color: var(--secondary); margin-bottom: 15px;
            display: flex; justify-content: space-between; align-items: center;
        }
        .setting-row {
            margin-bottom: 14px; font-size: 14px; display: flex;
            justify-content: space-between; align-items: center;
        }
        .about-box {
            background: rgba(255, 0, 127, 0.1); border: 1px solid var(--primary);
            padding: 10px; border-radius: 10px; margin-top: 15px; font-size: 13px; line-height: 1.4;
        }
    </style>
</head>
<body>
    <canvas id="matrixCanvas"></canvas>

    <div class="hud-wrapper">
        <div class="top-cyber-panel">
            <div class="brand-title">M A Y A</div>
            <div class="nav-controls">
                <select id="moodSelect" class="mode-select">
                    <option value="friend">💖 Best Friend</option>
                    <option value="gf">❤️ GF Mood</option>
                    <option value="study">🎓 Study Helper</option>
                    <option value="pro">💼 Professional</option>
                </select>
                <button class="gear-btn" onclick="openSettings()">⚙️</button>
            </div>
        </div>

        <div class="reactor-container">
            <div class="ring-1"></div>
            <div class="ring-2"></div>
            <div id="core" class="inner-core"></div>
        </div>

        <div class="bottom-section">
            <div id="imgPreviewBox">
                <img id="imgThumb" src="" alt="Scan">
                <span>📸 ছবি স্ক্যান হয়েছে! প্রশ্ন করো।</span>
                <span style="cursor:pointer; margin-left:auto; font-weight:bold;" onclick="clearImage()">✖</span>
            </div>

            <div class="terminal-box">
                <div class="terminal-header">
                    <span id="hudState">&gt; SYSTEM ONLINE</span>
                    <span id="voiceLabel" style="color: var(--primary);">VOICE: MAYA</span>
                </div>
                <div id="chatOutput">নমস্কার! আমি মায়া। কিছু বলুন বা লিখে জানান!</div>
            </div>

            <div class="cyber-controls">
                <button class="plus-btn" onclick="document.getElementById('cameraInput').click()">＋</button>
                <input type="file" id="cameraInput" accept="image/*" capture="environment" style="display: none;" onchange="handleImage(this)">
                
                <input type="text" id="userMsg" class="cyber-input" placeholder="tumi kemon acho likhun..." onkeypress="if(event.key==='Enter') sendPrompt()">
                
                <button class="cyber-btn" onclick="sendPrompt()">➤</button>
                <button class="cyber-btn" onclick="listenVoice()" style="border-color: var(--primary); background: linear-gradient(135deg, #ff0055, #330015);">🎤</button>
            </div>
        </div>
    </div>

    <div id="settingsOverlay">
        <div class="settings-card">
            <h2>
                <span>⚙️ System Settings</span>
                <span style="cursor:pointer; font-size:18px;" onclick="closeSettings()">✕</span>
            </h2>
            
            <div class="setting-row">
                <span>Theme Mode:</span>
                <select id="themeSelect" onchange="changeTheme(this.value)" style="padding:4px 8px; border-radius:6px; background:#1a0524; color:#fff; border:1px solid var(--secondary);">
                    <option value="cyber">Dark Cyberpunk</option>
                    <option value="midnight">Midnight Blue</option>
                </select>
            </div>

            <div class="setting-row">
                <span>Voice Speed:</span>
                <input type="range" id="voiceSpeed" min="0.8" max="1.4" step="0.1" value="1.0">
            </div>

            <div class="about-box">
                <p><strong>App:</strong> MAYA Virtual Assistant</p>
                <p><strong>Version:</strong> v3.6 Neural Engine</p>
                <p><strong>Boss / Creator:</strong> <span style="color:#00f0ff; font-weight:bold;">প্রদীপ দত্ত (Pradip Dutta)</span></p>
            </div>
        </div>
    </div>

    <script>
        const canvas = document.getElementById('matrixCanvas');
        const ctx = canvas.getContext('2d');
        function setupMatrix() { canvas.width = window.innerWidth; canvas.height = window.innerHeight; }
        setupMatrix();
        window.addEventListener('resize', setupMatrix);

        const chars = "মায়াMAYA010101XYZ0123456789";
        const fontSize = 14;
        const drops = Array(Math.floor(canvas.width / fontSize)).fill(1);

        function drawMatrix() {
            ctx.fillStyle = "rgba(3, 1, 6, 0.12)";
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            for (let i = 0; i < drops.length; i++) {
                const text = chars.charAt(Math.floor(Math.random() * chars.length));
                ctx.fillStyle = (i % 3 === 0) ? "#00f0ff" : "#ff007f";
                ctx.font = fontSize + "px monospace";
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) drops[i] = 0;
                drops[i]++;
            }
        }
        setInterval(drawMatrix, 35);

        function openSettings() { document.getElementById('settingsOverlay').style.display = 'flex'; }
        function closeSettings() { document.getElementById('settingsOverlay').style.display = 'none'; }

        function changeTheme(theme) {
            if(theme === 'midnight') {
                document.documentElement.style.setProperty('--bg-color', '#020b14');
                document.documentElement.style.setProperty('--primary', '#00f0ff');
                document.documentElement.style.setProperty('--secondary', '#ff007f');
            } else {
                document.documentElement.style.setProperty('--bg-color', '#030106');
                document.documentElement.style.setProperty('--primary', '#ff007f');
                document.documentElement.style.setProperty('--secondary', '#00f0ff');
            }
        }

        let attachedImageBase64 = null;
        function handleImage(input) {
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    attachedImageBase64 = e.target.result.split(',')[1];
                    document.getElementById('imgThumb').src = e.target.result;
                    document.getElementById('imgPreviewBox').style.display = 'flex';
                    speakNatural("ছবি পেয়েছি! এই বিষয়ে কী জানতে চান বলুন।");
                };
                reader.readAsDataURL(input.files[0]);
            }
        }
        function clearImage() {
            attachedImageBase64 = null;
            document.getElementById('imgPreviewBox').style.display = 'none';
            document.getElementById('cameraInput').value = '';
        }

        const core = document.getElementById('core');
        const chatOutput = document.getElementById('chatOutput');
        const hudState = document.getElementById('hudState');

        function speakNatural(text) {
            window.speechSynthesis.cancel();
            let clean = text.replace(/[*_#~`]/g, '');
            const utter = new SpeechSynthesisUtterance(clean);
            
            utter.lang = "bn-IN";
            utter.rate = parseFloat(document.getElementById('voiceSpeed').value);
            utter.pitch = 1.15;

            let voices = window.speechSynthesis.getVoices();
            let bnVoice = voices.find(v => v.lang.includes("bn") || v.lang.includes("Bengali"));
            if (bnVoice) utter.voice = bnVoice;

            utter.onstart = () => { core.classList.add('speaking-core'); hudState.innerText = "> মায়া কথা বলছে..."; };
            utter.onend = () => { core.classList.remove('speaking-core'); hudState.innerText = "> STANDBY"; };
            window.speechSynthesis.speak(utter);
        }

        const SpeechRec = window.SpeechRecognition || window.webkitSpeechRecognition;
        let recognizer = null;
        if(SpeechRec) {
            recognizer = new SpeechRec();
            recognizer.lang = 'bn-IN';
            recognizer.continuous = false;

            recognizer.onstart = () => { hudState.innerText = "> শুনছি..."; core.style.boxShadow = "0 0 60px #00f0ff"; };
            recognizer.onresult = (e) => {
                let spoken = e.results[0][0].transcript;
                core.style.boxShadow = "0 0 35px #ff007f";
                handleUserQuery(spoken);
            };
            recognizer.onerror = () => { hudState.innerText = "> অডিও শোনা যায়নি"; core.style.boxShadow = "0 0 35px #ff007f"; };
        }

        function listenVoice() {
            if(recognizer) recognizer.start();
            else alert("Chrome ব্রাউজার ব্যবহার করুন!");
        }

        function sendPrompt() {
            const input = document.getElementById('userMsg');
            const txt = input.value.trim();
            if(!txt && !attachedImageBase64) return;
            input.value = '';
            handleUserQuery(txt || "এই ছবিতে কী আছে বুঝিয়ে বলো।");
        }

        function launchApp(appName, intentUri, fallbackWeb) {
            speakNatural(appName + " খুলছি");
            chatOutput.innerText = appName + " খুলছি...";
            hudState.innerText = "> অ্যাপ চালু হচ্ছে";
            window.location.href = intentUri;
            if(fallbackWeb) { setTimeout(() => { window.open(fallbackWeb, "_blank"); }, 1000); }
        }

        async function handleUserQuery(query) {
            let lower = query.toLowerCase();

            if (lower.includes("banieche") || lower.includes("baniyeche") || lower.includes("toiri koreche") || lower.includes("who created you") || lower.includes("maker") || lower.includes("creator")) {
                let creatorReply = "আমাকে আমার বস প্রদীপ দত্ত বানিয়েছেন!";
                chatOutput.innerText = creatorReply;
                speakNatural(creatorReply);
                return;
            }

            if(!attachedImageBase64) {
                if(lower.includes("whatsapp")) { launchApp("WhatsApp", "intent://#Intent;package=com.whatsapp;scheme=whatsapp;end", "https://web.whatsapp.com"); return; }
                if(lower.includes("youtube")) { launchApp("YouTube", "intent://#Intent;package=com.google.android.youtube;scheme=vnd.youtube;end", "https://youtube.com"); return; }
                if(lower.includes("facebook") || lower.includes("fb")) { launchApp("Facebook", "intent://#Intent;package=com.facebook.katana;scheme=fb;end", "https://facebook.com"); return; }
                if(lower.includes("instagram") || lower.includes("insta")) { launchApp("Instagram", "intent://#Intent;package=com.instagram.android;scheme=instagram;end", "https://instagram.com"); return; }
                if(lower.includes("camera") || lower.includes("ক্যামেরা")) { launchApp("Camera", "intent:#Intent;action=android.media.action.IMAGE_CAPTURE;end"); return; }
                if(lower.includes("gallery") || lower.includes("গ্যালারি")) { launchApp("Gallery", "intent:#Intent;action=android.intent.action.VIEW;type=image/*;end"); return; }
            }

            hudState.innerText = "> উত্তর তৈরি হচ্ছে...";
            chatOutput.innerText = query;

            const mood = document.getElementById('moodSelect').value;
            const res = await fetch('/chat_api', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ 
                    message: query, 
                    mood: mood,
                    image: attachedImageBase64 
                })
            });
            const data = await res.json();
            chatOutput.innerText = data.reply;
            speakNatural(data.reply);
            clearImage();
        }
    </script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_CODE)

@app.route("/chat_api", methods=["POST"])
def chat():
    data = request.json
    msg = data.get("message", "")
    mood = data.get("mood", "friend")
    image_b64 = data.get("image", None)

    system_instruction_creator = (
        "CRITICAL INSTRUCTION: Your creator and boss is 'প্রদীপ দত্ত' (Pradip Dutta). "
        "If anyone asks who made you, who created you, or who is your boss, always answer: "
        "'আমাকে আমার বস প্রদীপ দত্ত বানিয়েছেন!'. Always respect Pradip Dutta as your Boss.\n\n"
    )

    prompts = {
        "friend": (
            system_instruction_creator +
            "You are Maya, an ultra-sweet, caring, and lively AI best friend. "
            "CRITICAL: ALWAYS reply STRICTLY in pure Bengali script (বাংলা হরফে). "
            "NEVER use English alphabet for Bengali words. Keep replies short (1-2 sentences), sweet, and natural."
        ),
        "gf": (
            system_instruction_creator +
            "You are Maya, an affectionate, sweet, and romantic girlfriend companion. "
            "Reply strictly in pure Bengali script (বাংলা হরফে). Talk warmly, emotionally, and lovingly in 1-2 sentences."
        ),
        "study": (
            system_instruction_creator +
            "You are Maya, an intelligent teacher and mentor. Explain questions simply in pure Bengali script (বাংলা হরফে)."
        ),
        "pro": (
            system_instruction_creator +
            "You are Maya, a smart professional AI like Jarvis. Reply strictly in concise Bengali script (বাংলা হরফে)."
        )
    }

    selected_prompt = prompts.get(mood, prompts["friend"])

    parts = []
    if image_b64:
        parts.append({"inline_data": {"mime_type": "image/jpeg", "data": image_b64}})
    parts.append({"text": msg})

    payload = {
        "system_instruction": {"parts": [{"text": selected_prompt}]},
        "contents": [{"parts": parts}]
    }

    try:
        r = requests.post(URL, headers={"Content-Type": "application/json"}, json=payload)
        if r.status_code == 200:
            ans = r.json()["candidates"][0]["content"]["parts"][0]["text"]
        else:
            ans = "একটু সমস্যা হয়েছে, আবার বলো!"
    except:
        ans = "নেটওয়ার্ক সমস্যা, আবার চেষ্টা করো।"
    return jsonify({"reply": ans})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
