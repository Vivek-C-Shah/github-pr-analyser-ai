from celery_app import celery_app
from app.github_utils import process_pr_files
from app.ai_utils import analyze_code_with_openai
from app.models import store_results

@celery_app.task
def analyze_pr_task(repo_url, pr_number, github_token):
    try:
        # Fetch files from GitHub PR
        file_contents = process_pr_files(repo_url, pr_number, github_token)
        
        # Analyze files
        analysis_results = []
        for file in file_contents:
            filename = file["filename"]
            content = file["content"]
            result = analyze_code_with_openai(filename, content)
            analysis_results.append({"filename": filename, "issues": result})
        
        # Store results in the database
        store_results(repo_url, pr_number, analysis_results)
    
    except Exception as e:
        raise Exception(f"Analysis failed: {str(e)}")
