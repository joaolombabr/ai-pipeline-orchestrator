from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from core.database import get_db
from models.pipeline import Pipeline, PipelineRun, PipelineStatus
from core.celery_app import celery_app

router = APIRouter()


# ── Schemas ──────────────────────────────────────────────────────────────────

class PipelineCreate(BaseModel):
    name: str
    description: Optional[str] = None
    config: Optional[dict] = None
    schedule: Optional[str] = None


class PipelineResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    status: PipelineStatus
    config: Optional[dict]
    schedule: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class RunResponse(BaseModel):
    id: str
    pipeline_id: str
    celery_task_id: Optional[str]
    status: PipelineStatus
    rows_processed: int
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    created_at: datetime

    class Config:
        from_attributes = True


# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.get("/", response_model=list[PipelineResponse])
async def list_pipelines(
    skip: int = 0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """Lista todos os pipelines."""
    result = await db.execute(
        select(Pipeline).order_by(desc(Pipeline.created_at)).offset(skip).limit(limit)
    )
    return result.scalars().all()


@router.post("/", response_model=PipelineResponse, status_code=status.HTTP_201_CREATED)
async def create_pipeline(
    payload: PipelineCreate,
    db: AsyncSession = Depends(get_db),
):
    """Cria um novo pipeline."""
    pipeline = Pipeline(**payload.model_dump())
    db.add(pipeline)
    await db.flush()
    await db.refresh(pipeline)
    return pipeline


@router.get("/{pipeline_id}", response_model=PipelineResponse)
async def get_pipeline(pipeline_id: str, db: AsyncSession = Depends(get_db)):
    """Retorna um pipeline pelo ID."""
    result = await db.execute(select(Pipeline).where(Pipeline.id == pipeline_id))
    pipeline = result.scalar_one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline não encontrado")
    return pipeline


@router.post("/{pipeline_id}/run", response_model=RunResponse, status_code=status.HTTP_202_ACCEPTED)
async def trigger_pipeline(pipeline_id: str, db: AsyncSession = Depends(get_db)):
    """Dispara a execução de um pipeline via Celery."""
    result = await db.execute(select(Pipeline).where(Pipeline.id == pipeline_id))
    pipeline = result.scalar_one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline não encontrado")

    # Envia tarefa para o Celery
    task = celery_app.send_task(
        "worker.tasks.run_etl_pipeline",
        args=[pipeline_id],
        kwargs={"config": pipeline.config},
    )

    # Registra o run no banco
    run = PipelineRun(
        pipeline_id=pipeline_id,
        celery_task_id=task.id,
        status=PipelineStatus.PENDING,
    )
    db.add(run)
    await db.flush()
    await db.refresh(run)
    return run


@router.get("/{pipeline_id}/runs", response_model=list[RunResponse])
async def list_runs(pipeline_id: str, db: AsyncSession = Depends(get_db)):
    """Lista todas as execuções de um pipeline."""
    result = await db.execute(
        select(PipelineRun)
        .where(PipelineRun.pipeline_id == pipeline_id)
        .order_by(desc(PipelineRun.created_at))
        .limit(50)
    )
    return result.scalars().all()


@router.delete("/{pipeline_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_pipeline(pipeline_id: str, db: AsyncSession = Depends(get_db)):
    """Remove um pipeline e seus runs."""
    result = await db.execute(select(Pipeline).where(Pipeline.id == pipeline_id))
    pipeline = result.scalar_one_or_none()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline não encontrado")
    await db.delete(pipeline)
