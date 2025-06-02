# 🧠 OS_AGENT – AI That Controls Your Operating System

This project implements a powerful **AI-driven OS Agent** that interacts with your operating system (Linux or Windows) using natural language via a **web-based terminal interface**. It is designed to understand and execute a wide range of system-level commands with persistent memory and real-time feedback.

> ⚠️ **Browser automation is excluded in this version.** The currently hosted demo runs on an AWS EC2 Ubuntu instance using a Web UI.

---

## ✨ Features

- 🔧 **Full Operating System Control via AI**  
  Perform *any* system-level task such as creating/deleting files, checking processes, managing directories, system monitoring, and more using natural language.

- 🌐 **Web-Based Terminal Interface**  
  Easy-to-use web terminal to type and execute commands in real time.

- 🧠 **Persistent Memory**  
  Remembers past interactions and system facts using a lightweight SQLite + JSON memory system.

- ⚙️ **Cross-Platform Compatibility**  
  Works on both **Linux** and **Windows** systems.

- 🔐 **Command Confirmation**  
  Confirms before executing sensitive commands (e.g., deleting files or folders).

- 📊 **System Monitoring & Statistics**  
  View system usage, memory stats, and active processes.

---

## 🧪 Live Demo (For Judges)

🖥️ **[Click here to access the live demo](https://tecrade.github.io/OS_AGENT_FRONTEND/)**  
> ✅ This version is hosted on an **AWS EC2 Ubuntu** server  
> 🚫 **Browser automation is excluded** in this demo  
> ✅ This demo showcases only the `osagent-v3` Web UI version

---

## 📁 Project Structure (osagent-v3)

```
osagent-v3/
├── app.py                   # FastAPI backend
├── os_agent.py              # Core OS agent logic
├── requirements.txt         # Python dependencies
├── agent_memory/            # Persistent memory (DB + JSON)
└── frontend/
    ├── index.html           # Terminal interface
    ├── script.js            # Frontend logic
    └── style.css            # Styling
```

---

## 🚀 Setup & Installation

### 📌 Prerequisites

- Python 3.8+
- `pip` installed
- Gemini API Key from Google AI Studio

---

### 1. Clone the Repository

```bash
git clone https://github.com/suryanarayanankv/OS_AGENT.git
cd OS_AGENT/osagent-v3
```

---

### 2. Set Up Environment Variables

Create a `.env` file in `osagent-v3/`:

```env
GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"
```

---

### 3. Install Python Dependencies

Install required libraries:

```txt
# requirements.txt
fastapi
uvicorn
python-dotenv
google-generativeai
psutil
```

Then run:

```bash
pip install -r requirements.txt
```

---

### 4. Run the Application

From the `osagent-v3/` folder:

```bash
uvicorn app:app --reload
```

Open in your browser:

```
http://127.0.0.1:8000
```

---

## 🔍 Example Commands

- `list files in home directory`
- `create a folder named test_dir`
- `show running processes`
- `delete file named temp.txt`
- `what is my current OS?`

---

## 🧠 Memory Storage

Persistent memory is stored in:

- `agent_memory/agent_memory.db` – Conversation history and facts
- `agent_memory/quick_memory.json` – Frequently accessed key-value data

---

## ⚠️ Important Reminders

- ✅ Only use the **`osagent-v3/`** folder. Earlier versions contain browser automation which is complex and excluded from demo.
- 🖥️ The current public demo runs purely on a Web UI hosted on **AWS EC2 Ubuntu**.
- ❌ No browser automation is active in this version.

---

## 🤝 Contributing

We welcome contributions! Feel free to fork the repo, raise issues, or submit PRs.

---

## 📄 License

This project is licensed under the **MIT License**.
