from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Log(Base):
    """
    Represents a single log entry in the system.

    Attributes:
        id (int): Unique identifier for the log entry.
        timestamp (datetime): Time when the log was created (defaults to current UTC time).
        level (str): Severity level of the log (e.g., INFO, WARNING, ERROR).
        message (str): Descriptive message for the log.
        source (str): Source of the log (e.g., api-server, worker-service).
    """
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    level = Column(String, index=True)       # e.g., INFO, ERROR
    message = Column(String)
    source = Column(String, index=True)      # e.g., api-server