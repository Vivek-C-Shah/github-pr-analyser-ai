from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery(
    "code_review_agent",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["app.tasks"],
)

print(f"Using Redis URL: {REDIS_URL}")