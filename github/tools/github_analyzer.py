from github import Github, Auth
from dotenv import load_dotenv
from typing import Dict
from ollama import chat
from pydantic import BaseModel
import os
import base64

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env')
load_dotenv(dotenv_path)
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

auth = Auth.Token(GITHUB_ACCESS_TOKEN) if GITHUB_ACCESS_TOKEN else None
g = Github(auth=auth)

class Endpoint(BaseModel):
    endpoints: list[str]

class APISpec(BaseModel):
    endpoint_name: str
    params: list[Dict]
    returns: list[Dict]
    code: str

class GitHubAnalyzer:
    def __init__(self):
        self.repo_owner = ""
        self.repo_name = ""
        self.repo = None
        self.default_branch = ""
        self.repo_tree = {}
        self.model = 'qwen3:8b'
    
    async def get_repository_tree(self, repo_owner, repo_name) -> Dict:
        self.repo_owner = repo_owner
        self.repo_name = repo_name

        try:
            self.repo = g.get_repo(f"{self.repo_owner}/{self.repo_name}")

            self.default_branch = self.repo.default_branch
            tree = self.repo.get_git_tree(self.default_branch, recursive=True)

            tree_data = {
                "repository": f"{self.repo_owner}/{self.repo_name}",
                "branch": self.default_branch,
                "tree": []
            }

            for item in tree.tree:
                tree_data["tree"].append({
                    "path": item.path
                })
            
            self.repo_tree = tree_data
            return self.repo_tree
        
        except Exception as e:
            return {"error": str(e)}
    
    async def get_api_endpoints_from_code(self, file_path: str) -> Dict:
        try:
            file_content = self.repo.get_contents(file_path, ref=self.default_branch)

            if file_content.encoding == 'base64':
                code = base64.b64decode(file_content.content).decode('utf-8')
            else:
                code = file_content.content

            response = chat(
                messages=[{
                    'role': 'user',
                    'content': f'Extract all API endpoint names defined in the following code: {code}'
                }],
                model=self.model,
                format=Endpoint.model_json_schema(),
            )
            endpoints = Endpoint.model_validate_json(response.message.content)

            api_specs = {}
            for endpoint in endpoints.endpoints:
                response = chat(
                    messages=[{
                        'role': 'user',
                        'content': f'Analyze the {endpoint} endpoint implementation in the following code: {code}'
                    }],
                    model=self.model,
                    format=APISpec.model_json_schema(),
                )
                api_specs[endpoint] = APISpec.model_validate_json(response.message.content)

            return api_specs
            
        except Exception as e:
            return {"error": str(e)}