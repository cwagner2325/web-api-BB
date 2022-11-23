from os import path
from requests import request
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
import re
from models import User

global items
items = []

#Filters list of users for a specific id and returns the user with matching id
def get_filtered(id):
    for user in items:
        jsonUser = (json.loads(user))
        if jsonUser['guid'] == id:
            return jsonUser
    return None


#Takes path (example /guid/9094E4C980C74043A4B586B420E69DDF)
#and returns just the guid (9094E4C980C74043A4B586B420E69DDF)
def getGUIDFromPath(path):
    print(path[6:])
    return path[6:]


#Checks if a guid is 32 bits of hex all uppercase, returns true
def isValidGUID(path):
    regex = re.compile('[({]?[A-F0-9]{32}[})]?')
    return regex.match(path)


class getPage(RequestHandler):
    def get(self):
        self.write(f'Output:\n: {items}')


class getUser(RequestHandler):
    def get(self):
        guid = getGUIDFromPath(self.request.path)
        if guid:
            item = get_filtered(guid)
            if item:
                self.write(f'Output: {item}')
            else:
                self.write('User Not Found')
                self.set_status(400, "User Does Not Exists")
        else:
            self.set_status(400, "User Does Not Exists")

    def post(self):
        user = User(user="Cayden")
        jsonUser = (json.dumps(user.__dict__))
        items.append(jsonUser)
        self.write(f'Output: {jsonUser}')

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
    ]

    return Application(urls, debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()