from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import plot_confusion_matrix
from sklearn import svm
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from joblib import dump, load

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
            total += [lineStorage]


totalData = []
targetData = []

# extracts data from files
extractData(open("C:/Users/mj4ey/Documents/YoutubeHackathon/0.txt", "r"), totalData, targetData)
extractData(open("C:/Users/mj4ey/Documents/YoutubeHackathon/1.txt", "r"), totalData, targetData)
extractData(open("C:/Users/mj4ey/Documents/YoutubeHackathon/2.txt", "r"), totalData, targetData)
extractData(open("C:/Users/mj4ey/Documents/YoutubeHackathon/3.txt", "r"), totalData, targetData)

x = 0
for data in targetData:
    if data < 10000.0:
        data = 1
    elif data < 50000.0:
        data = 2
    elif data < 250000.0:
        data = 3
    elif data < 1000000.0:
        data = 4
    else:
        data = 5

    targetData[x] = data
    x += 1

#separates data into training and test sections
trainData, testData, trainTarget, testTarget = train_test_split(totalData, targetData, test_size=0.2, random_state=None)

#viewPredict = svm.SVC(gamma=0.001)

from sklearn.neighbors import KNeighborsClassifier

#viewPredict = KNeighborsClassifier(n_neighbors = 60, weights = 'uniform')
viewPredict = AdaBoostClassifier(n_estimators = 300, learning_rate = .5)
#viewPredict = RandomForestClassifier(n_estimators=400, max_depth=50, min_samples_split=30)

viewPredict.fit(trainData, trainTarget)
prediction = viewPredict.predict(testData)

sampleTest = []

print(viewPredict.score(testData, testTarget))
disp = plot_confusion_matrix(viewPredict, testData, testTarget,normalize='true')

print("Confusion Matrix")
print(disp.confusion_matrix)

dump(viewPredict, 'Prediction.joblib')

x = 0
for video in testData:
    views = targetData[x]

    x += 1

    #print("\nLength: " + str(runtime) + "\nViews: " + str(views) + "\nRating: " + str(rate) + "\nNumber of ratings: " +
    #      str(ratings) + "\nComments: " + str(comments))


