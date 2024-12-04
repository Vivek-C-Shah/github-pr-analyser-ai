import hashlib
import hmac
from fastapi import Request
import requests

def fetch_pr_files(repo_url, pr_number, github_token=None):
    owner, repo = repo_url.replace("https://github.com/", "").split("/")
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    
    headers = {"Authorization": f"Bearer {github_token}"} if github_token else {}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch PR files: {response.status_code}")
    
    return response.json()

def fetch_file_content(raw_url, github_token=None):
    headers = {"Authorization": f"Bearer {github_token}"} if github_token else {}
    response = requests.get(raw_url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch file content: {response.status_code}")
    
    return response.text

def process_pr_files(repo_url, pr_number, github_token=None):
    files = fetch_pr_files(repo_url, pr_number, github_token)
    file_contents = []
    for file_info in files:
        filename = file_info["filename"]
        if is_code_file(filename):
            raw_url = file_info.get("raw_url")
            if raw_url:
                content = fetch_file_content(raw_url, github_token)
                file_contents.append({"filename": filename, "content": content})
        else:
            print(f"Skipping non-code file: {filename}")
    return file_contents

def is_code_file(filename):
    code_extensions = ['.py', '.js', '.java', '.go', '.cpp', '.c', '.cs', '.rb', '.php', '.html', '.css', '.ts', '.rs', '.kt', '.swift']
    return any(filename.endswith(ext) for ext in code_extensions)

async def validate_signature(request: Request, signature: str, secret: str) -> bool:
    if not signature:
        return False
    body = await request.body()
    computed_signature = f"sha256={hmac.new(secret.encode(), body, hashlib.sha256).hexdigest()}"
    return hmac.compare_digest(computed_signature, signature)
