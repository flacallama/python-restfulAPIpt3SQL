from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'Dylan'
api = Api(app)

jwt = JWT(app, authenticate, identity)

# # the api works with resources, and each resource must be a class
# # ex class Student inherits from Resource
# class Student(Resource):
#     #this is the old way - @app.route('/student...')
#     def get(self, name):
#         return {'student': name}
#
# api.add_resource(Student, '/student/<string:name>')

items = []

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True, #all requests must have prices
        help="this field cannot be left black"
    )



    @jwt_required()
    def get(self, name):
        # lets update this...
        # for item in items:
        #     if item['name'] == name:
        #         return item

        # USING FILTER()
        # item = filter(lambda x: x['name'] == name, items)
        # filter takes 2 arguments - the lambda function, and the list of whats being filtered
        # the filter function might return more than one item, or no items, in a 'filter object'
        # item = list(filter(lambda x: x['name'] == name, items))
        # this would give us the complete list of all items in the list
        item = next(filter(lambda x: x['name'] == name, items), None) #give us only first item
        # next throws an error if there are no objects, so we put in None.
        return {"item": item}, 200 if item else 404 #update this to turnary

    def post(self, name):
        # LETS UPDATE THIS POST TO HANDLE A PREVIOUSLY INSERTED ITEM
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return {'message': "an item with name {} already exists.".format(name)}, 400 #badrequest
        # lets change the data to user the parser...
        data = Item.parser.parse_args() # old data request below
        # data = request.get_json() #this will give an error without params if header is wrong
        # data = request.get_json(force=True)  #here we don't look at header
        # data = request.get_json(silent=True) #doesnt give error
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201 # 201 is for "created"   202 is accepted/delaying created

    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': 'Item deleted'}

    def put(self, name):
        # # this route needs to be parsed bc we can update a Name and Price simulatenously
        # # lets use reqparse to control what gets updated
        # # ... actually, let's cut it from here and let the whole class use parser
        # # we do that by adding "item." in front of parser.parse_args()
        # parser = reqparse.RequestParser()
        # parser.add_argument('price',
        #     type=float,
        #     required=True, #all requests must have prices
        #     help="this field cannot be left black"
        # )
        # # data = request.get_json()  #lets change this to user parser
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)   # dictionaries have an update method
        return item

class ItemList(Resource):
    def get(self):
        return {"items": items}

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)  #creates a html page for troubleshooting
