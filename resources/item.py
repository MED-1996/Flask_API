from flask_restful import Resource, reqparse 
from flask_jwt import jwt_required
from models.item import ItemModel

class ItemList(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]}


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type = float,
        required = True,
        help = "This field cannot be left blank"
    )
    parser.add_argument('store_id',
        type = float,
        required = True,
        help = "Every item needs a store id"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'The item doesn\'t exist!'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': f'An item with name {name} already exists!'}, 400
 
        data = Item.parser.parse_args()
        new_item = ItemModel(name, data['price'], data['store_id'])

        try:
            new_item.save_to_db()
        except:
            return {'message': 'There was an error inserting the item into the database.'}, 500

        return new_item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)
        
        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
            item.price = data['price']
        
        item.save_to_db()
        
        return item.json()

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        
        return {'message': 'Item Deleted'}