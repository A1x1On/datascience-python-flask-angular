from flask            import Flask, jsonify, Response, request, send_from_directory, send_file
from flask_restful    import Resource, Api, fields, marshal_with
from werkzeug.routing import BaseConverter

from controllers      import create_api
import os

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
