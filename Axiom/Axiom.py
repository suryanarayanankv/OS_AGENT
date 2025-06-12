from Axiom_State import AgentState
from langgraph.graph import add_messages, StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3
from langgraph.prebuilt import ToolNode
from terminal_tool import execute_shell_command



load_dotenv()

graph = StateGraph(AgentState)

llm = ChatGroq(
    model="llama-3.1-8b-instant",)
tools= [execute_shell_command]
llm_with_tools = llm.bind_tools(tools=tools)

def AxiomChat(state : AgentState):
    response = llm_with_tools.invoke(state["messages"])
    return {
        "messages": [response], 
    }


def tools_router(state: AgentState):
    last_message = state["messages"][-1]

    if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
        return "tool_node"
    else: 
        return END
    
tool_node = ToolNode(tools=tools)
graph.add_node("chat",AxiomChat)
graph.add_node("tool_node",tool_node) # Corrected node name used consistently

graph.add_conditional_edges(
    "chat",
    tools_router,
    {
        "tool_node": "tool_node", # Map the string "tool_node" from router to the node "tool_node"
        END: END # Map the END object from router to the END point
    }
)
graph.add_edge("tool_node","chat")
graph.set_entry_point("chat")


app = graph.compile()
print(app.get_graph().print_ascii())
print(app.get_graph().draw_mermaid())

print("Agent is ready. Type 'exit' or 'end' to stop.")

# ... (rest of your code) ...

while True: 
    user_input = input("User: ")
    if(user_input in ["exit", "end"]):
        break
    else: 
        result = app.invoke({
            "messages": [HumanMessage(content=user_input)]
        })

        print(result)