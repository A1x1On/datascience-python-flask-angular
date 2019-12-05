from flask            import Flask, Blueprint, jsonify, request, Response, send_from_directory, send_file
from .usersRepository import Repository
from random           import randrange
from os.path          import dirname, join
from werkzeug.utils   import secure_filename

import json
import os

users = Blueprint('api', __name__, template_folder='templates', static_folder='static')

@users.route('/')
def index():
    return jsonify({'users': 'dskfjhdskhdskfh'})

@users.route('/getAvg', methods=['GET'])
def getAvg():
    criteria = request.args.get('val')
    return Response(Repository.get(criteria))

@users.route('/upload', methods=['POST'])
def upload():

    print(request.files)
    test                     = request.files['test']
    print(test)

    rand                     = str(randrange(1000))
    testName                 = rand + test.filename
    criteria                 = Object()
    criteria.titles          = [Object()]
    criteria.titles[0].title = testName

    try:
        test .save(os.path.join(join(dirname(__file__), '..\\..\\static\\uploaded\\'), testName))
        return Response(criteria.toJSON())
    except:
        return Response({'ERROR': 'CAN\'t UPLOAD'})

@users.route('/getSubResults', methods=['POST'])
def getSubResults():
    criteria = json.loads(request.data.decode('utf-8'), object_hook=CSVData)

    print('getSubResults!!!')
    print(criteria)
    if criteria.pattern == 'titanic':
        return Response('TITANIC')
    elif criteria.pattern == 'risk-company':
        return Response(Repository.getRiskCompPrediction(criteria))
    else:
        return Response('CUSTOM')


# AUX --------------------
class CSVData:
  def __init__(self, dict):
      vars(self).update(dict)


class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
