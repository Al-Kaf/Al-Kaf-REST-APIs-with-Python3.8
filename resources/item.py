import sqlite3
from flask_restful import reqparse, Resource
from flask_jwt import jwt_required

from models.items import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This is to be a number")
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="need a store_id")

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            return item.json()
        return {"massage": " item Not found"}, 404

    def post(self, name):

        if ItemModel.find_item_by_name(name):
            return {"message": "An item with name '{}' already exists.".format(name)}, 400  # 400 for bad requst

        # request_data = request.get_json(silent=True)  # this code for read the Json Content send with post requst if the file dose not has a Content-Type in header or the file is  not a josn file, it will return error masg.to avoid  # it use (force=True) to read body with out looking to Content-Type in header also, we can use (silent=True) to return null if hear is error.
        request_data = Item.parser.parse_args()
        item = ItemModel(name,request_data["price"], request_data['store_id'])
        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred when insert_item."}, 500  # 500 > internal Server error

        return item.json(), 201  # 201 is the number for creat

    def delete(self, name):
        item = ItemModel.find_item_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "item deleted"}
        return {"message": "item NOT found"}

    def put(self, name):
        request_data = Item.parser.parse_args()
        # request_data = request.get_json(silent=True)

        item = ItemModel.find_item_by_name(name)
        if item is None:
            try:
                item = ItemModel(name, **request_data) #**request_data it is the same of (request_data["price"], request_data["price"])
            except:
                return {"message": "An error occurred When insert_item."}, 500
        else:
            try:
                item.price = request_data["price"]
            except:
                return {"message": "An error occurred When update_item."}, 500

        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {"items": [item.json() for item in ItemModel.query.all()]}
