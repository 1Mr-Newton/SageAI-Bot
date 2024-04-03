from pydantic import BaseModel, UUID4
from datetime import datetime


class User(BaseModel):
    id: UUID4
    created_at: datetime
    user_id: str
    oai_id: UUID4
    display_name: str
