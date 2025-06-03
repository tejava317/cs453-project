import asyncio
import os
import traceback
import logging

def get_job_logger(log_file):
    logger = logging.getLogger(log_file)
    logger.setLevel(logging.DEBUG)
    if not logger.handlers:
        handler = logging.FileHandler(log_file, encoding='utf-8')
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger

async def run_jest_tests(base_dir: str, log_dir: str, job_id: str, jobs: dict) -> None:
    jobs[job_id]["status"] = "running"
    
    log_file = os.path.join(log_dir, "run_jest_tests.log")
    logger = get_job_logger(log_file)
    
    try:
        if not os.path.isdir(base_dir):
            raise FileNotFoundError(f"base_dir does not exist: {base_dir}")
        
        logger.debug(f"Starting Jest for all tests in base_dir: {base_dir}")
        
        npx_command = "npx.cmd" if os.name == "nt" else "npx"
        proc = await asyncio.create_subprocess_exec(
            npx_command, "jest", "--json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=base_dir
        )
        
        logger.debug("Jest started, waiting for result...")
        stdout, stderr = await proc.communicate()
        logger.debug("Jest finished.")
        
        if proc.returncode == 0:
            jobs[job_id]["status"] = "done"
            jobs[job_id]["result"] = stdout.decode("utf-8")
        else:
            jobs[job_id]["status"] = "done"
            jobs[job_id]["result"] = stderr.decode("utf-8") or stdout.decode("utf-8")
    
    except Exception as e:
        tb = traceback.format_exc()
        logger.error("Exception occurred: %s\n%s", e, tb)
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = f"Exception: {e}\nTraceback:\n{tb}"
    # 폴더는 삭제하지 않고 남겨둠 (필요시 shutil.rmtree(log_dir)로 정리 가능) 