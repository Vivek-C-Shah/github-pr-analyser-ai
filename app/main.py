from fastapi.responses import JSONResponse
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.api import router
from app.models import init_db

# Initialize Limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI()

app.state.limiter = limiter

# Add SlowAPI middleware
app.add_middleware(SlowAPIMiddleware)

# Include API routes
app.include_router(router)

# Initialize the database
@app.on_event("startup")
def startup_event():
    init_db()

# Rate limit exception handler
@app.exception_handler(RateLimitExceeded)
async def rate_limit_exceeded_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"detail": f"Rate limit exceeded: {exc.detail}"}
    )
