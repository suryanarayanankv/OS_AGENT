
from Axiom_State import AgentState
from langgraph.graph import add_messages, StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
import sqlite3
import aiosqlite
from langgraph.prebuilt import ToolNode
from terminal_tool import execute_shell_command
from zapier_tools import initialize_and_get_mcp_tools 
from file_tools import get_file_tools, create_file, write_file, read_file, replace_in_file, delete_file
from prompts import SYSTEM_PROMPT

import asyncio

load_dotenv()




# Initialize global variable for Zapier tools
zapier_tools_list = []

async def main():
    sqlite_conn = await aiosqlite.connect("checkpoint.sqlite"
                               ,check_same_thread=False)
    memory =  AsyncSqliteSaver(sqlite_conn)
    global zapier_tools_list

    # --- Initialize Zapier tools ONCE at startup ---
    zapier_tools_list = await initialize_and_get_mcp_tools()

    graph = StateGraph(AgentState)

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash")

    # --- Combine all tools, including directly loaded Zapier tools ---
    all_tools = [
        execute_shell_command,
    ]
    all_tools.extend(get_file_tools())
    all_tools.extend(zapier_tools_list) # NEW: Add the directly loaded Zapier tools

    llm_with_tools = llm.bind_tools(tools=all_tools)

    async def AxiomChat(state : AgentState):
        response = await llm_with_tools.ainvoke(state["messages"])
        return {
            "messages": [response]
        }


    def tools_router(state: AgentState):
        last_message = state["messages"][-1]

        if isinstance(last_message, ToolMessage):
            return "chat"
        
        if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
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

    app = graph.compile(checkpointer=memory)
    config = {"configurable": {
        "thread_id": 1
    }}
    print(app.get_graph().print_ascii())
    print(app.get_graph().draw_mermaid())

    print("Agent is ready. Type 'exit' or 'end' to stop.")

    while True: 
        user_input = input("User: ")
        if(user_input.lower() in ["exit", "end"]):
            break
        else: 
            initial_message_content = f"{SYSTEM_PROMPT}\n\nUser request: {user_input}"
            
            result = await app.ainvoke({
                "messages": [HumanMessage(content=initial_message_content)],
            },config=config)

            final_message = result["messages"][-1]
            if isinstance(final_message, AIMessage):
                print(f"Agent: {final_message.content}")
            elif isinstance(final_message, ToolMessage):
                print(f"Agent executed tool. Output: {final_message.content}")
            else:
                print(f"Agent: {final_message}")

if __name__ == "__main__":
    asyncio.run(main())

