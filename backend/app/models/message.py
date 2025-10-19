"""
Message Model
Represents individual messages in a debate
"""

from sqlalchemy import Column, String, Integer, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.models.debate import Base

class Message(Base):
    """Message model for debate chat history"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    debate_id = Column(String, ForeignKey('debates.id'), nullable=False)
    sender = Column(String, nullable=False)  # 'human', 'ai', 'system'
    content = Column(Text, nullable=False)
    round_number = Column(Integer, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    # debate = relationship("Debate", back_populates="messages")
    
    def to_dict(self):
        """Convert message to dictionary"""
        return {
            "id": self.id,
            "debate_id": self.debate_id,
            "sender": self.sender,
            "content": self.content,
            "round_number": self.round_number,
            "timestamp": self.timestamp.isoformat() if self.timestamp else None
        }
