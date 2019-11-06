
# DATA SCIENCE
#numpy
@app.route("/getNums")
def getNums():
    n = np.array([2, 3, 4])
    name1 = "name-" + str(n[1])
    return Response('{ "name":"' + name1 + '", "age":31, "city":"New York" }')

@app.route("/api/getAvg", methods=['GET'])
def getAvg():
    val = request.args.get('val')
    print(val)
    l1=val.split(',')
    ar=np.array(l1,dtype=int)
    return Response(str(np.average(ar)))

#matplotlib
@app.route("/api/getImage", methods=['GET'])
def getImage():
        x = np.arange(0, 20 * np.pi, 0.1)
        s = np.cos(x) ** 2
        plt.plot(x, s)
        plt.xlabel('xlabel(X)')
        plt.ylabel('ylabel(Y)')
        plt.title('Simple Graph!')
        plt.grid(True)
        plt.savefig('graph', format="png")
        return send_file("graph", mimetype='image/jpeg')

#pandas
@app.route("/api/getData", methods=['GET'])
def getData():
    module_dir      = os.path.dirname(__file__)
    file_path_train = os.path.join(module_dir, 'train.csv')
    train           = pd.read_csv(file_path_train)
    resultText      = 'Result'
    html_string     = """<html>
        <style type = "text/css">{style}</style>
        <head><title>HTML Pandas Dataframe with CSS</title></head>
        <body class='mystyle' style='color:red'>
            %s
            {table}
        </body
    </html>""" % (resultText)

    with open('df_style.css', 'r') as myfile:
         style = myfile.read()

    print(train.describe())
    return Response(html_string.format(table=train.to_html(classes='mystyle'), style=style))

    #samp = np.random.randint(100, 600, size=(4, 5))
    #df = pd.DataFrame(samp, index=['avi', 'dani', 'rina', 'dina'],
    #                  columns=['Jan', 'Feb', 'Mar', 'Apr', 'May'])
    #return Response(df.to_html(classes='table table-bordered'))

@app.route("/api/getMissingData", methods=['GET'])
def getMissingData():
    plt.figure(figsize = (12,8))
    module_dir      = os.path.dirname(__file__)
    file_path_train = os.path.join(module_dir, 'train.csv')
    train           = pd.read_csv(file_path_train)
    gr = sns.heatmap(train.isnull(), yticklabels = False, cmap = 'viridis', cbar = False)
    plt.savefig('miss', format="png")
    return send_file("miss", mimetype='image/jpeg')

#seaborn
@app.route("/api/getSBData", methods=['GET'])
def getSBData():
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'train.csv')
    df = pd.read_csv(file_path)

    gr=sns.factorplot(x='Survived', hue='Sex', data=df, col='Pclass', kind='count')
    plt.savefig('state', format="png")
    return send_file("state", mimetype='image/jpeg')

@app.route("/api/getTrained", methods=['GET'])
def getTrained():
    module_dir      = os.path.dirname(__file__)
    file_path_train = os.path.join(module_dir, 'train.csv')
    file_path_test  = os.path.join(module_dir, 'test.csv')
    train           = pd.read_csv(file_path_train)
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

    print(X_train.head())
    print(X_test.head())


    rfc = RandomForestClassifier(n_estimators = 151)
    rfc.fit(X_train, y_train)


    predictions = rfc.predict(X_test)

    score = rfc.score(X_train, y_train)
    print(score)

    predictions = pd.DataFrame(predictions)
    titanic     = pd.concat([PassengerId,predictions], axis = 1)

    titanic.to_csv('Improved_predictions.csv', index = False)

    return Response(train.to_html(classes='mystyle'))

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
    print(Pclass)

    if pd.isnull(Fare) or Fare == 0:
        if Pclass == 1:
            return 60
        elif Pclass == 2:
            return 16
        else:
            return 8
    else:
        return Fare

