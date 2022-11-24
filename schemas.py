def userEntity(item) -> dict: 
  return {
    "guid":str(item["guid"]),
    "expiration":int(item["expiration"]),
    "user":str(item["user"]),
  }

def usersEntity(entity) -> list:
  return [userEntity(item) for item in entity]