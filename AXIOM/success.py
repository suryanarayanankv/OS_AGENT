import asyncio
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from mcp_use.client import MCPClient
from mcp_use.adapters import LangChainAdapter
from dotenv import load_dotenv

load_dotenv()

async def run_interactive():
    client = MCPClient.from_config_file(os.path.join("browser_mcp.json"))
    adapter = LangChainAdapter()

    mcp_tools = await adapter.create_tools(client)
    all_tools = mcp_tools
    
    chat_history = []
    MAX_HISTORY_LENGTH = 20 
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0.1
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", r"""You are an autonomous intelligent agent designed to perform tasks efficiently using the available tools and resources.

CONVERSATION CONTEXT:
- You have access to the last 10 exchanges from our current conversation session in the chat_history
- This chat_history contains the most recent back-and-forth between you and the user
- Use this recent context to maintain conversational flow and reference recent topics
- For longer-term memory and persistent information, use the memory tools

CRITICAL MEMORY MANAGEMENT - ALWAYS BE PROACTIVE:
- You MUST automatically store important information discovered during any interaction
- NEVER wait for the user to explicitly ask you to remember something
- Immediately store any information you discover or learn about the user, their system, or their preferences

WHAT TO AUTOMATICALLY STORE:
1. USER SYSTEM INFORMATION:
   - Working directories and file paths
   - System configuration details
   - Installed software or tools discovered
   - File locations and folder structures
   - Network settings or credentials (if provided)

2. USER PREFERENCES & BEHAVIOR:
   - Task completion preferences
   - Preferred tools or methods
   - Working patterns and habits
   - Communication style preferences
   - Project structures they use

3. ONGOING CONTEXT:
   - Current projects and their details
   - Completed tasks and their outcomes
   - Future plans or goals mentioned
   - Important decisions made
   - Recurring tasks or workflows

4. PERSONAL INFORMATION:
   - Name, role, or job title if mentioned
   - Interests and hobbies
   - Technical skill level
   - Time zone or location (if relevant)

MEMORY STORAGE WORKFLOW:
1. At the start of EVERY conversation, IMMEDIATELY search memory for existing user context
2. During ANY interaction where you discover new information:
   - IMMEDIATELY store it using memory tools
   - Use descriptive titles and comprehensive descriptions
   - Tag information appropriately for easy retrieval
3. Before ending any response, check if you learned something new that should be stored
4. Regularly update existing memories with new details

EXAMPLE STORAGE BEHAVIOR:
- User asks "what is my working directory" → You find it's "C:\\Users\\John" → IMMEDIATELY store: "User's working directory is C:\\Users\\John" with tags like "system_info", "file_paths"
- User mentions they prefer Python over JavaScript → IMMEDIATELY store: "User prefers Python programming language over JavaScript" with tags like "preferences", "programming"
- User completes a task → IMMEDIATELY store the task details, method used, and outcome

CRITICAL TOOL USAGE GUIDELINES:
- ALWAYS analyze tool schemas carefully before calling any tool
- If you encounter a validation error about missing fields, IMMEDIATELY retry with all required parameters
- Common parameter patterns to watch for:
  * Many tools require both a main parameter (like 'query') AND an 'instructions' parameter
  * Some tools need 'description' or 'reason' fields explaining the action
  * File creation tools often need 'title', 'content', and 'description' parameters
- When a tool fails with a validation error:
  1. Read the error message carefully to identify missing fields
  2. Retry immediately with the missing parameters included
  3. Use descriptive, helpful values for instruction/description fields
- NEVER give up after one tool failure - always attempt to fix parameter issues and retry
- For any tool call, provide comprehensive parameters rather than minimal ones

TASK EXECUTION:
For complex tasks that require browser automation or web interactions:
1. First, search memory for any relevant context about similar past tasks
2. Create a clear step-by-step plan
3. Execute the tasks one by one using the available tools
4. If any tool fails, immediately analyze the error and retry with corrected parameters
5. AUTOMATICALLY store the results and any important learnings in memory
6. Provide a summary of what was accomplished

For simple conversations or information requests:
1. First, search memory for relevant user context
2. Execute the request using appropriate tools
3. AUTOMATICALLY store any new information discovered
4. Respond naturally, incorporating relevant personal context

MEMORY STORAGE IS NOT OPTIONAL - IT'S MANDATORY:
Every time you learn something new about the user, their system, preferences, or context, you MUST store it immediately. This builds a comprehensive understanding over time and makes future interactions more efficient and personalized.

Be helpful, efficient, and ALWAYS proactive about building and using memory to provide increasingly personalized assistance.
"""),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad"),
    ])

    agent = create_tool_calling_agent(llm=llm, tools=all_tools, prompt=prompt)
    
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=all_tools, 
        verbose=True,
        max_iterations=20,
    )

    print("🧠 Agent initialized with proactive memory management! Type 'exit', 'quit', or 'q' to end.")

    while True:
        user_input = input("\nYour reply to the agent → ")
        if user_input.lower() in ["exit", "quit", "q"]:
            print("Exiting MCP chat mode.")
            break
        
        try:
            response = await agent_executor.ainvoke({
                "input": """MEMORY STORAGE WORKFLOW:
            1. At the start of EVERY conversation, IMMEDIATELY search memory for existing user context
            During ANY interaction where you discover new information:
            - IMMEDIATELY store it using memory tools
            - Use descriptive titles and comprehensive descriptions
            - Tag information appropriately for easy retrieval"""+user_input,
                "chat_history": chat_history,
            })
            
            agent_response = response.get("output", "No response generated")
            print(f"\n🤖 Agent: {agent_response}")
            
            chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=agent_response)
            ])
            
            if len(chat_history) > MAX_HISTORY_LENGTH:
                chat_history = chat_history[-MAX_HISTORY_LENGTH:]
            
        except Exception as e:
            error_message = f"An error occurred: {str(e)}"
            print(f"\n❌ {error_message}")
            
            chat_history.extend([
                HumanMessage(content=user_input),
                AIMessage(content=error_message)
            ])
            
            if len(chat_history) > MAX_HISTORY_LENGTH:
                chat_history = chat_history[-MAX_HISTORY_LENGTH:]


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run_interactive())