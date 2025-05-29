from openai import OpenAI

from typing import Any
import httpx
import ast
import os
from mcp.server.fastmcp import FastMCP

API_KEY = os.getenv("PERPLEXITY_API_KEY")
# Initialize FastMCP server
mcp = FastMCP("perplexityAPI")
@mcp.tool()
def generate_test(analysis: str) -> str:
    """Generate a test based on the analysis.
    Args:
        analysis (str): Analysis of the code.
    """
    # Here you would implement logic to generate a test based on the analysis
    # For simplicity, we will just return the analysis as the test code
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
            "analysis: {analysis}"
        ),
    },
    ]
    # chat completion without streaming
    response = client.chat.completions.create(
        model="sonar-pro",
        messages=messages,
    )
    return response



if __name__ == "__main__":
    # Initialize and run the server
    client = OpenAI(api_key=API_KEY, base_url="https://api.perplexity.ai")
    mcp.run(transport='stdio')

# messages = [
#     {
#         "role": "system",
#         "content": (
#             "You are an artificial intelligence assistant and you need to "
#             "engage in a helpful, detailed, polite conversation with a user."
#         ),
#     },
#     {   
#         "role": "user",
#         "content": (
#             "How many stars are in the universe?"
#         ),
#     },
# ]

# client = OpenAI(api_key=YOUR_API_KEY, base_url="https://api.perplexity.ai")

# # chat completion without streaming
# response = client.chat.completions.create(
#     model="sonar-pro",
#     messages=messages,
# )
# print(response)

# # chat completion with streaming
# response_stream = client.chat.completions.create(
#     model="sonar-pro",
#     messages=messages,
#     stream=True,
# )
# for response in response_stream:
#     print(response)