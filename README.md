💻 Cross-Platform OS Agent with Persistent Memory (Web UI)
This project implements a powerful AI-driven OS Agent that can interact with your operating system (Linux or Windows) through natural language commands via a web-based terminal interface. It leverages Google's Gemini 1.5 Flash model for understanding and executing tasks, and features persistent memory to learn from past interactions.

Note: The browser automation feature has been explicitly removed from this version of the agent to simplify installation and focus on core OS functionalities.

✨ Features
Natural Language OS Control: Issue commands like "list files in my home directory," "create a new folder named 'my_project'," or "show me running processes."

Cross-Platform Compatibility: Designed to work on both Linux and Windows operating systems.

Persistent Memory: The agent learns and remembers system facts, command usage patterns, and conversation history across sessions, providing more relevant and efficient responses over time.

Web-Based Terminal Interface: Interact with the agent through a user-friendly terminal emulation in your web browser.

Command Confirmation: For sensitive or potentially destructive commands (e.g., deleting files, modifying critical permissions), the agent will prompt for explicit user confirmation before execution, enhancing safety.

Real-time Feedback: Get immediate feedback on command execution success or failure, along with relevant output.

System Monitoring: Query system status, list running processes, and view agent memory statistics.

📁 Project Structure
The project is organized into the following key files:

os_agent.py:

The core intelligence of the OS Agent.

Handles interaction with the Gemini 1.5 Flash model.

Manages persistent memory (SQLite database and JSON for quick access).

Executes system commands (e.g., ls, dir, mkdir, rm).

Provides system information and process management.

app.py:

A FastAPI application that serves as the backend API.

Exposes an /execute endpoint for the frontend to send commands.

Initializes and interacts with the OSAgent instance.

Serves static frontend files (index.html, script.js, style.css).

frontend/index.html:

The main HTML file for the web-based terminal interface.

Provides the structure for the terminal display and input.

frontend/script.js:

The JavaScript logic for the frontend.

Handles user input, sends commands to the backend, and displays responses.

Manages the command confirmation flow.

Provides client-side commands like help, clear, and quit.

frontend/style.css:

CSS file for styling the web terminal, giving it a modern and clean look.

.env:

(You will create this file) Stores your GEMINI_API_KEY securely as an environment variable.

requirements.txt:

(You will create this file) Lists all Python dependencies required for the project.

🚀 Setup and Installation
Follow these steps to get the OS Agent up and running on your local machine.

Prerequisites
Python 3.8+

pip (Python package installer)

An active Google Cloud Project with the Gemini API enabled. You'll need a GEMINI_API_KEY.

1. Clone the Repository (or download files)
If you have these files already, ensure they are in the correct structure:

your-os-agent-project/
├── os_agent.py
├── app.py
├── .env  (you will create this)
├── requirements.txt (you will create this)
└── frontend/
    ├── index.html
    ├── script.js
    └── style.css

2. Set up your Gemini API Key
Create a file named .env in the root directory of your project (the same directory as app.py and os_agent.py). Add your Gemini API key to this file:

GEMINI_API_KEY="YOUR_GEMINI_API_KEY_HERE"

Important: Replace "YOUR_GEMINI_API_KEY_HERE" with your actual Gemini API key. Keep this file private and do not commit it to public repositories.

3. Install Python Dependencies
Create a requirements.txt file in the root directory of your project with the following content:

fastapi
uvicorn
python-dotenv
google-generativeai
psutil

Then, install the dependencies using pip:

pip install -r requirements.txt

4. Run the FastAPI Application
Navigate to the root directory of your project in your terminal and run the FastAPI application using Uvicorn:

uvicorn app:app --reload

app:app refers to the app object within the app.py file.

--reload is useful during development as it automatically restarts the server when code changes are detected.

You should see output indicating that the server is running, typically on http://127.0.0.1:8000 or http://localhost:8000.

🌐 Usage
Access the Web UI: Open your web browser and navigate to the address provided by Uvicorn (e.g., http://127.0.0.1:8000).

Interact with the Agent: You will see a terminal-like interface. Type your natural language commands or OS commands into the input field and press Enter.

Example Commands to Try:
list files in current directory

create a folder named 'test_agent_dir'

show me running processes

what is my current operating system?

status (frontend-only command for system status)

processes (frontend-only command to list processes)

memory_stats (frontend-only command for agent memory info)

help (frontend-only command to see available commands)

clear (frontend-only command to clear the terminal screen)

quit (frontend-only command to disable the input)

Command Confirmation
For sensitive operations (e.g., delete file 'important.txt', rm -rf /), the agent will ask for your explicit confirmation. Type yes to proceed or no to cancel.

🧠 Memory and Persistence
The agent uses an agent_memory directory (created automatically) to store its persistent memory:

agent_memory.db: An SQLite database storing conversational history, learned system facts, and command execution logs.

quick_memory.json: A JSON file for quick access to frequently used commands and learned preferences.

This memory allows the agent to build context and provide more intelligent responses over time.

🤝 Contributing
Feel free to fork this repository, open issues, or submit pull requests. Contributions are welcome!

📄 License
This project is open-source and available under the MIT License.