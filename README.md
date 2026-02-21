# 🌍 Travel AI Agent

A smart AI-powered travel assistant built with Python and Groq. Ask anything about any country in the world — temperature, currency, language, and famous food — and the agent will think, search, and answer step by step.

---

## 🤖 What is this?

This project is a **ReAct AI Agent** (Reasoning + Acting). Instead of just answering from memory, the agent:

1. **Thinks** about the question
2. **Calls tools** to gather information
3. **Observes** the results
4. **Answers** with a complete response

All of this runs in a loop until the agent finds a satisfying answer.

---

## ✨ Features

- Ask about **any country in the world**
- Agent thinks step by step (you can see its thinking process)
- Dark modern web interface in the browser
- Completely **free** using Groq API
- No frameworks needed — pure Python web server

---

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.11 | Main language |
| Groq API | Free AI model (llama-3.3-70b) |
| python-dotenv | Load API key securely |
| HTTP Server | Built-in Python web server |
| HTML/CSS/JS | Frontend chat interface |

---

## 📁 Project Structure

```
dog-agent/
│
├── app.py          ← Main application (agent + web server)
├── .env            ← Your secret API key (never share this!)
├── .gitignore      ← Tells Git to ignore .env file
└── README.md       ← This file
```

---

## 🚀 Getting Started

### Step 1: Clone the repository

```bash
git clone https://github.com/Mohammed-Abdallah-Owais/travel-ai-agent.git

```

### Step 2: Install Python 3.11

Download from [python.org](https://python.org) and install.

### Step 3: Install required libraries

```bash
pip install groq python-dotenv
```

### Step 4: Get a free Groq API key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign up for free
3. Go to **API Keys** and create a new key

### Step 5: Create your `.env` file

Create a file called `.env` in the project folder:

```
GROQ_API_KEY=your_api_key_here
```

### Step 6: Run the app

```bash
python app.py
```

### Step 7: Open your browser

```
http://localhost:8080
```

---

## 💬 How to Use

Type any question about a destination, for example:

- `"Tell me about Japan"`
- `"What is the currency in Brazil?"`
- `"What food should I try in Italy?"`
- `"Tell me everything about Egypt"`

The agent will think through the question, call the right tools, and give you a full answer.

---

## 🧠 How the Agent Works

The agent follows the **ReAct loop**:

```
User Question
      ↓
   THOUGHT  →  Agent thinks about what it needs
      ↓
   ACTION   →  Agent calls a tool
      ↓
   PAUSE    →  Waits for result
      ↓
OBSERVATION →  Gets the result back
      ↓
  (loop repeats until...)
      ↓
   ANSWER   →  Final response to user
```

---

## 🔧 Available Tools

| Tool | What it does |
|------|-------------|
| `get_temperature` | Returns typical temperature of a city |
| `get_currency` | Returns the currency used in a country |
| `get_language` | Returns the language spoken in a country |
| `get_famous_food` | Returns the most famous food in a country |

---

## ➕ How to Add a New Tool

You need to change **3 places** in `app.py`:

**1. Add to the prompt** — tell the AI the tool exists:
```python
get_best_time_to_visit:
e.g. get_best_time_to_visit: Japan
Returns the best time of year to visit that country
```

**2. Write the Python function:**
```python
def get_best_time_to_visit(country):
    completion = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        temperature=0,
        messages=[{"role": "user", "content":
            f"What is the best time to visit {country}? One sentence only."}]
    )
    return completion.choices[0].message.content
```

**3. Register in `known_actions`:**
```python
known_actions = {
    "get_temperature": get_temperature,
    "get_currency": get_currency,
    "get_language": get_language,
    "get_famous_food": get_famous_food,
    "get_best_time_to_visit": get_best_time_to_visit  # new!
}
```



## 🆓 Cost

This project is **completely free** to run using the Groq free tier. No credit card required.

---

## 👨‍💻 Author

Built with Python and Groq by **Eng Mohammed Abdallah Owais**

---

## 📜 License

This project is open source and available under the [MIT License](LICENSE).
