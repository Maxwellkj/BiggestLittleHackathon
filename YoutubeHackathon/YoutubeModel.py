from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from joblib import dump, load
import os


#parses all lines in the file, stores data
def extractData(file1, total, target):
    for line in file1:
        currentIndex = 0
        lineStorage = []

        # separates data within line
        while len(line) > 1:
            index = line.find('\t')
            if index == -1:
                index = len(line)
            data = line[0:index]
            line = line[index+1:len(line)]

            #length, views, rate, ratings, and number of comments of each video stored for later
            if 5 <= currentIndex <= 8:
                if currentIndex == 5:
                    target += [float(data)]  # total views
                #elif currentIndex == 6:
                    #x=0
                else:
                    lineStorage += [float(data)]

            currentIndex += 1

        if currentIndex >= 4:
            lineStorage += [(lineStorage[0] - 3.0) * lineStorage[1]]  # comment quality * num comments
            lineStorage += [(lineStorage[1] + 0.01) / (lineStorage[2] + 0.01)]  # num ratings / num comments
            lineStorage += [lineStorage[2] - lineStorage[1]]  # comments - ratings

            total += [lineStorage]

totalData = []
targetData = []

cwd = os.getcwd()
# extracts data from files
extractData(open(cwd + "/0.txt", "r"), totalData, targetData)
extractData(open(cwd + "/1.txt", "r"), totalData, targetData)
extractData(open(cwd + "/2.txt", "r"), totalData, targetData)
extractData(open(cwd + "/3.txt", "r"), totalData, targetData)

viewSave = []


#separates data into training and test sections
trainData, testData, trainTarget, testTarget = train_test_split(totalData, targetData, test_size=0.2, random_state=None)

x = 0
for data in trainTarget:
    #if data < 1000.0:
        #data = 1
    if data< 10000.0:
        data = 1
    elif data < 50000.0:
        data = 2
    elif data < 250000.0:
        data = 3
    elif data < 1000000.0:
        data = 4
    else:
        data = 5

    trainTarget[x] = data
    x += 1
    
x = 0
for data in testTarget:
    viewSave += [data]
    #if data < 1000.0:
        #data = 1
    if data< 10000.0:
        data = 1
    elif data < 50000.0:
        data = 2
    elif data < 250000.0:
        data = 3
    elif data < 1000000.0:
        data = 4
    else:
        data = 5

    testTarget[x] = data
    x += 1

viewPredict = AdaBoostClassifier(n_estimators = 400, learning_rate = .7)


viewPredict.fit(trainData, trainTarget)
prediction = viewPredict.predict(testData)

sampleTest = []

print(viewPredict.score(testData, testTarget))
disp = plot_confusion_matrix(viewPredict, testData, testTarget,normalize='true')

print("Confusion Matrix")
print(disp.confusion_matrix)

dump(viewPredict, 'Prediction.joblib')