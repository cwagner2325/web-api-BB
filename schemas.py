def userEntity(item) -> dict: 
  return {
    "guid":str(item["guid"]),
    "expire":int(item["expire"]),
    "user":str(item["user"]),
  }

def usersEntity(entity) -> list:
  return [userEntity(item) for item in entity] 