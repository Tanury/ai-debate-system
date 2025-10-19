
from sqlalchemy import Column, String, Integer, DateTime, JSON, Text, Boolean
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Debate(Base):
    __tablename__ = "debates"
    
    id = Column(String, primary_key=True)
    topic = Column(Text, nullable=False)
    status = Column(String, default="active")  # active, completed, abandoned
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_rounds = Column(Integer, default=0)
    final_winner = Column(String, nullable=True)  # human, ai, draw
    metadata = Column(JSON, default={})

class DebateRound(Base):
    __tablename__ = "debate_rounds"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    debate_id = Column(String, nullable=False)
    round_number = Column(Integer, nullable=False)
    human_argument = Column(Text, nullable=False)
    ai_argument = Column(Text, nullable=False)
    human_score = Column(Integer, default=0)
    ai_score = Column(Integer, default=0)
    round_winner = Column(String, nullable=True)
    keywords = Column(JSON, default=[])
    created_at = Column(DateTime, default=datetime.utcnow)
    evaluation_data = Column(JSON, default={})

