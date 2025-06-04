from mcp.server.fastmcp import FastMCP
from tools.github import RepositoryAnalyzer
from openai import OpenAI
from typing import Any
from dotenv import load_dotenv
import subprocess
import os
import httpx
import ast
import esprima
import json

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")

mcp = FastMCP(
    name="GitHub Repository Agent",
    instructions="""
        This server provides GitHub repository analysis tools.
        """
)

repository_analyzer =  RepositoryAnalyzer()
client = OpenAI(api_key=PERPLEXITY_API_KEY, base_url="https://api.perplexity.ai")

@mcp.tool()
def load_repository(repo_owner: str, repo_name: str) -> str:
    """Load information about a GitHub repository"""
    return repository_analyzer.load_documents(repo_owner, repo_name)

@mcp.tool()
def generate_test(codepath:str) -> str:
    """Generate a test of the given file path.
    Args:
        codepath: javascript file path.
    """
    # Here you would implement logic to generate a test based on the analysis
    # For simplicity, we will just return the analysis as the test code
    code = None
    try:
        with open(codepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        return "Invalid file path."
    try:
        ast = esprima.parseModule(code)
        analysis = json.dumps(ast.toDict(), indent=2, ensure_ascii=False)
    except Exception as e:
        return f"invalid java script code:{code}, this code cannot be parsed."
    
    # process = subprocess.Popen(
    # "ollama run gemma3:4b",  
    # stdin=subprocess.PIPE,
    # stdout=subprocess.PIPE,
    # stderr=subprocess.PIPE,
    # text=True,  # Python 3.7 이상에서 텍스트 모드 사용
    # bufsize=10,
    # encoding='utf-8' # 라인 단위 버퍼링
    # )

    user_input = f"code: {code}'\n---------------'\n' analysis:{analysis}, give me EXACT, PROPER, and VARIOUS test cases."
    # outs, errs = process.communicate(input=user_input, timeout=60)
    
    messages = [
    {
        "role": "system",
        "content": (
            "You are the best expert in code analysis and generation. "
            "You MUST generate a test based on the analysis provided."
            "The test should be a as VARIOUS as possible and EXACT."
            "You must use the following format."
            "- test case name: <name of test case>"
            "- test code: <code of the test>"
        ),  
    },
    {   
        "role": "user",
        "content": (
            "Please crate a good test code based on the analysis provided."
            f"analysis: {analysis}"
            f"code: {code}"
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
            "You are the best expert in code analysis and generation. "
            "You MUST generate a test based on the analysis provided."
            "The test should be a as VARIOUS as possible and EXACT."
            "You must use the following format."
            "- test case name: <name of test case>"
            "- test code: <code of the test>"
        ),  
    },
    {   
        "role": "user",
        "content": (
            f"analyze your previous response {str(response)} and modify properly, add new test cases."
            f"analysis: {analysis}"
            f"code: {code}"
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
    # Use 'mcp dev src/server.py' to start MCP Inspector
    try:
        mcp.run(transport="stdio")
    except Exception as e:
        print(f"Error: {e}")