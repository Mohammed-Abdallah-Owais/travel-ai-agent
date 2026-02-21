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

# -------- Tools (uses AI for ANY country in the world) --------

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

# -------- Query Function --------
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
<html>
<head>
    <title>Travel AI Agent</title>
    <meta charset="utf-8">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; font-family: Segoe UI, sans-serif; }
        body { background: #0f0f1a; color: #e2e8f0; min-height: 100vh; }
        .header { background: linear-gradient(135deg, #7c3aed, #2563eb); padding: 25px; text-align: center; }
        .header h1 { font-size: 2em; color: white; }
        .header p { color: #ddd; margin-top: 5px; }
        .container { max-width: 800px; margin: 30px auto; padding: 0 20px; }
        .examples { display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 25px; }
        .examples button {
            background: #1e293b; color: #a78bfa;
            border: 1px solid #334155; padding: 8px 14px;
            border-radius: 20px; cursor: pointer; font-size: 13px;
        }
        .examples button:hover { background: #334155; }
        .chat-box {
            background: #111827; border: 1px solid #1e293b;
            border-radius: 15px; padding: 20px;
            min-height: 400px; max-height: 500px;
            overflow-y: auto; margin-bottom: 20px;
        }
        .msg-user {
            background: linear-gradient(135deg, #7c3aed, #4f46e5);
            color: white; padding: 12px 16px;
            border-radius: 15px 15px 3px 15px;
            margin: 10px 0; margin-left: 20%; font-size: 14px;
        }
        .msg-bot {
            background: #1e293b; color: #e2e8f0;
            padding: 12px 16px; border-radius: 15px 15px 15px 3px;
            margin: 10px 0; margin-right: 20%; font-size: 14px;
            white-space: pre-wrap; line-height: 1.6;
        }
        .thinking {
            background: #0f172a; color: #94a3b8;
            padding: 10px 14px; border-radius: 8px;
            font-size: 12px; margin-bottom: 10px;
            border-left: 3px solid #7c3aed;
            white-space: pre-wrap;
        }
        .answer { color: #34d399; font-weight: bold; font-size: 15px; }
        .input-area { display: flex; gap: 10px; }
        .input-area input {
            flex: 1; background: #1e293b; color: white;
            border: 1px solid #7c3aed; border-radius: 10px;
            padding: 12px 16px; font-size: 15px; outline: none;
        }
        .input-area input::placeholder { color: #64748b; }
        .input-area button {
            background: linear-gradient(135deg, #7c3aed, #2563eb);
            color: white; border: none; border-radius: 10px;
            padding: 12px 24px; font-size: 15px;
            font-weight: bold; cursor: pointer;
        }
        .input-area button:hover { opacity: 0.85; }
        .loading { color: #a78bfa; font-style: italic; padding: 10px; }
        .label { color: #a78bfa; font-weight: bold; margin-bottom: 10px; font-size: 14px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Travel AI Agent</h1>
        <p>Your smart travel assistant - ask anything about any destination!</p>
    </div>
    <div class="container">
        <div class="label">Try these examples:</div>
        <div class="examples">
            <button onclick="ask('Tell me about Italy')">Italy</button>
            <button onclick="ask('Tell me about Brazil')">Brazil</button>
            <button onclick="ask('Tell me about South Korea')">South Korea</button>
            <button onclick="ask('Tell me about Morocco')">Morocco</button>
            <button onclick="ask('Tell me about Argentina')">Argentina</button>
            <button onclick="ask('Tell me about Egypt')">Egypt</button>
        </div>
        <div class="chat-box" id="chat"></div>
        <div class="input-area">
            <input type="text" id="userInput"
                   placeholder="Ask me about any country in the world..."
                   onkeypress="if(event.key==='Enter') sendMessage()">
            <button onclick="sendMessage()">Send</button>
        </div>
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

            chat.innerHTML += '<div class="msg-user">' + question + '</div>';
            input.value = '';
            chat.innerHTML += '<div class="loading" id="loading">Agent is thinking...</div>';
            chat.scrollTop = chat.scrollHeight;

            fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({question: question})
            })
            .then(r => r.json())
            .then(data => {
                document.getElementById('loading').remove();
                chat.innerHTML += '<div class="msg-bot"><div class="thinking">' +
                    data.thinking + '</div><div class="answer">Answer: ' +
                    data.answer + '</div></div>';
                chat.scrollTop = chat.scrollHeight;
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

print("Server running at http://localhost:8080")
print("Open your browser and go to: http://localhost:8080")
HTTPServer(('localhost', 8080), Handler).serve_forever()