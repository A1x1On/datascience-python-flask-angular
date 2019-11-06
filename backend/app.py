from flask import Flask, jsonify, Response, request, send_from_directory, send_file
from flask_restful import Resource, Api, fields, marshal_with

from pymongo import MongoClient
from bson.json_util import dumps
from bson.objectid import ObjectId
from werkzeug.routing import BaseConverter

import os

from controllers import create_api

# mongodb config
DB_HOST_MONGO = 'mongodb://127.0.0.1:27017/'
DB_NAME_MONGO = "test"
DB_COLLECTION_MONGO = "accounts"
DB_USERNAME = 'root'
DB_PASSWORD = '12345678'

# mongodb connection
mongo_client = MongoClient(DB_HOST_MONGO)
mongo_client[DB_NAME_MONGO].authenticate(DB_USERNAME, DB_PASSWORD, mechanism='SCRAM-SHA-1')
db = mongo_client[DB_NAME_MONGO]
collection = db[DB_COLLECTION_MONGO]

# start flask app
app = Flask(__name__, static_url_path="", static_folder="../frontend/dist/file-manager/")


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]

app.url_map.converters['regex'] = RegexConverter

create_api(app)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8081)
