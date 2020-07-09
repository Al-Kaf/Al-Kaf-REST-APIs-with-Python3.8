from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import  UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from db import db

app = Flask(__name__)  #creat a Flask Object
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = 'jose'
api = Api(app)         # Passing the Flask Opject to Api Of flask_restful, so we use falsk-restful the has Flask inside it.


jwt = JWT(app, authenticate, identity)  # it is creat route with (/auth) addrees.// it reseve username and password and return token


api.add_resource(Item, "/item/<string:name>")  #define the route for item that call the item class
api.add_resource(ItemList, "/items")         #define the route for items that call the itemlist class
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if __name__ == '__main__': # to Prevents the app.run from running when we import the file.
    db.init_app(app)
    app.run(port=5000,debug=True)    #run the server on port 5000, and i can use (debug=True) to see if there any problem a clear in text format


