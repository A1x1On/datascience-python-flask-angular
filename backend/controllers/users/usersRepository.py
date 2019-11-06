import numpy                   as np
import matplotlib              as pl
import matplotlib.pyplot       as plt
import pandas                  as pd
import seaborn                 as sns
from sklearn.pipeline          import Pipeline
from   sklearn.ensemble        import RandomForestClassifier
from   sklearn.ensemble        import GradientBoostingClassifier
from   sklearn.ensemble        import ExtraTreesClassifier
from   sklearn.ensemble        import BaggingClassifier
from   sklearn.ensemble        import AdaBoostClassifier
from   sklearn.ensemble        import VotingClassifier

from   sklearn.model_selection import GridSearchCV

import os
from os.path import dirname, join
from werkzeug.utils import secure_filename


pl.use('Agg')

class Repository():
    def get(criteria):
        print('RUNS', criteria)

        l1=criteria.split(',')
        ar=np.array(l1,dtype=int)

        return str(np.average(ar))
    def prepareFile(file):

        print(file)
        print(file.filename)


        df = pd.DataFrame.from_dict(file)
        print(df.head())
        return 'succs'
        #pd.DataFrame(np_array).to_csv("path/to/file.csv")

    def getTrained(criteria):

        print(criteria.classifier)

        #module_dir      = os.path.dirname(__file__)
        file_path_train = os.path.join(join(dirname(__file__), '..\\..\\temp\\csvs\\'), criteria.titles[0].title)
        train           = pd.read_csv(file_path_train)

        file_path_test = os.path.join(join(dirname(__file__), '..\\..\\temp\\csvs\\'), criteria.titles[1].title)
        test            = pd.read_csv(file_path_test)

        #train ---------------------------------------
        train.drop(['PassengerId','Name','Ticket'], axis = 1, inplace = True)

        sex = pd.get_dummies(train['Sex'], drop_first = True) # превратить строки в числовые уникальные порказатели
        train = pd.concat([train,sex], axis = 1) # зделать concat в таблицу train колонку sex
        train.drop('Sex',axis = 1, inplace = True) # удалить старую колонку sex со строковыми значениями

        Embarked = pd.get_dummies(train['Embarked'])
        train = pd.concat([train,Embarked], axis = 1)
        train.drop('Embarked',axis = 1,inplace = True)
        train.drop('Cabin', axis = 1, inplace = True)

        train['Age']  = train[['Age','Pclass']].apply(impute_age, axis = 1)
        train['Fare'] = train[['Fare','Pclass']].apply(impute_fare, axis = 1)

        #test --------------------------------
        PassengerId = pd.DataFrame(test['PassengerId']) # соъроняем колонку для будущего конката ее после получения результатов для test
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
        X_train = train.drop('Survived', axis = 1)
        y_train = train['Survived']
        X_test  = test

        #print(X_train.head())
        #print(X_test.head())


        if criteria.classifier == 1:
            rfc = RandomForestClassifier(n_estimators = 151)
        elif criteria.classifier == 2:
            rfc = AdaBoostClassifier(n_estimators = 151)
        elif criteria.classifier == 3:
            rfc = BaggingClassifier(n_estimators = 151)
        elif criteria.classifier == 4:
            rfc = ExtraTreesClassifier(n_estimators = 151)
        elif criteria.classifier == 5:
            rfc = GradientBoostingClassifier(n_estimators = 151)
        elif criteria.classifier == 6:
            p1 = Pipeline([['clf1', RandomForestClassifier()]])
            p2 = Pipeline([['clf2', AdaBoostClassifier()]])
            rfc = VotingClassifier(estimators=[("p1",p1), ("p2",p2)])


        rfc.fit(X_train, y_train)

        predictions = rfc.predict(X_test)

        score = rfc.score(X_train, y_train)
        print(score)

        predictions = pd.DataFrame(predictions)
        titanic     = pd.concat([PassengerId,predictions], axis = 1)
        #titanic.to_csv('Improved_predictions.csv', index = False)



        resultText      = ''
        html_string     = """<html>
            <style type = "text/css">{style}</style>
            <head><title>HTML Pandas Dataframe with CSS</title></head>
            <body class='mystyle'>
                %s
                {table}
            </body
        </html>""" % (resultText)

        with open('df_style.css', 'r') as myfile:
            style = myfile.read()

        html = html_string.format(table=train.to_html(classes='mystyle'), style=style)

        response = '{"result": 9, "score": ' + str(score) + '}'+ html

        return response


        #return train.to_html(classes='mystyle')


        #return Response('TRAINED!!!!!!!!!!!!!!')

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

