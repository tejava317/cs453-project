from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from test_generator_function import _test_and_repeat, generate_test_code
from typing import Dict, Optional

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

mcp = FastMCP(
    name="Test Generator MCP Server",
    instructions="""
        This server provides test code generation and execution tools.
        """
)

@mcp.tool()
async def test_and_repeat(code_path:str, test_code_path:str, save_code_path:str) -> Dict:
    """execute test code and return test result."""
    """
    Args:
        code_path: must be absolute path, where the target code is saved.
        test_code_path: must be absolute path, the file path of test code to be saved.
        save_code_path: must be absolute path where syntatically modified test_code is saved
    """
    return _test_and_repeat(code_path, test_code_path, save_code_path)

@mcp.tool()
async def generate_test_code_from_openapi_spec(openapi_spec:Dict) -> str:
    """Generate test from given raw code, code's file path, and directory tree.
    Args:
        openapi_spec: The open api specification information, which is necessary.
    """
    return generate_test_code(openapi_spec)

if __name__ == "__main__":
    try:
        mcp.run(transport="stdio")
        print("Test Suite Generator MCP Server is running")
    except Exception as e:
        print(f"Error: {e}")