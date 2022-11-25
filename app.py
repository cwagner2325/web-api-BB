import time
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
import re
from models import User
from pymongo import MongoClient
from schemas import userEntity, usersEntity
import certifi
import schedule

global cache
cache = {}
global cluster, db, collection

# Adds a user to cache if not already in cache
# Keys is guid, value is user
def addToCache(user):
    if user['guid'] not in cache.keys():
        cache[user['guid']] = user

# iterates through cache and deletes expired users
def deleteExpiredFromCache():
    for user in cache.values():
        if user['expire'] < time.time():
            del cache[user['guid']]
            print(f'deleting {user} from cache')

# returns user from cache and None if not found
def getFromCache(guid):
    if guid in cache.keys():
        return cache[guid]
    return None

# Updates a user in cache if it exists
# Does not add user to cache if it doesn't exist
def updateCache(user):
    if user['guid'] in cache.keys():
        cache[user['guid']] = user

# Deletes data entries with expired expiration in MongoDB
def deleteExpired():
    res = collection.delete_many({"expire": { "$lt" : time.time() }})
    if res.deleted_count > 0:
        deleteExpiredFromCache()


# Takes path (example /guid/9094E4C980C74043A4B586B420E69DDF)
# and returns just the guid (9094E4C980C74043A4B586B420E69DDF)
def getGUIDFromPath(path):
    return path[6:]


# Checks if a string is 32 bits of hex all uppercase, returns true
def isValidGUID(path):
    regex = re.compile('[({]?[A-F0-9]{32}[})]?')
    return regex.match(str(path)) and regex.match(str(path).upper())


# checks if a time is a validint and present time
def isValidExpiration(expire):
    try:
        return int(expire) > int(time.time())
    except:
        return False


# makes a user object using the body of a request
# if variables are invalid or missing, it uses default values
# returns None if no user name was given
def makeUserObject(data, guid=None):
    expire = None
    user = None

    if guid == None and 'guid' in data:
        if isValidGUID(data['guid']):
            guid = data['guid']

    if 'expire' in data:
        if isValidExpiration(data['expire']):
            expire = data['expire']

    if 'user' in data:
        user = data['user']
    else:
        return None

    return User(guid=guid, expire=expire, user=user)


class getPage(RequestHandler):
    def get(self):
        res = (usersEntity(collection.find()))
        for user in res:
            addToCache(user)
        self.write({'Output': res})


class getUser(RequestHandler):
    def get(self):
        guid = getGUIDFromPath(self.request.path)
        if guid:
            #check cache
            item = getFromCache(guid)
            #if not in cache, query database
            if not item:
                res = collection.find_one({"guid": guid })
                if res:
                    item = userEntity(res)
                    addToCache(item)
            if not item: 
                self.write('400 User Not Found')
                return
            self.write(f'Output: {item}')
        else:
            self.write("400 No Guid Provided")

    def delete(self):
        guid = getGUIDFromPath(self.request.path)
        res = collection.delete_one({"guid" : guid})
        if res.deleted_count == 0:
            self.write('400 User Not Found')

    def post(self):
        guid = getGUIDFromPath(self.request.path)
        user = None
        if guid:
            if isValidGUID(guid):
                data = json.loads(self.request.body)
                user = makeUserObject(data, guid)
            else:
                self.write("400 Invalid GUID Provided")
                return
        else:
            data = json.loads(self.request.body)
            user = makeUserObject(data)

        if not user:
            self.write("400 No User Name Provided")
            return

        self.write(f'Output: {user}')

        userDict = user.__dict__
        res = collection.find_one({"guid" : userDict["guid"] })
        
        if res:
            #Replacing exisitng object with new data
            collection.replace_one({"guid" : userDict["guid"]}, userDict )
            updateCache(userDict)
        else:
            #posting new user
            collection.insert_one(userDict)
            addToCache(userDict)


# Throws 404 page not found error for all URLs that don't match
class handleURL(RequestHandler):
    def post(self):
        self.write("404 Page Not Found")

    def get(self):
        self.write("404 Page Not Found")

    def delete(self):
        self.write("404 Page Not Found")

def make_app():
    urls = [
        ("/", getPage),
        (r"/guid/[({]?[a-fA-F0-9]{0,50}[})]?", getUser),
        (r"/guid", getUser),
        (r"/.*", handleURL)
    ]

    return Application(urls, debug=True)


if __name__ == '__main__':
    username = input("Enter mongodb username: ")
    password = input("Enter mongodb password: ")

    try: 
        cluster = MongoClient(
            f'mongodb+srv://{username}:{password}@cluster0.s5krs43.mongodb.net/test', tlsCAFile=certifi.where())
        db = cluster['users']
        collection = db['users']
        deleteExpired()
        print('Success')
    except:
        print("error connecting to mongodb")
        quit()

    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()
  #  schedule.every(10).seconds.do(deleteExpired())
