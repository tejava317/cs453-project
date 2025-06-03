from langchain_community.document_loaders import GitLoader
import tempfile
import shutil

class RepositoryAnalyzer:
    def __init__(self):
        self.repo_owner = ""
        self.repo_name = ""
        self.repo_path = None
        self.loader = None
        self.documents = None
        self.valid_file_extensions = [".js", ".ts", ".jsx", ".tsx"]  # TODO: Add more file extensions

    def load_documents(self, repo_owner, repo_name):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.repo_path = tempfile.mkdtemp()
        self.loader = GitLoader(
            clone_url=f"https://github.com/{self.repo_owner}/{self.repo_name}",
            repo_path=self.repo_path,
            # file_filter=lambda x: x.endswith(tuple(self.valid_file_extensions)),
            branch="master"
        )
        self.documents = self.loader.load()
        shutil.rmtree(self.repo_path)
        return self.documents