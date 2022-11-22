from typing import List
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
from models import User

items = [
    {
        "id": 1,
        "name": "test1"
    },
    {
        "id": 2,
        "name": "test2"
    },
    {
        "id": 3,
        "name": "test3"
    }
]


class getRequest(RequestHandler):
    def get(self, id=None):
        global items
        if id is not None:
            item = [item for item in items if item['id'] is int(id)]
            self.write({'Output': item})
        else:
            self.write({"Output:\n": items})


class postRequest(RequestHandler):
    global items
    print('reached')
    def post(self, id=None):
        if id is not None:
            print('reached2')
            user = [item for item in items if item['id'] is int(id)]
            print( f'editing {user}')
        else:
            print('reached3')
            user = {
                "id": 5,
                "name": "newAddition"
            }
            newItems = items.append(user)
            items = newItems
            self.write({"Output:\n": newItems})


    # def delete(self, id):
    #     global items
    #     new_items = [item for item in items if item['id'] is not int(id)]
    #     items = new_items
    #     self.write({'message': 'Item with id %s was deleted' % id})


def make_app():
    urls = [
        ("/", getRequest),
        (r"/guid/([^/]+)?", getRequest),
        (r"/guid/([^/]+)?", postRequest),
        (r"/guid/", postRequest),
    ]
    return Application(urls, debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()
