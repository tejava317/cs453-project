import asyncio
import os
from ollama import chat
from ollama import ChatResponse
import ollama
model = 'gemma3'
MAX_ITER = 2

async def _execute_validate_test(test_code_path:str, save_path:str):
    test_code = None
    with open(test_code_path, 'r') as f:
        test_code = f.read()
    with open(save_path, 'w') as f:
        f.write(test_code)
    
    npx_command = "npx.cmd" if os.name == "nt" else "npx"
    for i in range(MAX_ITER):
        with open('log.txt', 'w') as f:
            f.write(f"{i}th iteration!")
        proc = await asyncio.create_subprocess_exec(
        npx_command, "jest", save_path,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await proc.communicate()
        if proc.returncode != 0:
            response: ChatResponse = chat(model=model, messages=[
            {
                'role': 'user',
                'content': f"""
                I executed below test code\n{test_code} \n but an error occurs,\n 
                stderr:{stderr.decode('utf-8')}\n
                Give me modified TOTAL code.\n
                The TOTAL code must not be shorten and can be executable.\n
                There must be nothing except for the code.
                """,
            },
            ])
            content = response.message.content
            with open(save_path, 'w') as f:
                f.write(content)  
        else:
            response: ChatResponse = chat(model=model, messages=[
            {
                'role': 'user',
                'content': f"""
                I executed below test code\n{test_code} and the result are as below,\n 
                {stdout.decode('utf-8')}\n
                Give me modified TOTAL code so that total test cases pass.\n
                The TOTAL code must not be shorten and can be executable.\n
                There must be nothing except for the code.
                """,
            },
            ])
            content = response.message.content
            with open(save_path, 'w') as f:
                f.write(content)
    return

if __name__ == "__main__":
    asyncio.create_task(_execute_validate_test('C:/github/Automated Software Testing/cs453-project/src/tools/funtion.generated.test.js', 
                                               'C:/github/Automated Software Testing/cs453-project/src/tools/funtion.generated_result.test.js'))