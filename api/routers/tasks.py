from fastapi import APIRouter
from celery.result import AsyncResult
from core.celery_app import celery_app

router = APIRouter()


@router.get("/{task_id}")
async def get_task_status(task_id: str):
    """Consulta o status de uma tarefa Celery pelo ID."""
    result = AsyncResult(task_id, app=celery_app)
    return {
        "task_id": task_id,
        "status": result.status,
        "result": result.result if result.ready() else None,
        "traceback": result.traceback if result.failed() else None,
    }


@router.delete("/{task_id}")
async def revoke_task(task_id: str):
    """Cancela uma tarefa em execução."""
    celery_app.control.revoke(task_id, terminate=True, signal="SIGTERM")
    return {"task_id": task_id, "message": "Tarefa cancelada"}
