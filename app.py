import re
import os
from dotenv import load_dotenv
from groq import Groq
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class Agent:
    def __init__(self, system=""):
        self.system = system
        self.messages = []
        if self.system:
            self.messages.append({"role": "system", "content": system})

    def __call__(self, message):
        self.messages.append({"role": "user", "content": message})
        result = self.execute()
        self.messages.append({"role": "assistant", "content": result})
        return result

    def execute(self):
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            temperature=0,
            messages=self.messages
        )
        return completion.choices[0].message.content

prompt = """

You were created by ENG Mohammed Abdallah Owais.
If anyone asks who made you or who created you, always answer:
"I was created by ENG Mohammed Abdallah Owais."

You run in a loop of Thought, Action, PAUSE, Observation.
At the end of the loop you output an Answer.
Use Thought to describe your thoughts about the question you have been asked.
Use Action to run one of the actions available to you - then return PAUSE.
Observation will be the result of running those actions.

Your available actions are:

get_best_time_to_visit:
e.g. get_best_time_to_visit: Japan
Returns the best time of year to visit that country

get_temperature:
e.g. get_temperature: Paris
Returns the typical temperature of a city

get_currency:
e.g. get_currency: Japan
Returns the currency used in that country

get_language:
e.g. get_language: Brazil
Returns the language spoken in that country

get_famous_food:
e.g. get_famous_food: Italy
Returns the most famous food in that country

Example session:
Question: Tell me about Japan
Thought: I need to get temperature, currency, language and food for Japan
Action: get_temperature: Japan
PAUSE
Observation: Japan is cold in winter around 5C and hot in summer around 30C
Answer: Japan has cold winters and hot summers...
""".strip()

def get_best_time_to_visit(country):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content":
            f"What is the best time of year to visit {country}? Answer in one short sentence only."}]
    )
    return completion.choices[0].message.content

def get_temperature(city):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content":
            f"What is the typical temperature in {city}? Answer in one short sentence only."}]
    )
    return completion.choices[0].message.content

def get_currency(country):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content":
            f"What currency is used in {country}? Answer in one short sentence only."}]
    )
    return completion.choices[0].message.content

def get_language(country):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content":
            f"What language do people speak in {country}? Answer in one short sentence only."}]
    )
    return completion.choices[0].message.content

def get_famous_food(country):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content":
            f"What is the most famous food in {country}? Answer in one short sentence only."}]
    )
    return completion.choices[0].message.content

known_actions = {
    "get_temperature": get_temperature,
    "get_currency": get_currency,
    "get_language": get_language,
    "get_famous_food": get_famous_food,
    "get_best_time_to_visit": get_best_time_to_visit
}

action_re = re.compile('^Action: (\w+): (.*)$')

def query(question, max_turns=10):
    i = 0
    bot = Agent(prompt)
    next_prompt = question
    thinking_log = []

    while i < max_turns:
        i += 1
        result = bot(next_prompt)
        actions = [
            action_re.match(a)
            for a in result.split('\n')
            if action_re.match(a)
        ]
        if actions:
            action, action_input = actions[0].groups()
            if action not in known_actions:
                raise Exception("Unknown action: {}".format(action))
            observation = known_actions[action](action_input)
            thinking_log.append("Action: {} -> {}".format(action, action_input))
            thinking_log.append("Observation: {}".format(observation))
            next_prompt = "Observation: {}".format(observation)
        else:
            for line in result.split('\n'):
                if line.startswith("Answer:"):
                    final_answer = line.replace("Answer:", "").strip()
                    return final_answer, "\n".join(thinking_log)
            return result, "\n".join(thinking_log)

    return "I could not find an answer.", "\n".join(thinking_log)


HTML = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travel AI Agent</title>
    <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg:       #050810;
            --surface:  #0c1120;
            --surface2: #111827;
            --surface3: #1a2438;
            --border:   #1e2d45;
            --border2:  #263548;
            --teal:     #14b8a6;
            --teal2:    #0d9488;
            --amber:    #f59e0b;
            --amber2:   #d97706;
            --rose:     #f43f5e;
            --blue:     #3b82f6;
            --text:     #e2eaf6;
            --muted:    #4a6080;
            --muted2:   #64748b;
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            background: var(--bg);
            color: var(--text);
            font-family: 'DM Sans', sans-serif;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        /* Animated background */
        body::before {
            content: '';
            position: fixed;
            inset: 0;
            background:
                radial-gradient(ellipse 80% 50% at 20% 10%, rgba(20,184,166,0.07) 0%, transparent 60%),
                radial-gradient(ellipse 60% 40% at 80% 80%, rgba(245,158,11,0.05) 0%, transparent 50%),
                radial-gradient(ellipse 40% 60% at 50% 50%, rgba(59,130,246,0.04) 0%, transparent 60%);
            pointer-events: none;
            z-index: 0;
        }

        body::after {
            content: '';
            position: fixed;
            inset: 0;
            background-image:
                linear-gradient(rgba(20,184,166,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(20,184,166,0.03) 1px, transparent 1px);
            background-size: 44px 44px;
            pointer-events: none;
            z-index: 0;
        }

        /* ===== HEADER ===== */
        .header {
            position: relative;
            z-index: 1;
            padding: 40px 24px 32px;
            text-align: center;
            border-bottom: 1px solid var(--border);
            background: linear-gradient(180deg, rgba(20,184,166,0.06) 0%, transparent 100%);
        }

        .header-badge {
            display: inline-flex;
            align-items: center;
            gap: 7px;
            background: rgba(20,184,166,0.1);
            border: 1px solid rgba(20,184,166,0.25);
            color: var(--teal);
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            padding: 5px 14px;
            border-radius: 20px;
            margin-bottom: 18px;
        }

        .header-badge::before {
            content: '';
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--teal);
            animation: blink 2s ease infinite;
        }

        @keyframes blink {
            0%, 100% { opacity: 1; }
            50% { opacity: 0.2; }
        }

        .header h1 {
            font-family: 'Playfair Display', serif;
            font-size: 3em;
            font-weight: 800;
            color: #fff;
            line-height: 1.1;
            margin-bottom: 10px;
        }

        .header h1 span {
            background: linear-gradient(135deg, var(--teal), var(--amber));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .header p {
            color: var(--muted2);
            font-size: 14px;
            font-weight: 400;
        }

        /* ===== MAIN LAYOUT ===== */
        .main {
            flex: 1;
            display: flex;
            flex-direction: column;
            max-width: 820px;
            width: 100%;
            margin: 0 auto;
            padding: 28px 20px 20px;
            position: relative;
            z-index: 1;
            gap: 20px;
        }

        /* ===== EXAMPLE PILLS ===== */
        .examples-label {
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--muted);
            margin-bottom: 10px;
        }

        .examples {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .examples button {
            background: var(--surface2);
            color: var(--teal);
            border: 1px solid var(--border2);
            padding: 7px 16px;
            border-radius: 20px;
            cursor: pointer;
            font-size: 13px;
            font-family: 'DM Sans', sans-serif;
            font-weight: 500;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .examples button:hover {
            background: rgba(20,184,166,0.12);
            border-color: rgba(20,184,166,0.4);
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(20,184,166,0.15);
        }

        /* ===== CHAT BOX ===== */
        .chat-box {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 24px;
            min-height: 420px;
            max-height: 480px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 16px;
            scroll-behavior: smooth;
        }

        .chat-box::-webkit-scrollbar { width: 4px; }
        .chat-box::-webkit-scrollbar-track { background: transparent; }
        .chat-box::-webkit-scrollbar-thumb { background: var(--border2); border-radius: 4px; }

        /* Empty state */
        .empty-state {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 12px;
            color: var(--muted);
            padding: 40px;
            text-align: center;
        }

        .empty-icon {
            font-size: 3em;
            filter: grayscale(0.3);
        }

        .empty-state p {
            font-size: 14px;
            line-height: 1.6;
            max-width: 260px;
        }

        /* User message */
        .msg-user {
            align-self: flex-end;
            background: linear-gradient(135deg, var(--teal2), #0e7490);
            color: white;
            padding: 12px 18px;
            border-radius: 18px 18px 4px 18px;
            max-width: 75%;
            font-size: 14px;
            line-height: 1.6;
            box-shadow: 0 4px 16px rgba(20,184,166,0.2);
            animation: slideRight 0.3s cubic-bezier(.16,1,.3,1);
        }

        @keyframes slideRight {
            from { opacity: 0; transform: translateX(20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        /* Bot message */
        .msg-bot {
            align-self: flex-start;
            max-width: 85%;
            animation: slideLeft 0.3s cubic-bezier(.16,1,.3,1);
        }

        @keyframes slideLeft {
            from { opacity: 0; transform: translateX(-20px); }
            to { opacity: 1; transform: translateX(0); }
        }

        /* Thinking block */
        .thinking {
            background: var(--surface3);
            border: 1px solid var(--border);
            border-left: 3px solid var(--amber);
            border-radius: 10px;
            padding: 12px 14px;
            font-size: 12px;
            color: var(--muted2);
            white-space: pre-wrap;
            line-height: 1.8;
            margin-bottom: 10px;
            font-family: 'DM Sans', sans-serif;
        }

        .thinking-label {
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--amber);
            margin-bottom: 6px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .thinking-label::before {
            content: '';
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: var(--amber);
        }

        /* Answer block */
        .answer-block {
            background: var(--surface2);
            border: 1px solid var(--border2);
            border-radius: 14px;
            padding: 16px 18px;
        }

        .answer-label {
            font-size: 10px;
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
            color: var(--teal);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .answer-label::before {
            content: '';
            width: 5px;
            height: 5px;
            border-radius: 50%;
            background: var(--teal);
        }

        .answer-text {
            font-size: 14px;
            color: var(--text);
            line-height: 1.7;
        }

        /* Loading */
        .loading {
            align-self: flex-start;
            display: flex;
            align-items: center;
            gap: 10px;
            background: var(--surface2);
            border: 1px solid var(--border);
            border-radius: 14px;
            padding: 14px 18px;
            font-size: 13px;
            color: var(--muted2);
        }

        .dots {
            display: flex;
            gap: 4px;
        }

        .dots span {
            width: 6px;
            height: 6px;
            border-radius: 50%;
            background: var(--teal);
            animation: bounce 1.2s ease infinite;
        }

        .dots span:nth-child(2) { animation-delay: 0.2s; }
        .dots span:nth-child(3) { animation-delay: 0.4s; }

        @keyframes bounce {
            0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; }
            40% { transform: scale(1); opacity: 1; }
        }

        /* ===== INPUT AREA ===== */
        .input-wrapper {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 6px 6px 6px 18px;
            display: flex;
            align-items: center;
            gap: 8px;
            transition: border-color 0.2s, box-shadow 0.2s;
        }

        .input-wrapper:focus-within {
            border-color: rgba(20,184,166,0.5);
            box-shadow: 0 0 0 3px rgba(20,184,166,0.08);
        }

        .input-wrapper input {
            flex: 1;
            background: transparent;
            color: var(--text);
            border: none;
            outline: none;
            font-size: 15px;
            font-family: 'DM Sans', sans-serif;
            padding: 10px 0;
        }

        .input-wrapper input::placeholder {
            color: var(--muted);
        }

        .send-btn {
            background: linear-gradient(135deg, var(--teal), var(--teal2));
            color: white;
            border: none;
            border-radius: 12px;
            padding: 12px 22px;
            font-size: 14px;
            font-weight: 600;
            font-family: 'DM Sans', sans-serif;
            cursor: pointer;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 7px;
            white-space: nowrap;
        }

        .send-btn:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 20px rgba(20,184,166,0.3);
        }

        .send-btn:active {
            transform: translateY(0);
        }

        /* Arrow icon */
        .send-btn::after {
            content: '';
            width: 0;
            height: 0;
            border-top: 5px solid transparent;
            border-bottom: 5px solid transparent;
            border-left: 7px solid white;
        }

        /* ===== FOOTER ===== */
        .footer {
            position: relative;
            z-index: 1;
            text-align: center;
            padding: 16px;
            font-size: 12px;
            color: var(--muted);
            border-top: 1px solid var(--border);
        }

        .footer span {
            color: var(--teal);
        }

        /* Animations */
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .header { animation: fadeIn 0.5s ease both; }
        .main { animation: fadeIn 0.5s ease 0.1s both; }
    </style>
</head>
<body>

    <!-- Header -->
    <div class="header">
        <div class="header-badge">AI Powered Travel Assistant</div>
        <h1>Explore the <span>World</span></h1>
        <p>Ask anything about any destination — powered by AI</p>
    </div>

    <!-- Main -->
    <div class="main">

        <!-- Examples -->
        <div>
            <div class="examples-label">Quick Destinations</div>
            <div class="examples">
                <button onclick="ask('Tell me about Italy')">Italy</button>
                <button onclick="ask('Tell me about Japan')">Japan</button>
                <button onclick="ask('Tell me about Brazil')">Brazil</button>
                <button onclick="ask('Tell me about Morocco')">Morocco</button>
                <button onclick="ask('Tell me about South Korea')">South Korea</button>
                <button onclick="ask('Tell me about Egypt')">Egypt</button>
                <button onclick="ask('Tell me about Argentina')">Argentina</button>
                <button onclick="ask('Tell me about Dubai')">Dubai</button>
            </div>
        </div>

        <!-- Chat Box -->
        <div class="chat-box" id="chat">
            <div class="empty-state" id="emptyState">
                <div class="empty-icon">✈️</div>
                <p>Ask me about any country in the world — temperature, currency, language, food and more!</p>
            </div>
        </div>

        <!-- Input -->
        <div class="input-wrapper">
            <input
                type="text"
                id="userInput"
                placeholder="Ask about any country... e.g. Tell me about Thailand"
                onkeypress="if(event.key==='Enter') sendMessage()"
                autocomplete="off"
            >
            <button class="send-btn" onclick="sendMessage()">Send</button>
        </div>

    </div>

    <!-- Footer -->
    <div class="footer">
        Powered by <span>Groq</span> & <span>LLaMA 3.3</span> — Free & Open Source
    </div>

    <script>
        function ask(question) {
            document.getElementById('userInput').value = question;
            sendMessage();
        }

        function sendMessage() {
            const input = document.getElementById('userInput');
            const chat = document.getElementById('chat');
            const question = input.value.trim();
            if (!question) return;

            // Remove empty state
            const empty = document.getElementById('emptyState');
            if (empty) empty.remove();

            // User message
            const userDiv = document.createElement('div');
            userDiv.className = 'msg-user';
            userDiv.textContent = question;
            chat.appendChild(userDiv);
            input.value = '';

            // Loading indicator
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'loading';
            loadingDiv.id = 'loading';
            loadingDiv.innerHTML = '<div class="dots"><span></span><span></span><span></span></div> Agent is thinking...';
            chat.appendChild(loadingDiv);
            chat.scrollTop = chat.scrollHeight;

            fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: question})
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('loading').remove();

                const botDiv = document.createElement('div');
                botDiv.className = 'msg-bot';

                let html = '';

                if (data.thinking) {
                    html += '<div class="thinking">';
                    html += '<div class="thinking-label">Agent Thinking</div>';
                    html += data.thinking.replace(/</g, '&lt;').replace(/>/g, '&gt;');
                    html += '</div>';
                }

                html += '<div class="answer-block">';
                html += '<div class="answer-label">Answer</div>';
                html += '<div class="answer-text">' + data.answer.replace(/</g, '&lt;').replace(/>/g, '&gt;') + '</div>';
                html += '</div>';

                botDiv.innerHTML = html;
                chat.appendChild(botDiv);
                chat.scrollTop = chat.scrollHeight;
            })
            .catch(() => {
                document.getElementById('loading').remove();
                const errDiv = document.createElement('div');
                errDiv.className = 'msg-bot';
                errDiv.innerHTML = '<div class="answer-block"><div class="answer-label">Error</div><div class="answer-text">Something went wrong. Please try again.</div></div>';
                chat.appendChild(errDiv);
            });
        }
    </script>
</body>
</html>"""

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(HTML.encode('utf-8'))

    def do_POST(self):
        length = int(self.headers['Content-Length'])
        body = json.loads(self.rfile.read(length))
        question = body.get('question', '')
        answer, thinking = query(question)
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps({
            "answer": answer,
            "thinking": thinking
        }).encode('utf-8'))

    def log_message(self, format, *args):
        pass

# print("Server running at http://localhost:8080")
# print("Open your browser and go to: http://localhost:8080")
port = int(os.environ.get('PORT', 8080))
HTTPServer(('0.0.0.0', port), Handler).serve_forever()
# HTTPServer(('localhost', 8080), Handler).serve_forever()