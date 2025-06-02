import os
import sys
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from dotenv import load_dotenv
import asyncio
import logging
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
# Import the OSAgent from your refactored file
from os_agent import OSAgent # BrowserCode import removed

load_dotenv()

# Configure logging for the FastAPI app
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

origins = [
    "http://localhost:8000", # For local testing
    "http://127.0.0.1:8000",
    # Once you get your frontend's URL from Render, add it here:
    # e.g., "https://your-os-agent-frontend.onrender.com"
    "*" # TEMPORARY: Allows all origins for hackathon simplicity. Be specific in production!
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files (for your HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize the OS Agent
gemini_api_key = os.getenv('GEMINI_API_KEY')
if not gemini_api_key:
    logger.error("GEMINI_API_KEY environment variable not set.")
    sys.exit(1) # Exit if API key is not set

os_agent = OSAgent(gemini_api_key=gemini_api_key)
logger.info("OSAgent initialized successfully for FastAPI.")

class CommandRequest(BaseModel):
    command: str
    # Add an optional list of commands that the user has confirmed
    confirmed_commands: Optional[List[str]] = Field(default_factory=list)

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the main HTML page."""
    with open("frontend/index.html", "r") as f:
        return HTMLResponse(content=f.read())

@app.post("/execute", response_model=dict)
async def execute_command(request: CommandRequest):
    """
    Endpoint to execute OS commands.
    """
    user_command = request.command
    confirmed_cmds = request.confirmed_commands
    logger.info(f"Received command from frontend: {user_command}")
    logger.info(f"Confirmed commands: {confirmed_cmds}")


    try:
        # Pass the confirmed_commands to the agent's process_request method
        result = await os_agent.process_request(user_command, confirmed_commands=confirmed_cmds)
        logger.info(f"OSAgent processing complete. Result: {result}")
        return result
    except Exception as e:
        logger.error(f"Error processing command '{user_command}': {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")