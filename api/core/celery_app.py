from celery import Celery
from celery.schedules import crontab
from core.config import settings

celery_app = Celery(
    "pipeline_orchestrator",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=["worker.tasks"],
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="America/Sao_Paulo",
    enable_utc=True,
    task_track_started=True,
    task_acks_late=True,
    worker_prefetch_multiplier=1,

    # Agendamentos automáticos (Celery Beat)
    beat_schedule={
        "run-etl-pipeline-every-hour": {
            "task": "worker.tasks.run_etl_pipeline",
            "schedule": crontab(minute=0),  # todo início de hora
            "args": ("scheduled_etl",),
        },
        "cleanup-old-tasks-daily": {
            "task": "worker.tasks.cleanup_old_tasks",
            "schedule": crontab(hour=2, minute=0),  # 02:00 todo dia
        },
    },
)
