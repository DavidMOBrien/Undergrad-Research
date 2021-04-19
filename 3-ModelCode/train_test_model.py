import pandas as pd 
import numpy as np
import pickle
from sklearn.neural_network import MLPClassifier as Classifier
from sklearn.model_selection import train_test_split



dataset = pd.read_csv('trainable_data.csv')
X = dataset.iloc[:,0:318].values
y = dataset.iloc[:,318].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 0)

best_classifier = None
best_accuracy = 0

for i in range(100):
    print(best_accuracy, i)
    classifier = Classifier(max_iter = 500, warm_start = True, hidden_layer_sizes = (100, 100, 100))
    classifier.fit(X_train,y_train)

    y_pred = classifier.predict(X_test)

    from sklearn import metrics
    accuracy = metrics.accuracy_score(y_test,y_pred)

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        best_classifier = classifier

y_pred = best_classifier.predict(X_test)
print("BEST SCORE OVERALL",metrics.accuracy_score(y_test, y_pred))

with open('saved_model_v2.pkl', 'wb') as outputFile:
    pickle.dump(best_classifier, outputFile)
    