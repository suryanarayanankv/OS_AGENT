import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

class SimplePlannerAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0.3
        )
        
        self.chat_history = []
        self.max_history = 20
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", """You are a friendly Prompt Enhancement Assistant for MCP agents.

YOUR JOB:
- Help users improve their prompts for better automation agent performance
- Remember our conversation and user preferences
- Make prompts clearer, more specific, and more actionable
- Focus on prompt optimization, not specific tools

HOW TO ENHANCE PROMPTS:
1. Make vague requests more specific
2. Break complex tasks into clear steps
3. Add helpful context and details
4. Improve clarity and structure
5. Suggest better wording and organization
6. Remember user preferences from our chat

PROMPT ENHANCEMENT PRINCIPLES:
- Be specific about what you want
- Include step-by-step instructions when helpful
- Add context about expected outcomes
- Use clear, actionable language
- Structure complex requests logically
- Include error handling hints

ALWAYS END WITH AN ENHANCED PROMPT:
=== ENHANCED PROMPT FOR AUTOMATION AGENT ===
[Your improved, clearer prompt here]
======================================

Keep it conversational and helpful!"""),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
    
    def chat(self, user_input: str) -> str:
        """Chat with the planner agent"""
        try:
            formatted_prompt = self.prompt.format_messages(
                chat_history=self.chat_history,
                input=user_input
            )
            
            response = self.llm.invoke(formatted_prompt)
            
            self.chat_history.append(HumanMessage(content=user_input))
            self.chat_history.append(AIMessage(content=response.content))
            
            if len(self.chat_history) > self.max_history:
                self.chat_history = self.chat_history[-self.max_history:]
            
            return response.content
            
        except Exception as e:
            return f"Sorry, something went wrong: {str(e)}"

def main():
    print("Simple Prompt Enhancer with Memory")
    print("=" * 40)
    print("I help you improve prompts for your MCP agent!")
    print("I'll remember our conversation and make your prompts clearer.")
    print("Type 'exit' or 'quit' to stop.")
    print("=" * 40)
    
    planner = SimplePlannerAgent()
    
    while True:
        user_input = input("\n💬 You: ").strip()
        
        if user_input.lower() in ['exit', 'quit', 'q', '']:
            print(" Goodbye! Hope the enhanced prompts help your MCP agent!")
            break
        
        print("\n🤖 Enhancer:")
        response = planner.chat(user_input)
        print(response)

if __name__ == "__main__":
    main()