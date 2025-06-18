# zapier_tools.py
import asyncio
import os
import json
from pathlib import Path
from typing import List
from langchain_core.tools import BaseTool

# Try to import MCP-related modules, but don't fail if they're not available
try:
    from mcp_use.client import MCPClient
    from mcp_use.adapters import LangChainAdapter
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    print("MCP modules not available. Running without MCP tools.")

from dotenv import load_dotenv

load_dotenv()

_mcp_client = None
_mcp_adapter = None
_initialized_mcp_tools: List[BaseTool] = []

# def ensure_mcp_config():
#     """Ensure the MCP configuration file exists with proper structure."""
#     config_path = Path("browser_mcp.json")
#     if not config_path.exists():
#         default_config = {
#             "mcpServers": {
#                 "openmemory": {
#                     "type": "stdio",
#                     "command": "npx",
#                     "args": ["-y", "openmemory"],
#                     "env": {
#                         "OPENMEMORY_API_KEY": "om-g9w12cm6ssfqrx3w9oei9tion4bs7yar",
#                         "CLIENT_NAME": "openmemory"
#                     }
#                 },
#                 "zapier": {
#                     "url": "https://mcp.zapier.com/api/mcp/s/YWVlMTMwY2UtMzk3ZS00ZTExLWI4ODUtNTEyMWZiMjVhOTY0OjYyODAxMTVkLTZkMDctNDNlNS05ZjM5LTU5NmU4ZTFhNzgxNg==/sse"
#                     }
#             }
#         }
#         with open(config_path, 'w') as f:
#             json.dump(default_config, f, indent=2)
#     return config_path

async def initialize_and_get_mcp_tools() -> List[BaseTool]:
    """
    Initializes the MCPClient and LangChainAdapter to create and return
    the raw list of Zapier tools directly. This function should be called once.
    """
    global _mcp_client, _mcp_adapter, _initialized_mcp_tools

    # If MCP is not available, return empty list
    if not MCP_AVAILABLE:
        print("MCP tools not available. Continuing without MCP functionality.")
        return []

    if not _initialized_mcp_tools:
        print("Initializing MCP Client and getting raw Zapier tools...")
        
        try:
            # Ensure config file exists
            config_path = r"C:\Users\Surya Narayanan K V\OS_AGENT\browser_mcp.json"
            
            # Load and validate config
            # with open(config_path, 'r') as f:
            #     config = json.load(f)
            
            # # Ensure proper configuration
            # if "mcpServers" not in config:
            #     print("Warning: Invalid MCP configuration: missing mcpServers")
            #     return []
                
            # for server_name, server_config in config["mcpServers"].items():
            #     if "type" not in server_config:
            #         print(f"Warning: Invalid server configuration for {server_name}: missing type")
            #         return []
            #     if "command" not in server_config:
            #         print(f"Warning: Invalid server configuration for {server_name}: missing command")
            #         return []
            
            # # Save updated config
            # with open(config_path, 'w') as f:
            #     json.dump(config, f, indent=2)
            
            _mcp_client = MCPClient.from_config_file(config_path)
            _mcp_adapter = LangChainAdapter()
            _initialized_mcp_tools = await _mcp_adapter.create_tools(_mcp_client)
            print(f"Discovered {len(_initialized_mcp_tools)} Zapier tools.")
        except Exception as e:
            print(f"Error initializing MCP tools: {e}")
            # Return empty list if initialization fails
            return []
            
    return _initialized_mcp_tools



