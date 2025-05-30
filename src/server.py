from mcp.server.fastmcp import FastMCP
from tools.github import GitHubTools

mcp = FastMCP(
    name="GitHub Repository Agent",
    instructions="""
        This server provides GitHub repository analysis tools.
        """
)

github_tools = GitHubTools()

@mcp.tool()
async def get_github_user_info(username: str) -> str:
    """Look up information about a GitHub user"""
    return await github_tools.get_user_info(username)

@mcp.tool()
async def get_github_repo_info(repo_owner: str, repo_name: str) -> str:
    """Look up information about a GitHub repository"""
    return await github_tools.get_repo_info(repo_owner, repo_name)

# @mcp.tool()
# async def get_github_code_content(file_path: str) -> str:
#     """Look up the content of a file in a GitHub repository"""
#     return await github_tools.get_code_content(file_path)

if __name__ == "__main__":
    # Use 'mcp dev src/server.py' to start MCP Inspector
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error: {e}")