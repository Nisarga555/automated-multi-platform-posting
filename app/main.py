
from fastapi import FastAPI

from app.schemas import PostingRequest, PostingResponse
from app.services.posting_service import publish_message


app = FastAPI(
    title="AutoPostHub",
    description="Automated Multi-Platform Posting System",
    version="1.0.0"
)


@app.get("/")
async def home():
    return {
        "message": "Welcome to AutoPostHub",
        "status": "Running"
    }


@app.post(
    "/postingRequest",
    response_model=PostingResponse
)
async def posting_request(request: PostingRequest):

    result = await publish_message(request.message)

    return result
