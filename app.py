from flask import Flask
from flask_restful import Api
from RestAPI import MainKeyword, SubKeyword


app = Flask(__name__)
api = Api(app)


api.add_resource(MainKeyword, '/mainKeyword')
api.add_resource(SubKeyword, '/subKeyword')


if __name__ == '__main__':
    app.run()
