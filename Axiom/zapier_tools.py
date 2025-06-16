# zapier_tools.py
import asyncio
import os
from mcp_use.client import MCPClient
from mcp_use.adapters import LangChainAdapter
from dotenv import load_dotenv
from typing import List
from langchain_core.tools import BaseTool # Import BaseTool type for clarity

load_dotenv()

_mcp_client = None
_mcp_adapter = None
_initialized_mcp_tools: List[BaseTool] = [] 

async def initialize_and_get_mcp_tools() -> List[BaseTool]:
    """
    Initializes the MCPClient and LangChainAdapter to create and return
    the raw list of Zapier tools directly. This function should be called once.
    """
    global _mcp_client, _mcp_adapter, _initialized_mcp_tools

    if not _initialized_mcp_tools:
        print("Initializing MCP Client and getting raw Zapier tools...")
        _mcp_client = MCPClient.from_config_file(os.path.join("browser_mcp.json"))
        _mcp_adapter = LangChainAdapter()
        _initialized_mcp_tools = await _mcp_adapter.create_tools(_mcp_client)
        print(f"Discovered {len(_initialized_mcp_tools)} Zapier tools.")
    return _initialized_mcp_tools



