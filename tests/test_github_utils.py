import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env.test")

from app.github_utils import fetch_pr_files, fetch_file_content

def test_fetch_pr_files():
    files = fetch_pr_files("https://github.com/potpie-ai/potpie", 1, os.getenv("GH_PAT"))
    assert isinstance(files, list)

def test_fetch_file_content():
    content = fetch_file_content("https://raw.githubusercontent.com/potpie-ai/potpie/main/app/main.py", os.getenv("GH_PAT"))
    assert isinstance(content, str)