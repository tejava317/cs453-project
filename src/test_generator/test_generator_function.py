import os
from ollama import chat
from ollama import ChatResponse
import ollama
from pathlib import Path
import json
from typing import Dict

model = 'qwen3:8b'
MAX_ITER = 10

def extract_code_from_response(response):
    beginIndex = response.find('javascript') + len('javascript') 
    response = response[beginIndex:]
    return response[:response.find('```')]

def query(code, test_code, json_content) -> str:
    """Query the LLM with the given prompt."""
    prompt = f"""
I executed below test code\n{test_code} and the result are as below,\n 
{json.dumps(json_content, indent=2)}\n
The original target code is {code}
If some test cases do not pass, then modify them properly. \n
Also, add as many as possible test cases that is not in the original test suite.
Give me modified TOTAL code, which must not be shorten and can be executable.\n
"""
    response: ChatResponse = chat(
    model=model,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    )
    return response.message.content

def _test_and_repeat(code_path: str, test_code_path: str, save_code_path: str):
    ollama.pull(model)
    """execute test code and return test result."""
    """test_code_path must be absolute path."""
    """save_code_path: must be absolute path where syntatically modified test_code is saved"""
    if not test_code_path.endswith('.test.js') or not not test_code_path.endswith('.test.ts'):
        return "The test_code_path is not valid. It must ends with .test.js or .test.ts"
    if not save_code_path.endswith('.test.js') or not save_code_path.endswith('.test.ts'):
        return "The save path must ends with .test.js or .test.ts"
    if not code_path.endswith('.js') or not code_path.endswith('.ts'):
        return "The code path must ends with .js or .ts"
    if code_path == test_code_path:
        return "The three paths must be mutually different."
    if test_code_path == save_code_path:
        return "Both file paths must be differnet."
    code = ''
    with open(code_path, 'r') as f:
        code = f.read()
    test_code_path = Path(test_code_path)
    save_code_path = Path(save_code_path)
    save_json_path = save_code_path.with_suffix('.json')
    test_code = None
    with open(test_code_path, 'r') as f:
        test_code = f.read()
    with open(save_code_path, 'w') as f:
        f.write(test_code)
    for i in range(MAX_ITER):
        command = f"npx.cmd jest --runTestsByPath {save_code_path} --json --outputFile {save_json_path} --coverage"
        os.system(f'start /wait cmd /c "{command}"')
        json_content = None
        with open(save_json_path, 'r', encoding='utf-8') as f:
            json_content = f.read()
            
        response = query(code, test_code, json_content)
        test_code = extract_code_from_response(response)
        # code_start = content.find('javascript')+len('javascript')
        with open(save_code_path, 'w') as f:
            f.write(test_code)
    return "done"

def generate_test_code(openapi_spec:Dict) -> str:
    
    openapi_spec_str = json.dumps(openapi_spec, indent=2)

    prompt = (
            "Crate a good jest test code based on the openapi spec. Test code must cover all the endpoints in the openapi spec. Test code must cover all the possible cases, edge cases and unexpected cases."
            f"openapi spec: {openapi_spec_str}"
    )
    
    response: ChatResponse = chat(
    model=model,
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    )
    response = extract_code_from_response(response.message.content)
    
    return response

# if __name__ == "__main__":
    # test_code_path = 'C:/github/cs453-project/src/tools/funtion.generated.test.js'
    #save_code_path = 'C:/github/cs453-project/src/tools/funtion.generated_result.test.js'
    # _test_and_repeat(test_code_path, save_code_path)
    # code_path = 'C:/github/cs453-project/funtion.js'
    # code = None
    # with open(code_path, 'r') as f:
    #     code = f.read()