from github import Github, Auth
from dotenv import load_dotenv
from typing import Dict
import os

dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '..', '.env')
load_dotenv(dotenv_path)
GITHUB_ACCESS_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

auth = Auth.Token(GITHUB_ACCESS_TOKEN) if GITHUB_ACCESS_TOKEN else None
g = Github(auth=auth)

class GitHubAnalyzer:
    def __init__(self):
        self.repo_owner = ""
        self.repo_name = ""
        self.repo = None
        self.default_branch = ""
        self.repo_tree = {}
    
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
    
    async def get_file_content(self, file_path: str) -> Dict:
        try:
            file_content = self.repo.get_contents(file_path, ref=self.default_branch)

            return {
                "file_path": file_path,
                "content": file_content.content
            }
            
        except Exception as e:
            return {"error": str(e)}