from typing import Any
import httpx
import ast

from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("ASTParser")

@mcp.tool()
def get_ast_tree(code: str):
    """Get ast tree of given code.
    Args:
        code (str): code script.
    """
    return ast.parse(code)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')