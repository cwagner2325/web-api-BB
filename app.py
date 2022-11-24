import time
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
import re
from models import User
from pymongo import MongoClient
from schemas import userEntity, usersEntity
import certifi

global items
items = []
global cluster, db, collection

# Filters list of users for a specific id and returns the user with matching id


def get_filtered(id):
    global items
    for user in items:
        jsonUser = json.loads(user)
        if jsonUser['guid'] == id:
            return jsonUser
    return None


# Takes path (example /guid/9094E4C980C74043A4B586B420E69DDF)
# and returns just the guid (9094E4C980C74043A4B586B420E69DDF)
def getGUIDFromPath(path):
    return path[6:]


# Checks if a string is 32 bits of hex all uppercase, returns true
def isValidGUID(path):
    regex = re.compile('[({]?[A-F0-9]{32}[})]?')
    return regex.match(str(path)) and regex.match(str(path).upper())


# checks if a time is a validint and present time
def isValidExpiration(expiration):
    try:
        return int(expiration) > int(time.time())
    except:
        return False


# makes a user object using the body of a request
# if variables are invalid or missing, it uses default values
# returns None if no user name was given
def makeUserObject(data, guid=None):
    expiration = None
    user = None

    if guid == None and 'guid' in data:
        if isValidGUID(data['guid']):
            guid = data['guid']

    if 'expiration' in data:
        if isValidExpiration(data['expiration']):
            expiration = data['expiration']
    if 'user' in data:
        name = data['user']
    else:
        return user

    if guid:
        if expiration:
            user = User(guid=guid, expiration=expiration, user=name)
        else:
            user = User(guid=guid, user=name)
    elif expiration:
        user = User(expiration=expiration, user=name)
    else:
        user = User(user=name)

    return user


class getPage(RequestHandler):
    def get(self):
        res = (usersEntity(collection.find()))
        self.write({'Output': res})


class getUser(RequestHandler):
    def get(self):
        guid = getGUIDFromPath(self.request.path)
        if guid:
            #check cache
            item = get_filtered(guid)
            #if not in cache, query database
            if not item:
                res = collection.find_one({"guid": guid })
                if res:
                    item = userEntity(res)
            if not item: 
                self.write('400 User Not Found')
                return
            self.write(f'Output: {item}')
        else:
            self.write("400 No Guid Provided")

    def delete(self):
        guid = getGUIDFromPath(self.request.path)
        collection.delete_one({"guid" : guid})

    def post(self):
        guid = getGUIDFromPath(self.request.path)
        user = None
        if guid:
            if isValidGUID(guid):
                item = get_filtered(guid)
                if item:
                    self.write(f'editing {item}')
                    return
                else:
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

        items.append(json.dumps(user.__dict__))
        self.write(f'Output: {user}')
        collection.insert_one(dict(user))


# Throws 404 page not found error for all URLs that don't match
class handleURL(RequestHandler):
    def post(self):
        self.write("404 Page Not Found")

    def get(self):
        self.write("404 Page Not Found")

    def delete(self):
        self.write("404 Page Not Found")

    # def delete(self, id):
    #     global items
    #     new_items = [item for item in items if item['id'] is not int(id)]
    #     items = new_items
    #     self.write({'message': 'Item with id %s was deleted' % id})


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

    cluster = MongoClient(
        f'mongodb+srv://{username}:{password}@cluster0.s5krs43.mongodb.net/test', tlsCAFile=certifi.where())
    db = cluster['users']
    collection = db['users']

    print('Success')

    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()
