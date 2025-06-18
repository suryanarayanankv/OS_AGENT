from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
from pathlib import Path
from typing import Dict, Any, List
import json
from contextlib import asynccontextmanager

# Import backend components
from axiom_backend.Axiom_2 import initialize_agent, invoke_agent, summarize_chat_history
from axiom_backend.Axiom_State import AgentState
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from axiom_backend.mcp_config import router as mcp_router
from axiom_backend.system_metrics import (
    get_system_metrics, 
    get_detailed_system_info, 
    log_system_metrics, 
    get_historical_metrics
)
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Serve the React frontend static files ---
frontend_dist_dir = Path(__file__).parent / "axiom-web" / "dist"

if not frontend_dist_dir.exists():
    raise RuntimeError(f"React build directory '{frontend_dist_dir.absolute()}' not found. "
                      "Please navigate to your React project and run `npm run build`.")

# Mount static files
app.mount("/assets", StaticFiles(directory=frontend_dist_dir / "assets"), name="assets")
templates = Jinja2Templates(directory=frontend_dist_dir)

# Include MCP router
app.include_router(mcp_router, prefix="/api")

async def periodic_metrics_logger(interval_seconds: int = 60):
    while True:
        try:
            log_system_metrics()
        except Exception as e:
            print(f"[Periodic Logger] Error logging system metrics: {e}")
        await asyncio.sleep(interval_seconds)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic - your old startup_event code goes here
    print("Initializing LangGraph agent...")
    await initialize_agent()
    print("LangGraph agent initialized.")
    # Start periodic logging in the background
    asyncio.create_task(periodic_metrics_logger(60))
    
    yield  # App runs here
    
    # Shutdown logic (optional - runs when app shuts down)
    print("Application shutting down...")



# API Routes - These must come BEFORE the catch-all route
@app.get("/api/system-metrics")
async def get_system_metrics_endpoint():
    """Get system performance metrics for the dashboard."""
    try:
        metrics = get_system_metrics()
        # Log the metrics for historical tracking
        log_system_metrics()
        return JSONResponse(content=metrics)
    except Exception as e:
        print(f"Error getting system metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting system metrics: {str(e)}")

@app.get("/api/system-info")
async def get_system_info_endpoint():
    """Get detailed system information."""
    try:
        info = get_detailed_system_info()
        return JSONResponse(content=info)
    except Exception as e:
        print(f"Error getting system info: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting system info: {str(e)}")

@app.get("/api/historical-metrics/{time_range}")
async def get_historical_metrics_endpoint(time_range: str):
    """Get historical system metrics for the specified time range."""
    try:
        valid_ranges = ['1h', '6h', '1d', '1w', '1m']
        if time_range not in valid_ranges:
            raise HTTPException(status_code=400, detail=f"Invalid time range. Must be one of: {valid_ranges}")
        
        metrics = get_historical_metrics(time_range)
        return JSONResponse(content={"metrics": metrics, "time_range": time_range})
    except Exception as e:
        print(f"Error getting historical metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Error getting historical metrics: {str(e)}")

@app.post("/api/log-metrics")
async def log_metrics_endpoint():
    """Manually log current system metrics."""
    try:
        success = log_system_metrics()
        if success:
            return JSONResponse(content={"message": "Metrics logged successfully"})
        else:
            raise HTTPException(status_code=500, detail="Failed to log metrics")
    except Exception as e:
        print(f"Error logging metrics: {e}")
        raise HTTPException(status_code=500, detail=f"Error logging metrics: {str(e)}")

@app.post("/api/chat")
async def chat_endpoint(payload: Dict[str, Any]):
    """Handle chat messages from the frontend."""
    session_id = payload.get("session_id")
    user_message_content = payload.get("message")

    if not session_id or not user_message_content:
        raise HTTPException(status_code=400, detail="Missing session_id or message in request.")

    try:
        config = {"configurable": {"thread_id": session_id}}
        result = await invoke_agent(user_message_content, config)

        if not result or "messages" not in result or not result["messages"]:
            raise HTTPException(status_code=500, detail="No response received from agent")

        final_message = result["messages"][-1]
        if final_message is None:
            raise HTTPException(status_code=500, detail="Empty response from agent")

        response_content = ""
        if isinstance(final_message, AIMessage):
            response_content = final_message.content if hasattr(final_message, "content") else str(final_message)
        elif isinstance(final_message, ToolMessage):
            response_content = f"Agent executed tool. Output: {final_message.content if hasattr(final_message, 'content') else str(final_message)}"
        else:
            response_content = str(final_message)

        return JSONResponse(content={"response": response_content})

    except Exception as e:
        print(f"Error invoking agent: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat: {str(e)}")

@app.post("/api/summarize_chat")
async def summarize_chat(request: Dict[str, Any]):
    """Summarize chat history."""
    try:
        messages = request.get("messages", [])
        if not messages:
            return JSONResponse(content={"summary": "Untitled Chat"})

        summary = await summarize_chat_history(messages)
        return JSONResponse(content={"summary": summary})
    except Exception as e:
        print(f"Error summarizing chat: {e}")
        raise HTTPException(status_code=500, detail=f"Error summarizing chat: {str(e)}")

# Catch-all route for frontend - This must come LAST
@app.get("/{full_path:path}", response_class=HTMLResponse)
async def serve_frontend(request: Request, full_path: str):
    """Serve the React frontend."""
    return templates.TemplateResponse("index.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1", port=8000)