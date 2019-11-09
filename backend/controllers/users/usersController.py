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
    train                    = request.files['train']
    test                     = request.files['test']
    print(train)
    print(test)


    rand                     = str(randrange(1000))
    trainName                = rand + train.filename
    testName                 = rand + test.filename
    criteria                 = Object()
    criteria.titles          = [Object(), Object()]
    criteria.titles[0].title = trainName
    criteria.titles[1].title = testName

    try:
        train.save(os.path.join(join(dirname(__file__), '..\\..\\static\\uploaded\\'), trainName))
        test .save(os.path.join(join(dirname(__file__), '..\\..\\static\\uploaded\\'), testName))
        return Response(criteria.toJSON())
    except:
        return Response({'ERROR': 'CAN\'t UPLOAD'})

@users.route('/getSubResults', methods=['POST'])
def getSubResults():
    criteria = json.loads(request.data.decode('utf-8'), object_hook=CSVData)
    if criteria.pattern == 'titanic':
        return Response(Repository.getTitanicPrediction(criteria))
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
