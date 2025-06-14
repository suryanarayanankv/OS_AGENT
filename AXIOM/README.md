# 🧠 MCP Agent

### Terminal-First, AI-Powered Automation with Built-In Tool Support

The **MCP Agent** is a lightweight, powerful terminal-based AI agent that connects to multiple services using modular tool servers. It can perform complex tasks like summarizing emails, interacting with GitHub, automating Airbnb workflows, and more — all through natural language. Designed for extensibility and privacy, it supports local LLMs and integrates easily with any service.

---

## ⚙️ Prerequisites

- **Python 3.11+** – Required to run the core MCP Agent and manage its execution environment.

---

## 🚀 Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/your-username/mcp-agent.git
   cd mcp-agent
   ```

2. **Create a `.env` file** and add your Google API key:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

3. **Create a `browser_mcp.json` file** in the root directory. This file will contain your configured MCP servers. See below for examples.

---

## 🧠 Adding Long-Term Memory (openMemory MCP)

To enable long-term memory in your agent, add the following config inside `browser_mcp.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "openmemory": {
      "command": "npx",
      "args": ["-y", "openmemory"],
      "env": {
        "OPENMEMORY_API_KEY": "your_api_key_here",
        "CLIENT_NAME": "openmemory"
      }
    }
  }
}
```

This provides persistent, searchable memory to your system — allowing agents to retain knowledge across sessions.

### 🔐 Get Your API Key

1. Visit [https://mem0.ai/openmemory-mcp](https://mem0.ai/openmemory-mcp) and sign in.
2. Click **"Install openMemory"**.
3. Click on the **MCP link** provided.
4. Copy your API key and paste it into the JSON above.

### 📦 Requirement

- **Node.js** – Required to run the `openmemory` server via `npx`.

📺 [Watch this guide to install Node.js](https://youtu.be/kC56yUZCKu4?feature=shared)

---

## 🔗 Connecting Automations (Zapier MCP)

To connect your agent with Zapier and unlock automations, add the following to `browser_mcp.json`:

```json
{
  "mcpServers": {
    "zapier": {
      "url": "https://hooks.zapier.com/mcp/your-server-url"
    }
  }
}
```

### 🛠 How to Set It Up

1. Go to [https://zapier.com/mcp](https://zapier.com/mcp)
2. Click **"Get Started"**
3. Click **"+ New MCP Server"**
4. Choose **"Other"** as the client
5. Add your tools in the **Configure** section
6. Set **Transport Type** to **SSE**
7. Copy the generated **Server URL**
8. Paste it into the JSON above

### 💡 Why Zapier?

Zapier MCP gives you instant access to **over 8000 built-in tools** — like Gmail, Slack, Sheets — without configuring each individually.

### ⚠️ Beta Warning

Zapier MCP is in **beta**, so you may encounter internal server errors. Retry after a few moments if needed.

---

## 📁 Example `browser_mcp.json` Structure

Here’s how your `browser_mcp.json` should look with both `openmemory` and `zapier` configured:

```json
{
  "mcpServers": {
    "openmemory": {
      "command": "npx",
      "args": ["-y", "openmemory"],
      "env": {
        "OPENMEMORY_API_KEY": "your_api_key_here",
        "CLIENT_NAME": "openmemory"
      }
    },
    "zapier": {
      "url": "https://hooks.zapier.com/mcp/your-server-url"
    }
  }
}
```

---

## 🌐 Add More MCP Servers

You can easily extend your agent by adding more MCP servers — there are thousands available!

Check out these curated lists:
- [punkpeye/awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)
- [appcypher/awesome-mcp-servers](https://github.com/appcypher/awesome-mcp-servers)

Just copy and paste their example JSON blocks into your `browser_mcp.json` under the `mcpServers` key.

---

## ✅ Next Steps

- Add more MCP servers (e.g., GitHub, Airbnb, Gmail)
- Connect to local or cloud LLMs
- Build workflows and memory with ease



## ▶️ Running the Agent
```bash
pip install  -r requirements.txt
```
Once your `browser_mcp.json` is configured, you can start using the agent:

```bash
python success.py
```

To get well-structured natural language prompts for tasks, you can also run:

```bash
python planner.py
```

This helps generate clear task prompts to pass to your MCP Agent.

---

## 📬 Contact

For any queries, reach out to **githubsurya@gmail.com**
