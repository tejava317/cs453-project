import esprima
import subprocess

def generate_test(codepath:str) -> str:
    """Generate a test based on the analysis.
    Args:
        codepath: js script filepath
    """
    # Here you would implement logic to generate a test based on the analysis
    # For simplicity, we will just return the analysis as the test code
    code = None
    try:
        with open(codepath, 'r', encoding='utf-8') as f:
            code = f.read()
    except Exception as e:
        return str(e)
    analysis = esprima.parseScript(code)
    # analysis = code
    return analysis
  

process = subprocess.Popen(
    "ollama run gemma3:4b",  
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
    text=True,  # Python 3.7 이상에서 텍스트 모드 사용
    bufsize=10,
    encoding='utf-8' # 라인 단위 버퍼링
)

user_input = "what are you doing?"
outs, errs = process.communicate(input=user_input, timeout=10)
print(outs)


