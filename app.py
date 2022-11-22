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
    def get(self, id):
        global items
        item = [item for item in items if item['id'] is int(id)]
        self.write({'item': item})


class requestHandlers(RequestHandler):
    def post(self, _):
        items.append(json.loads(self.request.body))
        self.write({'message': 'new item added'})

    def delete(self, id):
        global items
        new_items = [item for item in items if item['id'] is not int(id)]
        items = new_items
        self.write({'message': 'Item with id %s was deleted' % id})


def make_app():
    urls = [
        (r"/GET/guid/([^/]+)?", getRequest),
        (r"/api/item/([^/]+)?", requestHandlers)
    ]
    return Application(urls, debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()
