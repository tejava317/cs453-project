from mcp.server.fastmcp import FastMCP

# Import the tool(s)
from tools.run_jest_tests import run_jest_tests

mcp = FastMCP("automated-api-testing-server")

@mcp.tool()
async def call_run_jest_tests(jest_code: str) -> str:
    return await run_jest_tests(jest_code)

if __name__ == "__main__":
    mcp.run(transport='stdio') 