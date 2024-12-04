from fastapi import APIRouter, BackgroundTasks, Request, Depends, HTTPException
from app.github_utils import validate_signature
from app.tasks import analyze_pr_task
from app.models import get_results
from celery_app import celery_app
from celery.result import AsyncResult
from slowapi import Limiter
from slowapi.util import get_remote_address

import os
from dotenv import load_dotenv
load_dotenv()

WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")

router = APIRouter()

limiter = Limiter(key_func=get_remote_address)

@router.post("/analyze-pr")
@limiter.limit("5/minute")
async def analyze_pr(
    request: Request,
    payload: dict,
    background_tasks: BackgroundTasks
):
    repo_url = payload["repo_url"]
    pr_number = payload["pr_number"]
    github_token = payload.get("github_token")
    
    # Start analysis task
    task = analyze_pr_task.delay(repo_url, pr_number, github_token)
    return {"task_id": task.id}

@router.get("/status/{task_id}")
async def get_status(task_id: str):
    result = AsyncResult(task_id, app=celery_app)
    return {"task_id": task_id, "status": result.status}

@router.get("/results/{pr_number}")
async def get_results_endpoint(repo_url: str, pr_number: int):
    results = get_results(repo_url, pr_number)
    if not results:
        return {"message": "Results not found or analysis in progress."}
    return {"results": results}

@router.post("/webhook")
async def github_webhook(request: Request):
    # Validate webhook signature
    signature = request.headers.get("X-Hub-Signature-256")
    if not await validate_signature(request, signature, WEBHOOK_SECRET):
        raise HTTPException(status_code=403, detail="Invalid signature")

    payload = await request.json()
    action = payload.get("action")
    pull_request = payload.get("pull_request")

    if action in ["opened", "synchronize"]:
        repo_url = payload["repository"]["html_url"]
        pr_number = pull_request["number"]

        # Log the event
        print(f"Webhook received: action={action}, repo={repo_url}, PR={pr_number}")

        # Trigger the Celery task
        analyze_pr_task.delay(repo_url, pr_number)

    return {"message": "Webhook processed successfully"}