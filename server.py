import uuid
import asyncio
import os
from mcp.server.fastmcp import FastMCP

from tools.run_jest_tests import run_jest_tests

mcp = FastMCP("automated-api-testing-server")

# 작업 상태를 저장할 딕셔너리
jobs = {}

# 작업 시작 툴
@mcp.tool()
async def start_jest_job(base_dir: str) -> str:
    # 작업 ID 생성
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "result": None, "error": None}

    # 작업 디렉토리 생성 (로그 등 저장용)
    log_dir = os.path.join(base_dir, ".mcp-logs", job_id)
    os.makedirs(log_dir, exist_ok=True)
    
    # 작업 실행 함수 호출
    asyncio.create_task(run_jest_tests(base_dir, log_dir, job_id, jobs))
    
    return job_id

# 작업 상태 조회 툴
@mcp.tool()
async def get_jest_job_status(job_id: str) -> dict:
    job = jobs.get(job_id)
    if not job:
        return {"status": "not_found"}
    return job

if __name__ == "__main__":
    mcp.run(transport='stdio') 