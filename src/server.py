from mcp.server.fastmcp import FastMCP
from tools.github import GitHubTools
import argparse

mcp = FastMCP(
    name="GitHub Repository Agent",
    instructions="""
        This server provides GitHub repository analysis tools.
        """
)

@mcp.tool()
async def get_github_repo_info() -> str:
    """Load information about the GitHub repository"""
    return await github_tools.get_repo_info()

@mcp.tool()
async def get_github_repo_tree() -> str:
    """Load the directory structure of the GitHub repository"""
    return await github_tools.get_repo_tree()

@mcp.tool()
async def get_github_repo_code(file_path: str) -> str:
    """Load the content of a file in the GitHub repository"""
    return await github_tools.get_repo_code(file_path)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-owner", type=str, required=True)
    parser.add_argument("--repo-name", type=str, required=True)
    args = parser.parse_args()
    
    github_tools = GitHubTools(args.repo_owner, args.repo_name)

    # Use 'mcp dev src/server.py' to start MCP Inspector
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error: {e}")