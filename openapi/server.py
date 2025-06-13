from mcp.server.fastmcp import FastMCP
from tools.openapi import OpenAPISpecGenerator
from typing import Dict

mcp = FastMCP(
    name="OpenAPI Specification Generator",
    instructions="""
        This server generates OpenAPI specification based on GitHub repository.
        """
)

spec_generator = OpenAPISpecGenerator()

@mcp.tool()
async def generate_openapi_spec(code: str) -> Dict:
    """Generate OpenAPI specification JSON file"""
    return await spec_generator.generate_spec(code)

if __name__ == "__main__":
    # Use 'mcp dev openapi/server.py' to start MCP Inspector
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error: {e}")