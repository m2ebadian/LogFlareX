from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from ..database import SessionLocal
from ..models import Log
from ..metrics import error_log_counter


router = APIRouter()


def get_db():
    """
    Dependency that provides a database session.
    Closes the session automatically after the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class LogCreate(BaseModel):
    """
    Request model for creating a new log entry.

    Attributes:
        level (str): Severity level of the log (e.g., INFO, WARNING, ERROR).
        message (str): Descriptive message for the log.
        source (str): Source of the log (e.g., api-server, worker-service).
    """

    level: str
    message: str
    source: str

class LogResponse(BaseModel):
    """
    Response model for a stored log entry.

    Attributes:
        id (int): Unique identifier for the log entry.
        timestamp (datetime): Time when the log was created.
        level (str): Severity level of the log.
        message (str): Descriptive message for the log.
        source (str): Source of the log.
    """

    id: int
    timestamp: datetime
    level: str
    message: str
    source: str

    class Config:
        orm_mode = True

@router.post("/logs", response_model=LogResponse)
async def create_log(log: LogCreate, db: Session = Depends(get_db)):
    """
    Store a new log in the database.

    Args:
        log (LogCreate): Log details including level, message, and source.
        db (Session): Active database session.

    Returns:
        LogResponse: The stored log entry with its ID and timestamp.

    Raises:
        HTTPException (500): If a database error occurs.
    """

    try:
        new_log = Log(level=log.level, message=log.message, source=log.source)
        db.add(new_log)
        db.commit()
        db.refresh(new_log)

        if log.level.upper() == "ERROR":
            error_log_counter.inc()
        return new_log
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@router.get("/logs", response_model=List[LogResponse])
async def get_logs(
    level: Optional[str] = Query(None, description="Filter by log level"),
    source: Optional[str] = Query(None, description="Filter by source"),
    limit: int = Query(50, description="Max logs to return"),
    db: Session = Depends(get_db)
):
    """
    Retrieve logs from the database, optionally filtered by level or source.

    Args:
        level (Optional[str]): Filter by log level (e.g., ERROR).
        source (Optional[str]): Filter by source (e.g., api-server).
        limit (int): Maximum number of logs to return (default: 50).
        db (Session): Active database session.

    Returns:
        List[LogResponse]: A list of logs sorted by timestamp (most recent first).

    Raises:
        HTTPException (500): If a database error occurs.
    """
    try:
        query = db.query(Log)
        if level:
            query = query.filter(Log.level == level)
        if source:
            query = query.filter(Log.source == source)
        return query.order_by(Log.timestamp.desc()).limit(limit).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")