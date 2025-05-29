from typing import Any
import httpx
import ast

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("ASTParser")

@mcp.tool()
def analyze(code: str):
    """Anaylyze the code
    Args:
        code (str): code script.
    """
    return code

@mcp.tool()
def generate_test(analysis: str):
    """Anaylyze the code
    Args:
        analysis (str): analysis (e.g. code)
    """
    test_code = analysis
    return test_code

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')