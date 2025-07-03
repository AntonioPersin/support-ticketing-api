from pydantic import BaseModel
from typing import Any, Optional

class Ticket(BaseModel):
    id: int
    title: str
    status: str  # "open" ili "closed"
    priority: str  # "low", "medium" ili "high"
    assignee: Optional[str]
    description: Optional[str] = None

class TicketDetail(Ticket):
    original: Any  # puni JSON iz DummyJSON