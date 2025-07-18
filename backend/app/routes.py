from fastapi import APIRouter, Depends
from typing import List, Optional
from fastapi import Query
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .database import SessionLocal
from .models import Log
from datetime import datetime, timedelta

router = APIRouter()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for incoming log data
class LogCreate(BaseModel):
    level: str
    message: str
    source: str

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/logs")
async def create_log(log: LogCreate, db: Session = Depends(get_db)):
    new_log = Log(level=log.level, message=log.message, source=log.source)
    db.add(new_log)
    db.commit()
    db.refresh(new_log)
    return {"id": new_log.id, "message": "Log stored successfully"}




@router.get("/logs")
async def get_logs(
    level: Optional[str] = Query(None, description="Filter by log level (INFO, ERROR, etc.)"),
    source: Optional[str] = Query(None, description="Filter by source (e.g., api-server)"),
    limit: int = Query(50, description="Max number of logs to return"),
    db: Session = Depends(get_db)
):
    query = db.query(Log)
    
    if level:
        query = query.filter(Log.level == level)
    if source:
        query = query.filter(Log.source == source)

    logs = query.order_by(Log.timestamp.desc()).limit(limit).all()

    return [
        {
            "id": log.id,
            "timestamp": log.timestamp,
            "level": log.level,
            "message": log.message,
            "source": log.source
        }
        for log in logs
    ]







@router.get("/alerts")
async def get_alerts(
    minutes: int = Query(5, description="Time window to check (minutes)"),
    error_threshold: int = Query(5, description="Trigger alert if ERROR count exceeds this"),
    db: Session = Depends(get_db)
):
    time_limit = datetime.utcnow() - timedelta(minutes=minutes)
    error_count = (
        db.query(Log)
        .filter(Log.level == "ERROR", Log.timestamp >= time_limit)
        .count()
    )

    alerts = []
    if error_count > error_threshold:
        alerts.append(
            {
                "alert": "High ERROR rate detected",
                "error_count": error_count,
                "time_window_minutes": minutes,
                "trigger_threshold": error_threshold,
                "timestamp": datetime.utcnow()
            }
        )

    return {"alerts": alerts}