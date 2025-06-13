from mcp.server.fastmcp import FastMCP
from tools.github_analyzer import GitHubAnalyzer
from typing import Dict

mcp = FastMCP(
    name="GitHub MCP Server",
    instructions="""
        This server provides GitHub repository analysis tools.
        """
)

github_analyzer = GitHubAnalyzer()

@mcp.tool()
async def get_github_repository_tree(repo_owner: str, repo_name: str) -> Dict:
    """Load the directory structure of the GitHub repository"""
    return await github_analyzer.get_repository_tree(repo_owner, repo_name)

@mcp.tool()
async def get_github_api_endpoints(file_path: str) -> Dict:
    """Load all API endpoints information from a file in the GitHub repository"""
    return await github_analyzer.get_api_endpoints_from_code(file_path)

if __name__ == "__main__":
    # Use 'mcp dev github/server.py' to start MCP Inspector
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error: {e}")