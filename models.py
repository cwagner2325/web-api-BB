from uuid import UUID, uuid1
from pydantic import BaseModel
from typing import Optional
import json


class User(BaseModel):
    guid: Optional[UUID] = uuid1().hex
    expiration: Optional[int] = 30
    user: str