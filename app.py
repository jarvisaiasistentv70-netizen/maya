import os
from flask import Flask, render_template_string, request, jsonify
import requests

app = Flask(__name__)

# তোমার আসল জেমিনি এপিআই কি এখানে সরাসরি সেট করা আছে
API_KEY = "AIzaSyDBfvwcPpaitEai2nqS7_6mJx5TBTujoBs"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={API_KEY}"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>MAYA AI ASSISTANT</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
        :root {
            --bg-color: #030106;
            --primary: #ff007f;
            --secondary: #00ffff;
            --text-color: #ffffff;
            --glass-bg: rgba(20, 10, 30, 0.75);
        }
        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            overflow: hidden;
            position: relative;
        }
        body::before {
            content: "MAYA 010110 AI 10101 CYBERPUNK 11001 ASSISTANT 01010";
            position: absolute;
            top: 0; left: 0; width: 100%; height: 100%;
            color: rgba(255, 0, 127, 0.03);
            font-size: 14px;
            word-break: break-all;
            z-index: -1;
            padding: 10px;
            pointer-events: none;
        }
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 15px 20px;
            background: var(--glass-bg);
            border-bottom: 1px solid var(--primary);
            box-shadow: 0 0 15px rgba(255, 0, 127, 0.3);
        }
        h1 {
            font-size: 24px;
            letter-spacing: 3px;
            color: var(--primary);
            text-shadow: 0 0 10px var(--primary);
        }
        .mode-selector {
            background: rgba(0, 0, 0, 0.5);
            border: 1px solid var(--primary);
            color: var(--primary);
            padding: 5px 10px;
            border-radius: 20px;
            outline: none;
            font-weight: bold;
        }
        .chat-container {
            flex: 1;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            position: relative;
        }
        .core-glow {
            width: 180px;
            height: 180px;
            border-radius: 50%;
            background: radial-gradient(circle, var(--primary) 0%, rgba(255,0,127,0.2) 60%, transparent 100%);
            box-shadow: 0 0 40px var(--primary), inset 0 0 20px var(--secondary);
            display: flex;
            justify-content: center;
            align-items: center;
            animation: pulse 3s infinite alternate;
        }
        .core-inner {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            border: 2px dashed var(--secondary);
            animation: rotate 10s linear infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.9); box-shadow: 0 0 20px var(--primary); }
            100% { transform: scale(1.1); box-shadow: 0 0 50px var(--primary), 0 0 20px var(--secondary); }
        }
        @keyframes rotate {
            100% { transform: rotate(360deg); }
        }
        .response-box {
            position: absolute;
            bottom: 20px;
            width: 90%;
            max-width: 600px;
            background: var(--glass-bg);
            border: 1px solid var(--primary);
            border-radius: 12px;
            padding: 15px;
            box-shadow: 0 0 15px rgba(255, 0, 127, 0.2);
            backdrop-filter: blur(5px);
        }
        .response-title {
            font-size: 11px;
            color: var(--secondary);
            margin-bottom: 5px;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .response-text {
            font-size: 15px;
            line-height: 1.4;
            color: #fff;
            min-height: 40px;
            max-height: 120px;
            overflow-y: auto;
        }
        .input-area {
            display: flex;
            padding: 15px 20px;
            background: var(--glass-bg);
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            gap: 10px;
        }
        .input-box {
            flex: 1;
            background: rgba(0, 0, 0, 0.6);
            border: 1px solid var(--primary);
            border-radius: 30px;
            padding: 12px 20px;
            color: #fff;
            outline: none;
            font-size: 16px;
        }
        .input-box:focus {
            box-shadow: 0 0 10px var(--primary);
        }
        .send-btn, .mic-btn {
            background: var(--primary);
            border: none;
            width: 45px;
            height: 45px;
            border-radius: 50%;
            color: white;
            font-size: 18px;
            cursor: pointer;
            display: flex;
            justify-content: center;
            align-items: center;
            box-shadow: 0 0 10px var(--primary);
            transition: 0.2s;
        }
        .send-btn:active, .mic-btn:active {
            transform: scale(0.9);
        }
    </style>
</head>
<body>

    <header>
        <h1>M A Y A</h1>
        <select class="mode-selector" id="personality">
            <option value="Best Friend">💖 Best Friend</option>
            <option value="Cyberpunk Hacker">⚡ Cyber Hacker</option>
            <option value="Wise Mentor">🦉 Wise Mentor</option>
        </select>
    </header>

    <div class="chat-container">
        <div class="core-glow">
            <div class="core-inner"></div>
        </div>

        <div class="response-box">
            <div class="response-title">> maya কথা বলছে...</div>
            <div class="response-text" id="responseText">হ্যালো! আমি মায়া, আপনার এআই অ্যাসিস্ট্যান্ট। আমাকে কিছু জিজ্ঞেস করুন।</div>
        </div>
    </div>

    <div class="input-area">
        <input type="text" class="input-box" id="userInput" placeholder="tumi kemon acho likhun..." autocomplete="off">
        <button class="send-btn" id="sendBtn">➤</button>
        <button class="mic-btn" id="micBtn">🎙️</button>
    </div>

    <script>
        const sendBtn = document.getElementById('sendBtn');
        const userInput = document.getElementById('userInput');
        const responseText = document.getElementById('responseText');
        const personalitySelect = document.getElementById('personality');
        const micBtn = document.getElementById('micBtn');

        async function sendMessage() {
            const text = userInput.value.trim();
            const personality = personalitySelect.value;
            if(!text) return;

            responseText.innerText = "প্রসেস হচ্ছে...";
            userInput.value = "";

            try {
                const res = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message: text, personality: personality })
                });
                const data = await res.json();
                if(data.reply) {
                    responseText.innerText = data.reply;
                    speak(data.reply);
                } else {
                    responseText.innerText = "একটি সমস্যা হয়েছে, আবার বলো!";
                }
            } catch(err) {
                responseText.innerText = "সার্ভারে সংযোগ স্থাপন করা যায়নি!";
            }
        }

        sendBtn.addEventListener('click', sendMessage);
        userInput.addEventListener('keypress', function(e) {
            if(e.key === 'Enter') sendMessage();
        });

        function speak(text) {
            if ('speechSynthesis' in window) {
                window.speechSynthesis.cancel();
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = 'bn-BD';
                window.speechSynthesis.speak(utterance);
            }
        }

        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (SpeechRecognition) {
            const recognition = new SpeechRecognition();
            recognition.lang = 'bn-BD';
            micBtn.addEventListener('click', () => {
                recognition.start();
                responseText.innerText = "শুনছি... বলুন...";
            });
            recognition.onresult = (e) => {
                userInput.value = e.results[0][0].transcript;
                sendMessage();
            };
        } else {
            micBtn.style.display = 'none';
        }
    </script>

</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        personality = data.get('personality', 'Best Friend')

        prompt = f"You are Maya, an advanced AI assistant. Your personality mode is: {personality}. Reply to the user naturally in Bengali or English based on their query. User says: {user_message}"

        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }

        response = requests.post(URL, json=payload)
        res_data = response.json()

        reply = res_data['candidates'][0]['content']['parts'][0]['text']
        return jsonify({"reply": reply})
    except Exception as e:
        return jsonify({"reply": "একটু সমস্যা হয়েছে, আবার বলো!"})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
