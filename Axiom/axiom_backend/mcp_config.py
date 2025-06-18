from fastapi import APIRouter, HTTPException
from typing import Dict, Any
import json
from pathlib import Path
from .Axiom_2 import initialize_agent,invoke_agent
router = APIRouter()

def get_config_path() -> Path:
    """Get the path to the MCP configuration file."""
    # Go up two levels from the current file to reach the root directory
    root_dir = Path(__file__).parent.parent.parent
    config_path = root_dir / "browser_mcp.json"
    print(f"DEBUG: MCP config path: {config_path.absolute()}")
    return config_path

def load_config() -> Dict[str, Any]:
    """Load the current MCP configuration."""
    config_path = get_config_path()
    print(f"DEBUG: Loading config from: {config_path}")
    if not config_path.exists():
        print("DEBUG: Config file does not exist, creating default")
        return {"mcpServers": {}}
        
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            print(f"DEBUG: Loaded config: {config}")
            return config
    except Exception as e:
        print(f"Error reading MCP configuration: {e}")
        return {"mcpServers": {}}

def save_config(config: Dict[str, Any]) -> None:
    """Save the MCP configuration."""
    config_path = get_config_path()
    print(f"DEBUG: Saving config to: {config_path}")
    print(f"DEBUG: Config to save: {config}")
    try:
        with open(config_path, 'w') as file:
            json.dump(config, file, indent=2)
        print("DEBUG: Config saved successfully")
    except Exception as e:
        print(f"Error saving MCP configuration: {e}")
        raise

@router.get("/mcp_config")
async def get_mcp_config():
    """Get the current MCP configuration."""
    try:
        return load_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading MCP configuration: {str(e)}")

@router.post("/mcp_config")
async def update_mcp_config(config: Dict[str, Any]):
    """Update the MCP configuration."""
    try:
        # Load existing configuration
        current_config = load_config()
        
        # Ensure mcpServers exists in both configs
        if "mcpServers" not in current_config:
            current_config["mcpServers"] = {}
        if "mcpServers" not in config:
            config["mcpServers"] = {}
            
        # Merge new servers with existing ones
        current_config["mcpServers"].update(config["mcpServers"])
        
        # Save the merged configuration
        save_config(current_config)
        
        return {
            "status": "success", 
            "message": "MCP configuration updated successfully",
            "config": current_config
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error updating MCP configuration: {str(e)}") 