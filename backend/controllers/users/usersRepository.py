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
from   sklearn.ensemble        import RandomForestClassifier
from   sklearn.tree            import DecisionTreeClassifier
from   sklearn.linear_model    import LogisticRegression
from   sklearn.neighbors       import KNeighborsClassifier
from   sklearn.model_selection import GridSearchCV

from sklearn.metrics           import accuracy_score
from sklearn.metrics           import f1_score
from sklearn.metrics           import recall_score
from sklearn.metrics           import precision_score

import numpy                   as np
import matplotlib              as pl
import matplotlib.pyplot       as plt
import pandas                  as pd
import seaborn                 as sns
import os

pl.use('Agg')

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

        train.drop(['binaryrisk'], axis=1, inplace=True)
        test.drop(['binaryrisk'] , axis=1, inplace=True)

        train['Target'] = train['Target'].map({'very high risk': 1, 'high risk': 2, 'the average risk': 3, 'low risk': 4, 'very low risk': 5})

        train           = execValidationTrain(train)
        test            = execValidationTest(test)

        X_train         = train.drop('Target', axis = 1)
        y_train         = train['Target']

        X_train         = train.drop('Target', axis = 1)
        y_train         = train['Target']
        X_test          = test

        if criteria.classifier == 5:
            predictions = getCombinedPredictions(X_train, y_train, X_test)
        else:
            rfc         = getClassifier(criteria.classifier)
            rfc.fit(X_train, y_train) # learned by train data and train target
            predictions = rfc.predict(X_test) # got prediction

        predictions           = pd.DataFrame(predictions)
        predictions.columns   = ['Target']
        predictions['Target'] = predictions['Target'].map({1: 'very high risk', 2: 'high risk', 3: 'the average risk', 4: 'low risk', 5: 'very low risk'})
        result                = pd.concat([pd.DataFrame(X_test['R3']),
                                           pd.DataFrame(X_test['R4']),
                                           pd.DataFrame(X_test['R5']),
                                           pd.DataFrame(X_test['L1']),
                                           pd.DataFrame(X_test['L2']),
                                           pd.DataFrame(X_test['P1']),
                                           pd.DataFrame(X_test['A2']),
                                           pd.DataFrame(X_test['A4']),
                                           pd.DataFrame(X_test['1/A5']),
                                           pd.DataFrame(X_test['A6']),
                                           pd.DataFrame(X_test['F1']),
                                           pd.DataFrame(X_test['F2']),
                                           pd.DataFrame(X_test['F3']),
                                           pd.DataFrame(X_test['F4']),
                                           pd.DataFrame(X_test['R6']),
                                           pd.DataFrame(X_test['L3']),
                                           pd.DataFrame(X_test['1/A1']),
                                           pd.DataFrame(X_test['1/A3']),
                                           pd.DataFrame(X_test['1/F8']),
                                           pd.DataFrame(X_test['F11']),
                                           pd.DataFrame(X_test['P2']),
                                           predictions], axis = 1)

        result                = result.sort_values(by=['Target'])

        return '{"result": 9, "score": ' + str(0.1) + '}'+ getHTML(result)

# AUX ------------------------------------
def getHTML(result):
    html_string     = """<html>
        <style type = "text/css">{style}</style>
        <head><title>HTML Pandas Dataframe with CSS</title></head>
        <body class='mystyle'>
            {table}
        </body
    </html>"""

    with open('static/df_style.css', 'r') as myfile:
        style = myfile.read()

    return html_string.format(table=result.to_html(classes='mystyle'), style=style)

def execValidationTrain(train):
    train           = train.dropna()

    train['R5']     = train[['R5']].apply(replaceComma, axis = 1)
    train['R3']     = train[['R3']].apply(replaceComma, axis = 1)
    train['R4']     = train[['R4']].apply(replaceComma, axis = 1)
    train['R5']     = train[['R5']].apply(replaceComma, axis = 1)
    train['L1']     = train[['L1']].apply(replaceComma, axis = 1)
    train['L2']     = train[['L2']].apply(replaceComma, axis = 1)
    train['P1']     = train[['P1']].apply(replaceComma, axis = 1)
    train['A2']     = train[['A2']].apply(replaceComma, axis = 1)
    train['A4']     = train[['A4']].apply(replaceComma, axis = 1)
    train['1/A5']   = train[['1/A5']].apply(replaceComma, axis = 1)
    train['A6']     = train[['A6']].apply(replaceComma, axis = 1)
    train['F1']     = train[['F1']].apply(replaceComma, axis = 1)
    train['F2']     = train[['F2']].apply(replaceComma, axis = 1)
    train['F3']     = train[['F3']].apply(replaceComma, axis = 1)
    train['F4']     = train[['F4']].apply(replaceComma, axis = 1)
    train['R6']     = train[['R6']].apply(replaceComma, axis = 1)
    train['L3']     = train[['L3']].apply(replaceComma, axis = 1)
    train['1/A1']   = train[['1/A1']].apply(replaceComma, axis = 1)
    train['1/A3']   = train[['1/A3']].apply(replaceComma, axis = 1)
    train['1/F8']   = train[['1/F8']].apply(replaceComma, axis = 1)
    train['F11']    = train[['F11']].apply(replaceComma, axis = 1)
    train['P2']     = train[['P2']].apply(replaceComma, axis = 1)
    return train

def execValidationTest(test):
    test            = test.dropna()

    test['R5']      = test[['R5']].apply(replaceComma, axis = 1)
    test['R3']      = test[['R3']].apply(replaceComma, axis = 1)
    test['R4']      = test[['R4']].apply(replaceComma, axis = 1)
    test['R5']      = test[['R5']].apply(replaceComma, axis = 1)
    test['L1']      = test[['L1']].apply(replaceComma, axis = 1)
    test['L2']      = test[['L2']].apply(replaceComma, axis = 1)
    test['P1']      = test[['P1']].apply(replaceComma, axis = 1)
    test['A2']      = test[['A2']].apply(replaceComma, axis = 1)
    test['A4']      = test[['A4']].apply(replaceComma, axis = 1)
    test['1/A5']    = test[['1/A5']].apply(replaceComma, axis = 1)
    test['A6']      = test[['A6']].apply(replaceComma, axis = 1)
    test['F1']      = test[['F1']].apply(replaceComma, axis = 1)
    test['F2']      = test[['F2']].apply(replaceComma, axis = 1)
    test['F3']      = test[['F3']].apply(replaceComma, axis = 1)
    test['F4']      = test[['F4']].apply(replaceComma, axis = 1)
    test['R6']      = test[['R6']].apply(replaceComma, axis = 1)
    test['L3']      = test[['L3']].apply(replaceComma, axis = 1)
    test['1/A1']    = test[['1/A1']].apply(replaceComma, axis = 1)
    test['1/A3']    = test[['1/A3']].apply(replaceComma, axis = 1)
    test['1/F8']    = test[['1/F8']].apply(replaceComma, axis = 1)
    test['F11']     = test[['F11']].apply(replaceComma, axis = 1)
    test['P2']      = test[['P2']].apply(replaceComma, axis = 1)
    return test

def getClassifier(classifier):
    if classifier   == 1:
        return LogisticRegression(n_jobs=-1, random_state=17, C=33)
    elif classifier == 2:
        return KNeighborsClassifier(n_neighbors = 23)
    elif classifier == 3:
        return DecisionTreeClassifier(random_state=17, min_samples_split=2, max_depth=3, max_features=0.7)
    elif classifier == 4:
        return RandomForestClassifier(random_state=56, n_jobs=-1, oob_score=True, max_depth=4, max_features=1, n_estimators=2)

def getCombinedPredictions(X_train, y_train, X_test):
    lr              = getClassifier(1)
    lr.fit(X_train, y_train)
    predictions_lr = lr.predict(X_test)

    knc             = getClassifier(2)
    knc.fit(X_train, y_train)
    predictions_knc = knc.predict(X_test)

    dtc             = getClassifier(3)
    dtc.fit(X_train, y_train)
    predictions_dtc = dtc.predict(X_test)

    rfc             = getClassifier(4)
    rfc.fit(X_train, y_train)
    predictions_rfc = rfc.predict(X_test)

    predictions     = (predictions_lr + predictions_knc + predictions_dtc + predictions_rfc)
    return (predictions / 4).round()

def replaceComma(cols):
    num = cols[0]

    if type(num) is str:
        num = num.replace(',', '.')

    return repr(float(num))
