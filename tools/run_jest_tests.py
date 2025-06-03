import asyncio
import os
import traceback
import logging
import uuid

async def run_jest_tests(jest_code: str, job_dir: str) -> str:
    # job_dir은 이미 생성되어 있다고 가정
    test_file = os.path.join(job_dir, "temp_jest_test.test.js")
    config_path = os.path.abspath("jest.config.js")  # 프로젝트 루트의 설정 파일 사용
    log_path = os.path.join(job_dir, "run_jest_tests.log")

    # 2. 로깅 설정 (job별로 로그 파일 분리)
    logging.basicConfig(filename=log_path, level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

    try:
        logging.debug(f"Opening test file {test_file} for writing.")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(jest_code)
        logging.debug(f"Successfully wrote jest code to {test_file}.")

        logging.debug(f"Actual cwd before subprocess: {os.getcwd()}")
        logging.debug(f"Config path: {config_path}, exists: {os.path.exists(config_path)}")
        logging.debug(f"Test file path: {test_file}, exists: {os.path.exists(test_file)}")
        logging.debug(f"Job dir: {job_dir}")

        logging.debug("Starting subprocess...")
        proc = await asyncio.create_subprocess_exec(
            "npx.cmd", "jest", test_file, "--json", "--config", config_path,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=job_dir
        )
        logging.debug("Subprocess started, waiting for result...")
        stdout, stderr = await proc.communicate()
        logging.debug("Subprocess finished.")
        logging.debug("stdout: %s", stdout.decode("utf-8"))
        logging.debug("stderr: %s", stderr.decode("utf-8"))
        if proc.returncode == 0:
            return stdout.decode("utf-8")
        else:
            return stderr.decode("utf-8") or stdout.decode("utf-8")
    except Exception as e:
        tb = traceback.format_exc()
        logging.error("Exception occurred: %s\n%s", e, tb)
        return f"Exception: {e}\nTraceback:\n{tb}"
    # 폴더는 삭제하지 않고 남겨둠 (필요시 shutil.rmtree(job_dir)로 정리 가능) 