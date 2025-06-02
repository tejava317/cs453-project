import asyncio
from tools.run_jest_tests import run_jest_tests

# example.test.js 파일 내용 읽기
with open("example.test.js", "r", encoding="utf-8") as f:
    jest_code = f.read()

# Jest 테스트 실행 (비동기)
result = asyncio.run(run_jest_tests(jest_code))

# 결과 출력
print(result)