from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="GitHub Repository Agent",
    instructions="""
        This server provides GitHub repository analysis tools.
        """
)

@mcp.tool()
async def greet(name: str) -> str:
    """Greet the client"""
    return f"Hello, {name}!"

if __name__ == "__main__":
    # Use 'mcp dev src/server.py' to start MCP Inspector
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error: {e}")