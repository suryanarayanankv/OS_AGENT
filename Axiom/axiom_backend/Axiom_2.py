from .Axiom_State import AgentState
from langgraph.graph import add_messages, StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import sqlite3
import aiosqlite
from langgraph.prebuilt import ToolNode
from .terminal_tool import execute_shell_command
from .zapier_tools import initialize_and_get_mcp_tools 
from .file_tools import get_file_tools, create_file, write_file, read_file, replace_in_file, delete_file
from .prompts import SYSTEM_PROMPT
import re

import asyncio

load_dotenv()

# Global variables
_agent = None
zapier_tools_list = []

def format_system_info(content: str) -> str:
    """Format system information without markdown formatting."""
    # Remove markdown formatting
    content = re.sub(r'\*\*|\*|`', '', content)
    
    # Split into sections
    sections = content.split('\n*')
    
    # Format each section
    formatted_sections = []
    for section in sections:
        if not section.strip():
            continue
            
        # Remove leading/trailing whitespace and colons
        section = section.strip().strip(':')
        
        # Split into title and content
        if ':' in section:
            title, content = section.split(':', 1)
            title = title.strip()
            content = content.strip()
            
            # Special handling for disk space and memory usage
            if title == 'Disk Space' or title == 'Memory Usage':
                # Split content into lines and format as a table
                lines = content.split('\n')
                if lines:
                    # Use the first line as header
                    header = lines[0].strip()
                    # Format the rest as table rows
                    rows = [line.strip() for line in lines[1:] if line.strip()]
                    # Join with newlines
                    content = f"{header}\n" + "\n".join(rows)
            
            # Format the section
            formatted_section = f"{title}:\n{content}"
            formatted_sections.append(formatted_section)
        else:
            formatted_sections.append(section)
    
    # Join sections with newlines
    return '\n\n'.join(formatted_sections)

def format_tool_output(content: str) -> str:
    """Format tool output in a user-friendly way."""
    # Remove any markdown formatting
    content = re.sub(r'\*\*|\*|`', '', content)
    
    # Split into lines and remove empty lines
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Format each line as a bullet point
    formatted_lines = []
    for line in lines:
        # Remove any existing bullet points or numbers
        line = re.sub(r'^[\d\.\s\-*]+', '', line).strip()
        if line:
            formatted_lines.append(f"• {line}")
    
    # Join with newlines
    return '\n'.join(formatted_lines)

async def initialize_agent():
    """Initialize the LangGraph agent with necessary tools and configuration."""
    global _agent, zapier_tools_list
    
    if _agent is not None:
        return _agent

    sqlite_conn = await aiosqlite.connect("memory.sqlite", check_same_thread=False)
    memory = AsyncSqliteSaver(sqlite_conn)

    # Initialize Zapier tools (will return empty list if MCP is not available)
    zapier_tools_list = await initialize_and_get_mcp_tools()

    graph = StateGraph(AgentState)

    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
    # llm = ChatGroq(model="llama-3.1-8b-instant")

    # Combine all tools
    all_tools = [execute_shell_command]
    all_tools.extend(get_file_tools())
    
    # Only add Zapier tools if they were successfully initialized
    if zapier_tools_list:
        all_tools.extend(zapier_tools_list)

    llm_with_tools = llm.bind_tools(tools=all_tools)

    async def AxiomChat(state: AgentState):
        response = await llm_with_tools.ainvoke(state["messages"])
        
        # Format system information if present
        if isinstance(response, AIMessage):
            if "system information" in response.content.lower():
                response.content = format_system_info(response.content)
            elif "tool" in response.content.lower() or "command" in response.content.lower():
                response.content = format_tool_output(response.content)
                
        return {"messages": [response]}

    def tools_router(state: AgentState):
        last_message = state["messages"][-1]
        if isinstance(last_message, ToolMessage):   
            return "chat"
        
        if hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0:
            return "tool_node"
        else: 
            return END
        
    tool_node = ToolNode(tools=all_tools)

    graph.add_node("chat", AxiomChat)
    graph.add_node("tool_node", tool_node)

    graph.add_conditional_edges(
        "chat",
        tools_router,
        {
            "tool_node": "tool_node",
            END: END
        }
    )

    graph.add_conditional_edges(
        "tool_node",
        tools_router,
        {
            "chat": "chat",
            END: END
        }
    )

    graph.set_entry_point("chat")
    _agent = graph.compile(checkpointer=memory)
    
    return _agent

async def invoke_agent(message: str, config: dict) -> dict:
    """Invoke the agent with a message and return the response."""
    global _agent
    
    if _agent is None:
        _agent = await initialize_agent()

    initial_message_content = f"{SYSTEM_PROMPT}\n\nUser request: {message}"
    
    result = await _agent.ainvoke({
        "messages": [HumanMessage(content=initial_message_content)],
    }, config=config)
    print(result["messages"][-1])
    return result

async def summarize_chat_history(messages: list) -> str:
    """Summarize the chat history."""
    if not messages:
        return "Untitled Chat"
        
    # Simple summarization: use the first user message as the title
    for msg in messages:
        if msg.get("role") == "user":
            content = msg.get("content", "")
            # Take first 50 characters or up to first newline
            summary = content.split("\n")[0][:50]
            return summary + "..." if len(content) > 50 else summary
            
    return "Untitled Chat"

