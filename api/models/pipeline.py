from sqlalchemy import Column, String, Text, DateTime, Enum, JSON, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base
import enum
import uuid


class PipelineStatus(str, enum.Enum):
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    PAUSED = "paused"


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    status = Column(Enum(PipelineStatus), default=PipelineStatus.PENDING, nullable=False)
    config = Column(JSON, nullable=True)           # configuração flexível em JSON
    schedule = Column(String(100), nullable=True)  # cron expression
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    runs = relationship("PipelineRun", back_populates="pipeline", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pipeline {self.name} [{self.status}]>"


class PipelineRun(Base):
    __tablename__ = "pipeline_runs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    pipeline_id = Column(String, ForeignKey("pipelines.id"), nullable=False, index=True)
    celery_task_id = Column(String, nullable=True)
    status = Column(Enum(PipelineStatus), default=PipelineStatus.PENDING, nullable=False)
    logs = Column(Text, nullable=True)
    result = Column(JSON, nullable=True)
    rows_processed = Column(Integer, default=0)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    pipeline = relationship("Pipeline", back_populates="runs")

    def __repr__(self):
        return f"<PipelineRun {self.id} [{self.status}]>"
