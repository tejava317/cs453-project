import uuid
import asyncio
import os
from mcp.server.fastmcp import FastMCP

# Import the tool(s)
from tools.run_jest_tests import run_jest_tests

mcp = FastMCP("automated-api-testing-server")

jobs = {}

@mcp.tool()
async def start_jest_job(jest_code: str) -> str:
    job_id = str(uuid.uuid4())
    jobs[job_id] = {"status": "pending", "result": None, "error": None}

    # 현재 파일(server.py) 기준으로 job_dir 생성
    base_dir = os.path.dirname(os.path.abspath(__file__))
    job_dir = os.path.join(base_dir, job_id)
    os.makedirs(job_dir, exist_ok=True)
    asyncio.create_task(_run_jest_job(job_id, jest_code, job_dir))
    return job_id

async def _run_jest_job(job_id, jest_code, job_dir):
    jobs[job_id]["status"] = "running"
    try:
        result = await run_jest_tests(jest_code, job_dir=job_dir)
        jobs[job_id]["status"] = "done"
        jobs[job_id]["result"] = result
    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)

@mcp.tool()
async def get_jest_job_status(job_id: str) -> dict:
    job = jobs.get(job_id)
    if not job:
        return {"status": "not_found"}
    return job

if __name__ == "__main__":
    mcp.run(transport='stdio') 