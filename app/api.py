from fastapi import APIRouter, BackgroundTasks
from app.tasks import analyze_pr_task
from app.models import get_results
from celery_app import celery_app
from celery.result import AsyncResult
router = APIRouter()

@router.post("/analyze-pr")
def analyze_pr(payload: dict, background_tasks: BackgroundTasks):
    repo_url = payload["repo_url"]
    pr_number = payload["pr_number"]
    github_token = payload.get("github_token")
    
    # Start analysis task
    task = analyze_pr_task.delay(repo_url, pr_number, github_token)
    return {"task_id": task.id}

@router.get("/status/{task_id}")
def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": result.status}

@router.get("/results/{pr_number}")
def get_results_endpoint(repo_url: str, pr_number: int):
    results = get_results(repo_url, pr_number)
    if not results:
        return {"message": "Results not found or analysis in progress."}
    return {"results": results}
