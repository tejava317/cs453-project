from typing import Any
import httpx
import ast
import esprima
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("ASTParser")

@mcp.tool()
def analyze(code: str):
    """Anaylyze the code
    Args:
        analysis (str): analysis (e.g. code)
    """
    ast = esprima.parseScript(code)
    test_code = ast
    return test_code

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')