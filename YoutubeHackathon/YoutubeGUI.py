import PySimpleGUI as sg
import main as model
from joblib import dump, load

clf = load('filename.joblib')
sg.theme('Dark Blue 3')  # please make your windows colorful

layout = [[sg.Text('Enter Video Length: \t'), sg.Input(key = '-IN-', size = (20,1))],
          [sg.Text('Enter Number of Ratings: \t'), sg.Input(key = '-RatingCount-', size = (20,1))],
          [sg.Text('Enter Average Rating: \t'), sg.Input(key = '-AvgRating-', size = (20,1))],
          [sg.Text('Number of Comments: \t'), sg.Input(key = '-CommentCount-', size = (20,1))],
          [sg.Text('')],
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
        X = [values['-RatingCount-'], values['-CommentCount-']]
        clf.predict(X)
        print(values)

window.close()