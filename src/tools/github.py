from dotenv import load_dotenv
import os
import httpx
import base64

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env')
load_dotenv(dotenv_path)

GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

class GitHubTools:
    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {GITHUB_API_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.username = ""
        self.repo_owner = ""
        self.repo_name = ""
    
    async def get_user_info(self, username: str) -> str:
        self.username = username
        url = f"https://api.github.com/users/{self.username}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_repo_info(self, repo_owner: str, repo_name: str) -> str:
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    # async def get_code_content(self, file_path: str) -> str:
    #     url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(url, headers=self.headers)
    #         response.raise_for_status()
    #         data = response.json()
    #         content = base64.b64decode(data['content']).decode('utf-8')
    #         return content