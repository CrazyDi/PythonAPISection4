from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity


app = Flask(__name__)
app.secret_key = 'kate'
api = Api(app)

jwt = JWT(app, authenticate, identity)

items = []


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help="This field cannot be left blank!")

    @jwt_required()
    def get(self, name):
        item = [x for x in items if x['name'] == name]
        if len(item) > 0:
            return item[0], 200
        else:
            return {'item': None}, 404

    def post(self, name):
        if len([x for x in items if x['name'] == name]) > 0:
            return {'message': "An item with name '{}' already exists".format(name)}, 400

        data = Item.parser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = [x for x in items if x['name'] == name]
        if len(item) == 0:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item[0].update(data)
        return item[0]

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': items}


api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')


if __name__ == "__main__":
    app.run()
