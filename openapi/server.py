from mcp.server.fastmcp import FastMCP
from tools.openapi import generate_spec

mcp = FastMCP(
    name="OpenAPI Specification Generator",
    instructions="""
        This server generates OpenAPI specification based on GitHub repository.
        """
)

@mcp.tool()
async def generate_openapi_spec() -> str:
    """Generate OpenAPI specification JSON file"""
    return await generate_spec()

if __name__ == "__main__":
    # Use 'mcp dev openapi/server.py' to start MCP Inspector
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error: {e}")