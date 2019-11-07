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
        file_path_train = os.path.join(join(dirname(__file__), '..\\..\\static\\csvs\\'), criteria.titles[0].title)
        train           = pd.read_csv(file_path_train, delimiter=";")

        file_path_test = os.path.join(join(dirname(__file__), '..\\..\\static\\csvs\\'), criteria.titles[1].title)
        test            = pd.read_csv(file_path_test, delimiter=";")

        le              = LabelEncoder() # convert string to numbers
        train['Target'] = le.fit_transform(train['Target'])

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
        X_test         = test

        #print(X_train.head())
        #print(y_train.head())
        #print(X_test.head())

        rfc            = getClassifier(criteria.classifier)

        rfc.fit(X_train, y_train) # learned by train data and train target
        predictions    = rfc.predict(X_test) # got prediction
        score          = rfc.score(X_train, y_train)

        # 2 - avarage, 0 - high risk 1 - low, 3 - veri high, 4 very low
        p2                  = pd.DataFrame(X_test['P2'])
        predictions         = pd.DataFrame(predictions)
        predictions.columns = ['target']

        risk                = pd.concat([p2,predictions], axis = 1)
        risk                = risk.sort_values(by=['target'])

        #risk.to_csv('test_predictions.csv', index = False)
        return '{"result": 9, "score": ' + str(score) + '}'+ getHTML(risk)

    def getTitanicPrediction(criteria):
        file_path_train = os.path.join(join(dirname(__file__), '..\\..\\static\\csvs\\'), criteria.titles[0].title)
        train           = pd.read_csv(file_path_train)

        file_path_test = os.path.join(join(dirname(__file__), '..\\..\\static\\csvs\\'), criteria.titles[1].title)
        test            = pd.read_csv(file_path_test)

        #train ---------------------------------------
        train.drop(['PassengerId','Name','Ticket'], axis = 1, inplace = True)

        sex = pd.get_dummies(train['Sex'], drop_first = True)
        train = pd.concat([train,sex], axis = 1)
        train.drop('Sex',axis = 1, inplace = True)

        Embarked = pd.get_dummies(train['Embarked'])
        train = pd.concat([train,Embarked], axis = 1)
        train.drop('Embarked',axis = 1,inplace = True)
        train.drop('Cabin', axis = 1, inplace = True)

        train['Age']  = train[['Age','Pclass']].apply(impute_age, axis = 1)
        train['Fare'] = train[['Fare','Pclass']].apply(impute_fare, axis = 1)

        #test --------------------------------
        PassengerId = pd.DataFrame(test['PassengerId'])
        test.drop(['PassengerId','Name','Ticket'], axis = 1, inplace = True)

        sex = pd.get_dummies(test['Sex'], drop_first = True)
        test = pd.concat([test,sex], axis = 1)
        test.drop('Sex',axis = 1, inplace = True)
        test.drop('Cabin', axis = 1, inplace = True)

        Embarked = pd.get_dummies(test['Embarked'])
        test = pd.concat([test,Embarked], axis = 1)
        test.drop('Embarked',axis = 1,inplace = True)

        test['Age']  = test[['Age','Pclass']].apply(impute_age, axis = 1)
        test['Fare'] = test[['Fare','Pclass']].apply(impute_fare, axis = 1)

        # learning
        X_train     = train.drop('Survived', axis = 1)
        y_train     = train['Survived']
        X_test      = test

        #print(X_train.head())
        #print(X_test.head())

        rfc         = getClassifier(criteria.classifier)
        rfc.fit(X_train, y_train)

        predictions = rfc.predict(X_test)
        score       = rfc.score(X_train, y_train)
        print(score)

        predictions = pd.DataFrame(predictions)
        titanic     = pd.concat([PassengerId,predictions], axis = 1)
        #titanic.to_csv('Improved_predictions.csv', index = False)

        return '{"result": 9, "score": ' + str(score) + '}'+ getHTML(titanic)

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
    return num # round(float(num), 3)

