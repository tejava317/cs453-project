from mcp.server.fastmcp import FastMCP
from tools.github import GitHubTools
from openai import OpenAI
from typing import Any
from dotenv import load_dotenv
import subprocess
import argparse
import os
import httpx
import ast
import esprima
import json
import ast
import subprocess
import asyncio 
from utils.foo import _test_and_repeat, _generate_test_from_raw_code
from ollama import ChatResponse, chat
import ollama
from pathlib import Path

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

mcp = FastMCP(
    name="GitHub Repository Agent",
    instructions="""
        This server provides GitHub repository analysis tools.
        """
)

client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
    
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
async def get_github_repo_info() -> str:
    """Load information about the GitHub remote repository"""
    return await github_tools.get_repo_info()

@mcp.tool()
async def get_github_repo_tree() -> str:
    """Load information about the GitHub remote repository"""
    return await github_tools.get_repo_tree()

@mcp.tool()
async def get_github_repo_code(file_path: str) -> str:
    """Load information about the GitHub remote repository"""
    return await github_tools.get_repo_code(file_path)
    
@mcp.tool()
def generate_test_from_raw_code(code:str, code_file_path:str, test_code_path:str, repo_tree:str) -> str:
    """Generate test from given raw code, code's file path, and directory tree.
    Args:
        code: raw code
        code_file_path: the file path of code
        test_code_path: the file path of test code to be saved.
        repo_tree: the entire repo tree that contains the code file.
    """
    # Here you would implement logic to generate a test based on the analysis
    # For simplicity, we will just return the analysis as the test code
    return _generate_test_from_raw_code(code, code_file_path, test_code_path, repo_tree)

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
    