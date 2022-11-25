from uuid import uuid1
import time

THIRTY_DAYS_IN_SEC = 60

class User:
    def  __init__(self, user, guid=None, expire=None):
        self.guid = guid if guid is not None else str(uuid1().hex).upper()
        self.expire = expire if expire is not None else int(time.time() + THIRTY_DAYS_IN_SEC)
        self.user = user

    def __str__(self):
        return f'guid: {self.guid}, expire: {self.expire}, user: {self.user}'