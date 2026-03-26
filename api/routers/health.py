from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from core.database import get_db
from core.config import settings
import redis.asyncio as aioredis

router = APIRouter()


@router.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    """Verifica saúde de todos os serviços."""
    checks = {}

    # PostgreSQL
    try:
        await db.execute(text("SELECT 1"))
        checks["postgresql"] = "ok"
    except Exception as e:
        checks["postgresql"] = f"error: {str(e)}"

    # Redis
    try:
        r = aioredis.from_url(settings.REDIS_URL)
        await r.ping()
        await r.aclose()
        checks["redis"] = "ok"
    except Exception as e:
        checks["redis"] = f"error: {str(e)}"

    all_ok = all(v == "ok" for v in checks.values())

    return {
        "status": "healthy" if all_ok else "degraded",
        "app": settings.APP_NAME,
        "services": checks,
    }
