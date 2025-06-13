## Accessible Automation Agent 

**Introduction:**

Meet the Accessible Automation Agent, designed to empower users of all technical backgrounds. This agent simplifies complex tasks, making automation accessible to everyone.

**Technical Aspects:**

*   **Key Files:**
    *   `success.py`: This file initializes and runs the main agent loop. It uses Langchain and Google Gemini to create an autonomous agent with memory management capabilities. It leverages the MCP (Managed Component Protocol) client for tool access.
    *   `planner.py`: This file implements a "Prompt Enhancement Assistant" that helps users refine their prompts for better agent performance. It uses Langchain and Google Gemini to provide conversational prompt improvement.
    *   `.env`: This file stores the Google API key.
    *   `browser_mcp.json`: This file likely contains configuration details for the MCP client, potentially including API keys or service endpoints.
*   **Key Functions and Classes:**
    *   `success.py`: `run_interactive()` initializes the agent, sets up the prompt, and runs the main loop to interact with the user.
    *   `planner.py`: `SimplePlannerAgent` class handles prompt enhancement. The `chat()` method formats the prompt, invokes the LLM, and manages chat history.
*   **Dependencies:**
    *   `langchain`: Framework for building LLM-powered applications.
    *   `langchain_google_genai`: Integration for Google's Gemini models.
    *   `mcp_use`: Library for interacting with the Managed Component Protocol.
    *   `dotenv`: For loading environment variables from a `.env` file.
    *   `asyncio`: For asynchronous programming.
*   **Interaction:** `success.py` uses the `MCPClient` to access various tools and the `LangChainAdapter` to make them compatible with the Langchain framework. The agent in `success.py` interacts with the user to receive instructions and executes tasks using the available tools. `planner.py` enhances user prompts before they are passed to the agent.
*   **Algorithms/Techniques:** The agent uses a prompt template to guide the LLM's behavior. It also implements memory management to maintain context across multiple turns of conversation.

**Features:**

*   **External Services:** Access to external services via the MCP client (details depend on the MCP configuration).
*   **OS-Level Integration:** Potentially, depending on the tools available through the MCP client.
*   **Task Automation:** Automates tasks based on user input and available tools.
*   **User-Friendly Interface:** Interactive command-line interface.
*   **Proactive Memory Management:** The agent actively stores and retrieves information to improve performance and personalize interactions.
*   **Prompt Enhancement:** The `planner.py` script provides a way to improve prompts for better automation results.

**How to Use:**

1.  Ensure you have a Google API key and place it in a `.env` file.
2.  Configure the `browser_mcp.json` file with the necessary credentials and service endpoints for the MCP client.
3.  Run `success.py` to start the agent.
4.  Interact with the agent via the command line, providing instructions and tasks.
5.  Use `planner.py` to refine your prompts for better results.

**Example Use Cases:**

*   "Search for repositories related to 'Langchain' and create an issue in one of them."
*   "Find the latest Airbnb listings in London for two adults."
*   "Help me write a better prompt for summarizing a document."

**Future Development:**

*   Integration with a graphical user interface.
*   Expanded toolset via the MCP client.
*   More sophisticated memory management and reasoning capabilities.
*   Improved prompt engineering and error handling.

**Competition Context:**

This Accessible Automation Agent is a submission for the 100x competition. It showcases the potential of accessible automation by providing a user-friendly interface to powerful LLM and tool-based automation. The agent's proactive memory management and prompt enhancement capabilities demonstrate its ability to learn and adapt to user needs, making it a valuable tool for users of all technical skill levels.
