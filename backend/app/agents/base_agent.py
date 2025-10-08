"""
Base Agent
to implement the foundation for all the debate agents with MCP support
MCP = model context protocol
"""

from abc import ABC, abstractmethod     #abc - abstract base classes
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datatime import datetime
import logging

logger = logging.getLogger(__name__)

@dataclass
class AgentMessage:
    """msg format for inter-agent communication - MCP"""
    sender: str
    receiver: str
    message_type = str
    content: Dict [str, Any]
    timestamp: datetime
    correlation_id: str

class BaseAgent(ABC):
    """
    base class of all agents 
    to implent MCP for agent communication
    """

    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.capabilities = []
        self.message_history = []
        self.state = "idle"

    @abstractmethod
    async def process(self, input_date: Dict[str,Any]) -> Dict[str, Any]:
        """
        Main processing method has to implemented by each agent
        """
        pass

    async def receive_message(self, message:AgentMessage) -> Optional[AgentMessage]:
        """
        handle incoming messages from the other agents
        """
        self.message_history.append(message)
        logger.info(f"{self.name} received message from {message.sender}")

        #process based on the message type
        if message.message_type == "process_request":
            result = await self.process(message.content)
            return self._create_response(message, result)
        
        return None
    
    def create_message(self, original_message:AgentMessage, content: Dict[str, Any]) -> AgentMessage:
        """create response message"""
        
        return AgentMessage(
            sender= self.agent_id,
            receiver= original_message.sender,
            message_type="process_response",
            content=content,
            timestamp=datetime.now(),
            correlation_id=original_message.correlation_id
        )
    
    def get_status(self) -> Dict[str, Any]:
        """Return current agent status"""
        return {
            "agent_id": self.agent_id,
            "name": self.name,
            "state": self.state,
            "capabilities": self.capabilities,
            "messages_processed": len(self.message_history)
        }
        