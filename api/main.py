from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from loguru import logger

from core.database import engine, Base
from core.config import settings
from routers import pipelines, tasks, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup e shutdown da aplicação."""
    logger.info(f"🚀 Starting {settings.APP_NAME}")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("✅ Database tables created")
    yield
    logger.info("🛑 Shutting down...")
    await engine.dispose()


app = FastAPI(
    title=settings.APP_NAME,
    description="Plataforma de orquestração de pipelines de dados com IA",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health.router, tags=["Health"])
app.include_router(pipelines.router, prefix="/api/v1/pipelines", tags=["Pipelines"])
app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["Tasks"])


@app.get("/", tags=["Root"])
async def root():
    return {
        "app": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
    }
