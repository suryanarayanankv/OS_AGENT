# 🧠 OS_AGENT – AI That Controls Your Operating System

**OS_AGENT** is an **AI-powered cross-platform agent** with **complete access to your operating system**, allowing it to understand and execute **natural language instructions**. It's not just a chatbot — it's an intelligent operating system companion capable of **controlling files, processes, applications, and environments** in real-time through a **web-based terminal interface**.

Built using **Gemini 1.5 Flash**, FastAPI, and a sleek web UI, it remembers your interactions with **persistent memory**, offering an evolving and personalized command-line assistant.

> 🔥 Whether you're a power user, system administrator, or automation enthusiast — OS_AGENT is your **next-generation shell**.

---

## 🚨 Important Notes

- ✅ Please use the latest version located in the `osagent-v3/` folder.
- 🚫 **Browser automation is currently not available** in the demo version.
- ☁️ The app is set up and running as a **web UI hosted on an AWS EC2 Ubuntu instance**.

---

## 🚀 Capabilities

- ✅ **Full Control of the Operating System**
  - List/create/delete files and directories
  - Read/write/edit files
  - Run OS-level commands
  - Launch and kill processes
  - Monitor CPU/memory/processes
  - Perform network-related tasks
  - Detect platform (Windows/Linux) and auto-adjust commands

- 💡 **Conversational AI with Memory**
  - Persistent memory of past commands and facts
  - Can refer to previous conversations or system states
  - Learns over time

- 🌐 **Web Terminal Interface**
  - Type and execute commands in your browser
  - Clean, terminal-like UI with real-time feedback
  - Input auto-suggestions and history support

- 🛡️ **Confirmation Layer**
  - Sensitive operations (e.g. deleting files, terminating processes) require confirmation
  - Prevents accidental destructive operations

- 📊 **Real-Time Monitoring**
  - System health and status
  - Active processes, memory usage, platform details

- 🔒 **Secure and Local**
  - Runs locally with no data sent externally
  - Your files and instructions never leave your machine unless you allow it

---

## 🏗️ Tech Stack

- 🧠 Gemini 1.5 Flash (Google Generative AI)
- ⚙️ Python 3.8+
- ⚡ FastAPI (Backend API)
- 🎨 HTML + CSS + JS (Frontend UI)
- 🗃️ SQLite + JSON (Memory persistence)
- 📦 psutil, python-dotenv, uvicorn, google-generativeai

---

## 📁 Directory Structure

```bash
osagent-v3/
├── os_agent.py              # Core OS control + Gemini agent logic
├── app.py                   # FastAPI backend
├── .env                     # Your Gemini API key
├── requirements.txt         # Python dependencies
├── agent_memory/            # Stores persistent memory
└── frontend/
    ├── index.html           # Web UI
    ├── script.js            # Terminal JS logic
    └── style.css            # Terminal design
```

---

## 🔧 Installation Guide

### 1. Clone the Repository

```bash
git clone https://github.com/suryanarayanankv/OS_AGENT.git
cd OS_AGENT/osagent-v3
```

### 2. Set Up Environment

Create a `.env` file:

```env
GEMINI_API_KEY="your_gemini_api_key_here"
```

Get your Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey).

### 3. Install Requirements

```bash
pip install -r requirements.txt
```

### 4. Run the App

```bash
uvicorn app:app --reload
```

Visit: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 💬 Example Commands

Try saying:

- `list all files in Downloads`
- `create a Python file named hello.py`
- `delete the folder test_dir` (will ask for confirmation)
- `show me the processes using the most memory`
- `what OS am I running on?`
- `open notepad` (on Windows)
- `kill process named chrome`

---

## 🧠 Agent Memory

Stored in `agent_memory/`:

- **`agent_memory.db`** – Conversation logs, system facts
- **`quick_memory.json`** – Frequently accessed memory slots

This memory persists across sessions, allowing long-term context.

---

## 🧩 Agent Commands

| Command        | Description                          |
|----------------|--------------------------------------|
| `status`       | Show system status summary           |
| `processes`    | List running system processes        |
| `memory_stats` | Show agent memory usage              |
| `clear`        | Clear the terminal UI                |
| `help`         | List all supported commands          |
| `quit`         | Disable input temporarily            |

---

## 🧠 Why This Matters

> Imagine a future where you don’t need to remember `bash` or `cmd` syntax.  
> You just say:  
> _“Zip all files from last week and email it to me”_ — and it’s done.

**OS_AGENT bridges the gap between human language and OS-level control.**

---

## 🔐 Warning

> **⚠️ This agent has real OS control.**
- Use it responsibly.
- Never run it in production environments without proper sandboxing.
- Confirmation prompts are included for safety but not foolproof.

---

## 🧑‍💻 Contributing

PRs are welcome!  
To contribute:

```bash
git checkout -b feature/your-feature-name
```

---

## 📜 License

[MIT License](LICENSE)

---

## 📎 Acknowledgements

- Gemini API by Google
- FastAPI for blazing-fast APIs
- Terminal.js inspiration from modern terminal emulators

---

**🚀 Your OS has never been this smart. Start talking to it.**
