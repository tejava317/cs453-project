from dotenv import load_dotenv
import os
import httpx

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env')
load_dotenv(dotenv_path)

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

headers = {
    "Authorization": f"Bearer {GITHUB_API_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

async def get_user_info(username: str) -> str:
    url = f"https://api.github.com/users/{username}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        response.raise_for_status()
        return response.json()