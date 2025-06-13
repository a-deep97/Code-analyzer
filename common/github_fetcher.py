import os
import shutil
import tempfile
from git import Repo

def clone_github_repo(repo_url: str) -> str:
    temp_dir = tempfile.mkdtemp()
    Repo.clone_from(repo_url, temp_dir)
    return temp_dir
