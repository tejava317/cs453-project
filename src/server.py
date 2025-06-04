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
def generate_test_from_raw_code(code:str, code_file_path:str, repo_tree:str) -> str:
    """Generate test from given raw code, code's file path, and directory tree.
    Args:
        code: raw code
        code_file_path: the file path of code
        repo_tree: the entire repo tree that contains the code file.
    """
    # Here you would implement logic to generate a test based on the analysis
    # For simplicity, we will just return the analysis as the test code
    if code_file_path.endswith('.py'):
        try:
            root = ast.parse(code)
            analysis = ast.dump(root, indent=4)
        except Exception as e:
            analysis = ''
    elif code_file_path.endswith('.js'):
        try:
            ast = esprima.parseModule(code)
            analysis = json.dumps(ast.toDict(), indent=2, ensure_ascii=False)
        except Exception as e:
            analysis = ''
    # process = subprocess.Popen(
    # "ollama run gemma3:4b",  
    # stdin=subprocess.PIPE,
    # stdout=subprocess.PIPE,
    # stderr=subprocess.PIPE,
    # text=True,  
    # bufsize=10,
    # encoding='utf-8'
    # )

    # user_input = f"code: {code}'\n---------------'\n' analysis:{analysis}, give me EXACT, PROPER, and VARIOUS test cases."
    # outs, errs = process.communicate(input=user_input, timeout=60)
    
    messages = [
    {
        "role": "system",
        "content": (
            "You MUST generate a test based on the analysis provided."
            "The test should be a as VARIOUS and EXACT as possible."
            "You must use the following format."
            "- test case name: <name of test case>"
            "- test code: <code of the test>"
        ),  
    },
    {   
        "role": "user",
        "content": (
            "Crate a good test code based on the analysis provided."
            f"analysis: {analysis}"
            f"code: {code}"
            f"current file paht: {code_file_path}"
            f"whole directory tree: {repo_tree}"
        ),
    },
    ]

    # chat completion without streaming
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    messages2 = [
    {
        "role": "system",
        "content": (
            "You are the validator the given test codes of the code and analysis."
            "You must solve potential complilation error by analyze the code line by line"
            "Particulary, focus on the IMPORT FILE PATH and "
        ),  
    },
    {   
        "role": "user",
        "content": (
            f"analyze these test cases {str(response)} and modify properly and add new test cases if possible."
            f"analysis: {analysis}"
            f"code: {code}"
            f"current file paht: {code_file_path}"
            f"whole directory tree: {repo_tree}"
        ),
    },
    ]
    # modify again.
    response2 = client.chat.completions.create(
        model="sonar-pro",
        messages=messages2,
    )
    return str(response2)

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