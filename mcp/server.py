#!/usr/bin/env python3
"""
Browser Automation MCP Server
Exposes browser automation capabilities via Model Context Protocol

Modular architecture with separate tool definitions and handlers
"""

import asyncio
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio

from config import SERVER_NAME, SERVER_VERSION
from tools import get_all_tools
from handlers import handle_tool
from utils import get_client

# Create server instance
server = Server(SERVER_NAME)


@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available browser automation tools"""
    return get_all_tools()


@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """Handle tool execution requests"""
    
    if arguments is None:
        arguments = {}
    
    try:
        return await handle_tool(name, arguments)
    except Exception as e:
        return [types.TextContent(
            type="text",
            text=f"❌ Error executing {name}: {str(e)}"
        )]


async def main():
    """Run the MCP server"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name=SERVER_NAME,
                server_version=SERVER_VERSION,
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        )


async def cleanup():
    """Cleanup resources"""
    client = get_client()
    await client.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer stopped")
    finally:
        asyncio.run(cleanup())
