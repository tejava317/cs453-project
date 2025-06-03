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

async def run_jest_tests(jest_code: str, job_id: str, job_dir: str, jobs: dict, base_dir: str) -> None:
    jobs[job_id]["status"] = "running"
    
    test_file = os.path.join(job_dir, "temp_jest_test.test.js")
    log_file = os.path.join(job_dir, "run_jest_tests.log")
    
    logger = get_job_logger(log_file)
    
    try:
        logger.debug(f"Opening test file {test_file} for writing.")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(jest_code)
        logger.debug(f"Successfully wrote jest code to {test_file}.")
        
        logger.debug("Starting subprocess...")
        proc = await asyncio.create_subprocess_exec(
            "npx.cmd", "jest", "--json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=base_dir
        )
        logger.debug("Subprocess started, waiting for result...")
        stdout, stderr = await proc.communicate()
        logger.debug("Subprocess finished.")
        
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
    # 폴더는 삭제하지 않고 남겨둠 (필요시 shutil.rmtree(job_dir)로 정리 가능) 