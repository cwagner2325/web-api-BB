from uuid import uuid1
from pydantic import BaseModel
from typing import Optional
import time

THIRTY_DAYS_IN_SEC = 2592000

class User(BaseModel):
    guid: Optional[str] = str(uuid1().hex).upper()
    expiration: Optional[int] = int(time.time() + THIRTY_DAYS_IN_SEC)
    user: str