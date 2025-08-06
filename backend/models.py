from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from database import Base

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    client_problem = Column(String, index=True)
    diagnostic_question = Column(String)
    root_cause_analysis = Column(String)
    foresight_prediction = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
