from fastapi import APIRouter, HTTPException
from pydantic import AnyHttpUrl, BaseModel
from celery.result import AsyncResult

from app.celery_app import celery_app
from app.tasks.parser_tasks import parse_url_task


router = APIRouter()


class ParseQueueRequest(BaseModel):
    url: AnyHttpUrl


@router.post("/queue")
async def enqueue_parser_task(request: ParseQueueRequest) -> dict:
    task = parse_url_task.delay(str(request.url))

    return {
        "task_id": task.id,
        "status": "queued",
    }


@router.get("/queue/{task_id}")
async def get_parser_task_status(task_id: str) -> dict:
    task_result = AsyncResult(task_id, app=celery_app)

    response = {
        "task_id": task_id,
        "status": task_result.status,
    }

    if task_result.successful():
        response["result"] = task_result.result

    if task_result.failed():
        response["error"] = str(task_result.result)

    return response