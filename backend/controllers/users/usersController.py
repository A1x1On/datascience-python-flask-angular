from flask            import Flask, Blueprint, jsonify, request, Response, send_from_directory, send_file
from .usersRepository import Repository
import json

from random import randrange

import os
from os.path import dirname, join
from werkzeug.utils import secure_filename

users = Blueprint('api', __name__, template_folder='templates', static_folder='static')

@users.route('/')
def index():
    return jsonify({'users': 'dskfjhdskhdskfh'})


@users.route('/getAvg', methods=['GET'])
def getAvg():
    criteria = request.args.get('val')
    print(request.args.get('val'))
    return Response(Repository.get(criteria))

@users.route('/getSubResults', methods=['POST'])
def getSubResults():
    #data = json.loads(request.data.decode('utf-8'))
    #print(data['titles'][0]['title'])

    print('---------------------------')
    print(request.data)
    criteria = json.loads(request.data.decode('utf-8'), object_hook=CSVData)
    print(criteria)


    return Response(Repository.getTrained(criteria))

class CSVData:
  def __init__(self, dict):
      vars(self).update(dict)


@users.route('/upload', methods=['POST'])
def upload():
    print(request.files['train'])

    train = request.files['train']
    test = request.files['test']

    #for val in request.files.getlist('file'):
    #    print(val)

    #file = request.files[0]['train']
    #file2 = request.files()

    #blob = file.read()
    #size = len(blob)
    #print(size)


    #print(type(request.files))


    #print('hell!!o im here------------->', file)

    rand = str(randrange(1000))
    trainName = rand + train.filename
    testName = rand + test.filename



    me = Object()
    me.titles = [Object(), Object()]
    me.titles[0].title = trainName
    me.titles[1].title = testName
    #me.age = 35
    #me.dog = Object()
    #me.dog.name = "Apollo"

    print(me.toJSON())


    try:
        train.save(os.path.join(join(dirname(__file__), '..\\..\\temp\\csvs\\'), trainName))
        test.save(os.path.join(join(dirname(__file__), '..\\..\\temp\\csvs\\'), testName))
        return Response(me.toJSON())
    except:
        return Response({'tt': 'ERROR'})


    #return Response(Repository.prepareFile(file))

class Object:
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
