from celery import shared_task
from loguru import logger
import time
import random


@shared_task(
    bind=True,
    name="worker.tasks.run_etl_pipeline",
    max_retries=3,
    default_retry_delay=60,
    acks_late=True,
)
def run_etl_pipeline(self, pipeline_id: str, config: dict = None):
    """
    Executa um pipeline ETL completo:
    Extract → Transform → Load
    """
    logger.info(f"▶️  Starting pipeline: {pipeline_id}")
    config = config or {}

    try:
        # ── EXTRACT ──────────────────────────────────────────
        self.update_state(state="PROGRESS", meta={"step": "extract", "progress": 10})
        logger.info("📥 Extracting data...")
        rows = _extract_data(config)
        logger.info(f"✅ Extracted {len(rows)} rows")

        # ── TRANSFORM ─────────────────────────────────────────
        self.update_state(state="PROGRESS", meta={"step": "transform", "progress": 50})
        logger.info("⚙️  Transforming data...")
        transformed = _transform_data(rows)
        logger.info(f"✅ Transformed {len(transformed)} rows")

        # ── LOAD ──────────────────────────────────────────────
        self.update_state(state="PROGRESS", meta={"step": "load", "progress": 80})
        logger.info("📤 Loading data...")
        _load_data(transformed, config)

        result = {
            "pipeline_id": pipeline_id,
            "rows_extracted": len(rows),
            "rows_transformed": len(transformed),
            "status": "success",
        }
        logger.info(f"🎉 Pipeline {pipeline_id} completed: {result}")
        return result

    except Exception as exc:
        logger.error(f"❌ Pipeline {pipeline_id} failed: {exc}")
        raise self.retry(exc=exc)


@shared_task(name="worker.tasks.cleanup_old_tasks")
def cleanup_old_tasks():
    """Remove registros antigos de execuções (roda diariamente às 02:00)."""
    logger.info("🧹 Running cleanup task...")
    # Aqui você conectaria ao banco e deletaria runs com mais de 30 dias
    time.sleep(1)
    logger.info("✅ Cleanup completed")
    return {"status": "cleaned"}


# ── Helpers privados (simula lógica ETL) ──────────────────────────────────────

def _extract_data(config: dict) -> list[dict]:
    """Extrai dados de uma fonte (API, CSV, banco externo, etc.)."""
    time.sleep(random.uniform(0.5, 1.5))
    return [{"id": i, "value": random.random() * 100} for i in range(100)]


def _transform_data(rows: list[dict]) -> list[dict]:
    """Aplica transformações e limpeza nos dados."""
    time.sleep(random.uniform(0.5, 1.0))
    return [
        {**row, "value_normalized": round(row["value"] / 100, 4)}
        for row in rows
        if row["value"] > 0
    ]


def _load_data(rows: list[dict], config: dict) -> None:
    """Carrega os dados transformados no destino."""
    time.sleep(random.uniform(0.3, 0.8))
    logger.info(f"📦 Loaded {len(rows)} rows to destination")
