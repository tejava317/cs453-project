import asyncio
import os
import traceback
import logging

# 로깅 설정
logging.basicConfig(filename='run_jest_tests.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

async def run_jest_tests(jest_code: str) -> str:
    test_file = "temp_jest_test.test.js"
    try:
        logging.debug(f"Opening test file {test_file} for writing.")
        with open(test_file, "w", encoding="utf-8") as f:
            f.write(jest_code)
        logging.debug(f"Successfully wrote jest code to {test_file}.")

        logging.debug("Starting subprocess...")
        proc = await asyncio.create_subprocess_exec(
            "npx.cmd", "jest", test_file, "--json",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
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
    finally:
        try:
            os.remove(test_file)
        except Exception as e:
            logging.warning(f"Failed to remove temp file: {e}") 