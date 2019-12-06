from   os.path                 import dirname, join
from   werkzeug.utils          import secure_filename
from   sklearn.pipeline        import Pipeline
from   sklearn.preprocessing   import LabelEncoder
from   sklearn.ensemble        import RandomForestClassifier
from   sklearn.ensemble        import GradientBoostingClassifier
from   sklearn.ensemble        import ExtraTreesClassifier
from   sklearn.ensemble        import BaggingClassifier
from   sklearn.ensemble        import AdaBoostClassifier
from   sklearn.ensemble        import VotingClassifier
from   sklearn.model_selection import GridSearchCV

from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score

import numpy                   as np
import matplotlib              as pl
import matplotlib.pyplot       as plt
import pandas                  as pd
import seaborn                 as sns
import os

pl.use('Agg')

def string2Number(cols, revert):
    risk = cols[0]

    if revert == 1:
        if risk == 1:
            return 'very high risk'
        elif risk == 2:
            return 'high risk'
        elif risk == 3:
            return 'the average risk'
        elif risk == 4:
            return 'low risk'
        elif risk == 5:
            return 'very low risk'
    else:
        if risk == 'very high risk':
            return 1
        elif risk == 'high risk':
            return 2
        elif risk == 'the average risk':
            return 3
        elif risk == 'low risk':
            return 4
        elif risk == 'very low risk':
            return 5

class Repository():
    def get(criteria):
        l1=criteria.split(',')
        ar=np.array(l1,dtype=int)
        return str(np.average(ar))

    def prepareFile(file):
        df = pd.DataFrame.from_dict(file)
        print(df.head())
        return 'succs'

    def getRiskCompPrediction(criteria):
        file_path_train = os.path.join(join(dirname(__file__), '..\\..\\static\\uploaded\\'), 'COMPANIES_TRAIN.csv')
        train           = pd.read_csv(file_path_train, delimiter=";")

        file_path_test  = os.path.join(join(dirname(__file__), '..\\..\\static\\uploaded\\'), criteria.titles[0].title)
        test            = pd.read_csv(file_path_test, delimiter=";")

        print(train.head())
        print(test.head())

        train['Target'] = train[['Target']].apply(string2Number, revert=0, axis = 1) # replace string risk to number

        bin             = pd.get_dummies(train['binaryrisk'], drop_first = True)
        train           = pd.concat([train,bin], axis = 1)
        train.drop('binaryrisk',axis = 1, inplace = True)

        train['R5']    = train[['R5']].apply(impute_r5, axis = 1)
        train['R3']    = train[['R3']].apply(replaceComma, axis = 1)
        train['R4']    = train[['R4']].apply(replaceComma, axis = 1)
        train['R5']    = train[['R5']].apply(replaceComma, axis = 1)
        train['L1']    = train[['L1']].apply(replaceComma, axis = 1)
        train['L2']    = train[['L2']].apply(replaceComma, axis = 1)
        train['P1']    = train[['P1']].apply(replaceComma, axis = 1)
        train['A2']    = train[['A2']].apply(replaceComma, axis = 1)
        train['A4']    = train[['A4']].apply(replaceComma, axis = 1)
        train['1/A5']  = train[['1/A5']].apply(replaceComma, axis = 1)
        train['A6']    = train[['A6']].apply(replaceComma, axis = 1)
        train['F1']    = train[['F1']].apply(replaceComma, axis = 1)
        train['F2']    = train[['F2']].apply(replaceComma, axis = 1)
        train['F3']    = train[['F3']].apply(replaceComma, axis = 1)
        train['F4']    = train[['F4']].apply(replaceComma, axis = 1)
        train['R6']    = train[['R6']].apply(replaceComma, axis = 1)
        train['L3']    = train[['L3']].apply(replaceComma, axis = 1)
        train['1/A1']  = train[['1/A1']].apply(replaceComma, axis = 1)
        train['1/A3']  = train[['1/A3']].apply(replaceComma, axis = 1)
        train['1/F8']  = train[['1/F8']].apply(replaceComma, axis = 1)
        train['F11']   = train[['F11']].apply(replaceComma, axis = 1)
        train['P2']    = train[['P2']].apply(replaceComma, axis = 1)

        bin            = pd.get_dummies(test['binaryrisk'], drop_first = True)
        test           = pd.concat([test,bin], axis = 1)
        test.drop('binaryrisk',axis = 1, inplace = True)

        test['R5']     = test[['R5']].apply(impute_r5, axis = 1)
        test['R3']     = test[['R3']].apply(replaceComma, axis = 1)
        test['R4']     = test[['R4']].apply(replaceComma, axis = 1)
        test['R5']     = test[['R5']].apply(replaceComma, axis = 1)
        test['L1']     = test[['L1']].apply(replaceComma, axis = 1)
        test['L2']     = test[['L2']].apply(replaceComma, axis = 1)
        test['P1']     = test[['P1']].apply(replaceComma, axis = 1)
        test['A2']     = test[['A2']].apply(replaceComma, axis = 1)
        test['A4']     = test[['A4']].apply(replaceComma, axis = 1)
        test['1/A5']   = test[['1/A5']].apply(replaceComma, axis = 1)
        test['A6']     = test[['A6']].apply(replaceComma, axis = 1)
        test['F1']     = test[['F1']].apply(replaceComma, axis = 1)
        test['F2']     = test[['F2']].apply(replaceComma, axis = 1)
        test['F3']     = test[['F3']].apply(replaceComma, axis = 1)
        test['F4']     = test[['F4']].apply(replaceComma, axis = 1)
        test['R6']     = test[['R6']].apply(replaceComma, axis = 1)
        test['L3']     = test[['L3']].apply(replaceComma, axis = 1)
        test['1/A1']   = test[['1/A1']].apply(replaceComma, axis = 1)
        test['1/A3']   = test[['1/A3']].apply(replaceComma, axis = 1)
        test['1/F8']   = test[['1/F8']].apply(replaceComma, axis = 1)
        test['F11']    = test[['F11']].apply(replaceComma, axis = 1)
        test['P2']     = test[['P2']].apply(replaceComma, axis = 1)

        X_train        = train.drop('Target', axis = 1)
        y_train        = train['Target']

        X_train        = train.drop('Target', axis = 1)
        y_train        = train['Target']
        X_test         = test

        rfc            = getClassifier(criteria.classifier)
        rfc.fit(X_train, y_train) # learned by train data and train target

        predictions           = rfc.predict(X_test) # got prediction
        R3                    = pd.DataFrame(X_test['R3'])
        R4                    = pd.DataFrame(X_test['R4'])
        R5                    = pd.DataFrame(X_test['R5'])
        L1                    = pd.DataFrame(X_test['L1'])
        L2                    = pd.DataFrame(X_test['L2'])
        P1                    = pd.DataFrame(X_test['P1'])
        A2                    = pd.DataFrame(X_test['A2'])
        A4                    = pd.DataFrame(X_test['A4'])
        A5                    = pd.DataFrame(X_test['1/A5'])
        A6                    = pd.DataFrame(X_test['A6'])
        F1                    = pd.DataFrame(X_test['F1'])
        F2                    = pd.DataFrame(X_test['F2'])
        F3                    = pd.DataFrame(X_test['F3'])
        F4                    = pd.DataFrame(X_test['F4'])
        R6                    = pd.DataFrame(X_test['R6'])
        L3                    = pd.DataFrame(X_test['L3'])
        A1                    = pd.DataFrame(X_test['1/A1'])
        A3                    = pd.DataFrame(X_test['1/A3'])
        F8                    = pd.DataFrame(X_test['1/F8'])
        Ff                    = pd.DataFrame(X_test['F11'])
        P2                    = pd.DataFrame(X_test['P2'])

        predictions           = pd.DataFrame(predictions)

        predictions.columns   = ['Target']
        predictions['Target'] = predictions[['Target']].apply(string2Number, revert=1, axis = 1) # replace numer risk to string

        risk                  = pd.concat([R3,R4,R5,L1,L2,P1,A2,A4,A5,A6,F1,F2,F3,F4,R6,L3,A1,A3,F8,Ff,P2,predictions], axis = 1)
        risk                  = risk.sort_values(by=['Target'])

        return '{"result": 9, "score": ' + str(0.1) + '}'+ getHTML(risk)

# AUX ------------------------------------
def getHTML(risk):
    html_string     = """<html>
        <style type = "text/css">{style}</style>
        <head><title>HTML Pandas Dataframe with CSS</title></head>
        <body class='mystyle'>
            {table}
        </body
    </html>"""

    with open('static/df_style.css', 'r') as myfile:
        style = myfile.read()

    return html_string.format(table=risk.to_html(classes='mystyle'), style=style)

def getClassifier(classifier):
    if classifier   == 1:
        return  RandomForestClassifier(n_estimators = 151)
    elif classifier == 2:
        return AdaBoostClassifier(n_estimators = 151)
    elif classifier == 3:
        return BaggingClassifier(n_estimators = 151)
    elif classifier == 4:
        return ExtraTreesClassifier(n_estimators = 151)
    elif classifier == 5:
        return GradientBoostingClassifier(n_estimators = 151)
    elif classifier == 6:
        p1 = Pipeline([['clf1', RandomForestClassifier()]])
        p2 = Pipeline([['clf2', AdaBoostClassifier()]])
        return VotingClassifier(estimators=[("p1",p1), ("p2",p2)])

def impute_age(cols):
    Age = cols[0]
    Pclass = cols[1]

    if pd.isnull(Age):
        if Pclass == 1:
            return 37
        elif Pclass == 2:
            return 29
        else:
            return 24
    else:
        return Age

def impute_fare(cols):
    Fare = cols[0]
    Pclass = cols[1]

    if pd.isnull(Fare) or Fare == 0:
        if Pclass == 1:
            return 60
        elif Pclass == 2:
            return 16
        else:
            return 8
    else:
        return Fare

def impute_r5(cols):
    r5 = cols[0]
    try:
        return float(r5)
    except:
        return 0.0028374

def replaceComma(cols):
    num = cols[0]

    if type(num) is str:
        num = num.replace(',', '.')

    return repr(float(num)) # round(float(num), 3) repr - without rouding!
