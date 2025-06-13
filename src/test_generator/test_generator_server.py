from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from test_generator_function import _test_and_repeat, _generate_test_from_raw_code

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

mcp = FastMCP(
    name="Test Suite Generator",
    instructions="""
        This server provides tools that generates test cases and validate test cases.
        """
)

@mcp.tool()
def test_and_repeat(code_path:str, test_code_path: str, save_code_path: str):
    """execute test code and return test result."""
    """
    Args:
        code_path: must be absolute path, where the target code is saved.
        test_code_path: must be absolute path, the file path of test code to be saved.
        save_code_path: must be absolute path where syntatically modified test_code is saved
    """
    return _test_and_repeat(code_path, test_code_path, save_code_path)

@mcp.tool()
def generate_test_from_raw_code(code_file_path:str, test_code_path:str, openapi_spec:str) -> str:
    """Generate test from given raw code, code's file path, and directory tree.
    Args:
        code_file_path: the file path of code
        test_code_path: the file path of test code to be saved.
        openapi_spec: The whole open api specification information, which is necessary.
    """
    # Here you would implement logic to generate a test based on the analysis
    # For simplicity, we will just return the analysis as the test code
    return _generate_test_from_raw_code(code_file_path, test_code_path, openapi_spec)

if __name__ == "__main__":
    # Use 'mcp dev github/server.py' to start MCP Inspector
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error: {e}")