from fastapi import FastAPI
from app.api import router
from app.models import init_db

app = FastAPI()

# Include API routes
app.include_router(router)

# Initialize the database
@app.on_event("startup")
def startup_event():
    init_db()
