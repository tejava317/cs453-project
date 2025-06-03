import asyncio
import os
from server import start_jest_job, get_jest_job_status

async def main():
    # 1. 작업 예약
    base_dir = os.path.dirname(os.path.abspath(__file__))
    job_id = await start_jest_job(base_dir)
    print(f"Job started. job_id={job_id}")

    # 2. 폴링으로 상태 확인
    while True:
        status = await get_jest_job_status(job_id)
        print(f"Current status: {status['status']}")
        if status["status"] == "done":
            print("Result:")
            print(status["result"])
            break
        elif status["status"] == "error":
            print("Error:")
            print(status["error"])
            break
        await asyncio.sleep(1)  # 1초마다 폴링

if __name__ == "__main__":
    asyncio.run(main())