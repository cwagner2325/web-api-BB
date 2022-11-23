from typing import List
from tornado.web import Application, RequestHandler
from tornado.ioloop import IOLoop
import json
from models import User

items = []


class getRequest(RequestHandler):
    def get(self, id=None):
        global items
        if id is not None:
            res = None
            for item in items:
                jsonItem = json.loads(item)
                print(jsonItem['guid'])
                print(id)
                if str(jsonItem['guid']) is str(id):
                    res = jsonItem
                    print(res)

            self.write({'Output': res})
        else:
            self.write({"Output:\n": items})


class postRequest(RequestHandler):
    print('reached')
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
        ("/", getRequest),
        (r"/guid/[({]?[a-fA-F0-9]{8}[-]?([a-fA-F0-9]{4}[-]?){3}[a-fA-F0-9]{12}[})]?", getRequest),
        (r"/guid/[({]?[a-fA-F0-9]{32}[})]?", postRequest),
        (r"/guid", postRequest),
    ]
    return Application(urls, debug=True)


if __name__ == '__main__':
    app = make_app()
    app.listen(3000)
    IOLoop.instance().start()
