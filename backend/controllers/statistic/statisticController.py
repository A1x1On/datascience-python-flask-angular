from flask import Flask, Blueprint, jsonify, request, Response, send_from_directory, send_file

import numpy as np
import matplotlib as pl
pl.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV


stat = Blueprint('st', __name__, template_folder='templates', static_folder='static')

@stat.route('/')
def index():
    return jsonify({'users': 'ssssssssssssssUSERSSSS'})


@stat.route('/getAvg', methods=['GET'])
def getAvg():
   val = '12,3,4,56,7,20'#request.args.get('val')
   print(val)
   l1=val.split(',')
   ar=np.array(l1,dtype=int)
   return Response(str(np.average(ar)))
