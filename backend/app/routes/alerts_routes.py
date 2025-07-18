from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List
from ..database import SessionLocal
from ..models import Log

router = APIRouter()

def get_db():
    """
    Dependency that provides a database session.
    Closes the session automatically after the request.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class AlertResponse(dict):
    """
    Represents a triggered alert.

    Keys:
        alert (str): Description of the alert.
        error_count (int): Number of ERROR logs in the time window.
        time_window_minutes (int): Time window in minutes used for evaluation.
        trigger_threshold (int): Threshold that triggered the alert.
        timestamp (datetime): Time when the alert was generated.
    """
    
    pass  # Keeping it simple, could use Pydantic later if needed

@router.get("/alerts")
async def get_alerts(
    minutes: int = Query(5, description="Time window to check (minutes)"),
    error_threshold: int = Query(5, description="Trigger alert if ERROR count exceeds this"),
    db: Session = Depends(get_db)
):
    """Check if ERROR logs exceed threshold within a time window."""
    try:
        time_limit = datetime.utcnow() - timedelta(minutes=minutes)
        error_count = (
            db.query(Log)
            .filter(Log.level == "ERROR", Log.timestamp >= time_limit)
            .count()
        )
        alerts = []
        if error_count > error_threshold:
            alerts.append({
                "alert": "High ERROR rate detected",
                "error_count": error_count,
                "time_window_minutes": minutes,
                "trigger_threshold": error_threshold,
                "timestamp": datetime.utcnow()
            })
        return {"alerts": alerts}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Alert check failed: {str(e)}")