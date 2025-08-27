"""Database operations for Observer."""

from datetime import datetime, timedelta
from pathlib import Path

from sqlalchemy import Column, DateTime, Float, Integer, String, Text, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .models import ActivityRecord, ProjectType

Base = declarative_base()


class Activity(Base):
    """SQLAlchemy model for activities."""

    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=datetime.now)
    window_title = Column(String(255))
    window_class = Column(String(100))
    project_name = Column(String(100))
    project_type = Column(String(50))
    details = Column(Text)
    confidence = Column(Float)
    screenshot_path = Column(String(500))
    context_summary = Column(Text)


class Database:
    """Database interface for Observer."""

    def __init__(self, db_path: Path):
        self.engine = create_engine(f"sqlite:///{db_path}")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def save_activity(self, record: ActivityRecord, screenshot_path: Path) -> int:
        """Save activity record to database."""
        session = self.Session()
        try:
            activity = Activity(
                timestamp=record.timestamp,
                window_title=record.window_title,
                window_class=record.window_class,
                project_name=record.project_name,
                project_type=record.project_type.value,
                details=record.details,
                confidence=None,
                screenshot_path=str(screenshot_path),
                context_summary=record.context_summary,
            )
            session.add(activity)
            session.commit()
            return activity.id
        finally:
            session.close()

    def get_recent_activities(self, minutes: int = 10) -> list[ActivityRecord]:
        """Get recent activities from database."""
        session = self.Session()
        try:
            cutoff = datetime.now() - timedelta(minutes=minutes)
            activities = (
                session.query(Activity)
                .filter(Activity.timestamp > cutoff)
                .order_by(Activity.timestamp.desc())
                .limit(20)
                .all()
            )

            return [
                ActivityRecord(
                    id=a.id,
                    timestamp=a.timestamp,
                    window_title=a.window_title,
                    window_class=a.window_class,
                    project_name=a.project_name,
                    project_type=ProjectType(a.project_type),
                    details=a.details,
                    screenshot_path=a.screenshot_path,
                    context_summary=a.context_summary,
                )
                for a in activities
            ]
        finally:
            session.close()
