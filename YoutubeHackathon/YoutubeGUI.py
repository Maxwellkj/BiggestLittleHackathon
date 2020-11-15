import PySimpleGUI as sg
from joblib import dump, load
import numpy as np
import pandas as pd

clf = load('Prediction.joblib')
sg.theme('Dark Blue 3')  # please make your windows colorful

layout = [[sg.Text('Enter Number of Ratings: \t'), sg.Input(key = '-RatingCount-', size = (20,1))],
          [sg.Text('Enter Average Rating: \t'), sg.Input(key = '-AvgRating-', size = (20,1))],
          [sg.Text('Number of Comments: \t'), sg.Input(key = '-CommentCount-', size = (20,1))],
          [sg.Text(key = '-OUT-', size = (50,2))],
          [sg.Text('')],
          [sg.Button('Predict'), sg.Button('Exit')]]

window = sg.Window('Predict Views', layout)

while True:  # Event Loop
    event, values = window.read()
    print(event, values)
    if event == sg.WIN_CLOSED or event == 'Exit':
        break
    if event == 'Predict':
        # change the "output" element to be the value of "input" element
        print(int(values['-RatingCount-']))
        X = (float(values['-AvgRating-']), int(values['-RatingCount-']), int(values['-CommentCount-']),
             (float(values['-AvgRating-'])-3.0) * int(values['-RatingCount-']),
             (int(values['-RatingCount-'])+.01)/(int(values['-CommentCount-'])+.01), 
            int(values['-RatingCount-'])-int(values['-CommentCount-']))
        X= np.reshape(X, (1,-1))
        print(X)
        Predict_X = clf.predict(X)
        if Predict_X[0] == 1:
            window['-OUT-'].update('Based on the given data, this program predicts that the video has less than 10,000 Views.')
        elif Predict_X[0] == 2:
            window['-OUT-'].update('Based on the given data, this program predicts that the video has between 10,000 and 50,000 Views.')
        elif Predict_X[0] == 3:
            window['-OUT-'].update('Based on the given data, this program predicts that the video has between 50,000 and 250,000 Views.')
        elif Predict_X[0] == 4:
            window['-OUT-'].update('Based on the given data, this program predicts that the video has between 250,000 and 1,000,000 Views.')
        elif Predict_X[0] == 5:
            window['-OUT-'].update('Based on the given data, this program predicts that the video has greater than 1,000,000 Views.')
        
        print(values)

window.close()