import base64
import httpx
from dotenv import load_dotenv
import os

load_dotenv()
GITHUB_API_TOKEN = os.getenv("GITHUB_API_TOKEN")

class GitHubTools:
    def __init__(self, repo_owner: str, repo_name: str):
        self.headers = {
            "Authorization": f"Bearer {GITHUB_API_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo_tree = ""
    
    async def get_repo_info(self) -> str:
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
    
    async def get_repo_tree(self) -> str:
        # Get the default branch name
        repo_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}"
        async with httpx.AsyncClient() as client:
            repo_response = await client.get(repo_url, headers=self.headers)
            repo_response.raise_for_status()
            repo_data = repo_response.json()
            default_branch = repo_data["default_branch"]

            # Get the latest commit SHA of the default branch
            branch_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/branches/{default_branch}"
            branch_response = await client.get(branch_url, headers=self.headers)
            branch_response.raise_for_status()
            branch_data = branch_response.json()
            tree_sha = branch_data["commit"]["commit"]["tree"]["sha"]

            # Get the full tree recursively
            tree_url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/git/trees/{tree_sha}?recursive=1"
            tree_response = await client.get(tree_url, headers=self.headers)
            tree_response.raise_for_status()
            self.repo_tree = tree_response.json()
            return self.repo_tree
    
    async def get_repo_code(self, file_path: str) -> str:
        url = f"https://api.github.com/repos/{self.repo_owner}/{self.repo_name}/contents/{file_path}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            content = base64.b64decode(data['content']).decode('utf-8')
            return content