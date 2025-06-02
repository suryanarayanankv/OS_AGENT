# 💻 Cross-Platform OS Agent with Persistent Memory (Web UI)

This project implements a powerful **AI-driven OS Agent** that can interact with your operating system (Linux or Windows) through natural language commands via a **web-based terminal interface**. It leverages **Google's Gemini 1.5 Flash model** for understanding and executing tasks and features **persistent memory** to learn from past interactions.

> ⚠️ **Important:** Please navigate to the `osagent-v3/` directory before installing or running the project. Earlier versions (`os_agent.py`, `os_agent-v2.py`) include browser automation logic and require additional setup which is not part of this streamlined demo.

---

## ✨ Features

- **Natural Language OS Control**  
  Issue commands like:  
  `"list files in my home directory"`,  
  `"create a new folder named 'my_project'"`, or  
  `"show me running processes"`.

- **Cross-Platform Compatibility**  
  Designed to work on both **Linux** and **Windows**.

- **Persistent Memory**  
  Learns and remembers system facts, command usage patterns, and conversation history **across sessions**.

- **Web-Based Terminal Interface**  
  Interact with the agent through a **user-friendly terminal emulation** in your browser.

- **Command Confirmation**  
  Prompts for **explicit confirmation** before executing sensitive commands (e.g., deleting files).

- **Real-time Feedback**  
  Immediate feedback on command success/failure along with command output.

- **System Monitoring**  
  Query system status, list running processes, and view agent memory statistics.

---

## 📁 Project Structure

```
osagent-v3/
├── os_agent.py              # Core OS agent logic
├── app.py                   # FastAPI backend
├── .env                     # Your Gemini API key (you will create this)
├── requirements.txt         # Python dependencies
├── agent_memory/            # Stores persistent memory and logs
└── frontend/
    ├── index.html           # Web terminal UI
    ├── script.js            # Frontend logic
    └── style.css            # Terminal styling
```

---

## 🚀 Setup and Installation

### 📌 Prerequisites

- Python 3.8+
- `pip` (Python package installer)
- An active Google Cloud project with Gemini API enabled  
  (you’ll need your `GEMINI_API_KEY`)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd osagent-v3
```

---

### 2. Set Up Your Gemini API Key

Create a `.env` file in the `osagent-v3/` directory:

```env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

> ⚠️ **Important:** Replace with your actual Gemini API key. Keep this file private and **never commit it** to a public repository.

---

### 3. Install Python Dependencies

Create or confirm `requirements.txt` includes the following:

```txt
fastapi
uvicorn
python-dotenv
google-generativeai
psutil
```

Then install:

```bash
pip install -r requirements.txt
```

---

### 4. Run the FastAPI Application

From inside the `osagent-v3` folder, run:

```bash
uvicorn app:app --reload
```

- `app:app` → Refers to the `app` object in `app.py`
- `--reload` → Auto-reloads the server when code changes (dev mode)

You should see output showing:

```
http://127.0.0.1:8000
```

---

## 🌐 Usage

Open your browser and go to `http://127.0.0.1:8000`

You’ll see a terminal-style web interface. Type commands and press `Enter`.

---

### 🧪 Example Commands to Try

- `list files in current directory`
- `create a folder named 'test_agent_dir'`
- `show me running processes`
- `what is my current operating system?`

---

### 🧩 Frontend-only Commands

- `status` → Show system status  
- `processes` → List running processes  
- `memory_stats` → Show agent memory info  
- `help` → List available commands  
- `clear` → Clear the terminal screen  
- `quit` → Disable terminal input

---

### 🔐 Command Confirmation

For potentially destructive commands, the agent will ask for confirmation:

```bash
Are you sure you want to delete 'important.txt'? (yes/no)
```

---

## 🧠 Memory and Persistence

The agent stores memory in the `agent_memory/` directory:

- `agent_memory.db` → SQLite database (conversations, facts, logs)
- `quick_memory.json` → JSON file for fast access to frequently used data

This enables contextual, intelligent responses over time.

---

## 🤝 Contributing

Contributions are welcome!  
Feel free to **fork the repository**, **open issues**, or **submit pull requests**.

---

## 📄 License

This project is open-source and available under the **MIT License**.
