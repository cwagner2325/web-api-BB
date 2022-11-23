from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
from models import User

items = []

def get_filtered(id):
    # Filters list and returns item with matching id
    result = [item for item in items if item['id'] == int(id)]
    return result

class getPage(RequestHandler):
    def get(self):
        self.write(f'Output:\n: {items}')

class getUser(RequestHandler):
    def get(self, guid=None):
        print('here:', guid)
        if id:
            item = get_filtered(id)
            if item:
                self.write(f'Output: {item}')
            else:
                self.set_status(404, "GUID Not Found")
        else:
            self.set_status(404, "Page Not Found")

    def post(self):
        global items
        user = User(user="Cayden Wagner")
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
        (r"/guid", getUser),
        (r"/guid/[({]?[a-fA-F0-9]{32}[})]?", getUser),
        (r"/guid", getUser),
    ]

    return Application(urls, debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()
