from flask import jsonify, Response, request, send_from_directory, send_file
from flask_restful import Resource, Api, fields, marshal_with

from controllers.users.usersController import users
from controllers.statistic.statisticController import stat


class HelloWorld(Resource):
    def get(self):
        return send_from_directory('../frontend/dist/file-manager', "index.html")


def create_api(app):
    api = Api(app)
    api.add_resource(HelloWorld, '/')

    app.register_blueprint(users, url_prefix='/api')
    app.register_blueprint(stat, url_prefix='/st')



