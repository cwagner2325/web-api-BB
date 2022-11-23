from uuid import UUID, uuid1
from pydantic import BaseModel
from typing import Optional
import json


class User(BaseModel):
    guid: Optional[str] = str(uuid1().hex).upper()
    expiration: Optional[int] = 30
    user: str