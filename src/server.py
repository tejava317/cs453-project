from mcp.server.fastmcp import FastMCP
from tools.github import RepositoryAnalyzer

mcp = FastMCP(
    name="GitHub Repository Agent",
    instructions="""
        This server provides GitHub repository analysis tools.
        """
)

repository_analyzer =  RepositoryAnalyzer()

@mcp.tool()
def load_repository(repo_owner: str, repo_name: str) -> str:
    """Load information about a GitHub repository"""
    return repository_analyzer.load_documents(repo_owner, repo_name)

if __name__ == "__main__":
    # Use 'mcp dev src/server.py' to start MCP Inspector
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error: {e}")