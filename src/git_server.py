from mcp.server.fastmcp import FastMCP
from openai import OpenAI
from typing import Any
from dotenv import load_dotenv
import argparse
import os
import httpx
import ast
import esprima
import json
import ast
import subprocess
import asyncio 
from tools.git_tools import GitHubAnalyzer, Dict
from ollama import ChatResponse, chat
import ollama
from pathlib import Path

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

mcp = FastMCP(
    name="Git Server",
    instructions="""
        This server provides GitHub repository analysis tools.
        """
)

client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")
    
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