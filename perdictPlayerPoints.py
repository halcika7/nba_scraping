
import numpy as np
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import csv
from sklearn.tree import DecisionTreeRegressor

playersA = []
playersB = []


def train():
    global playersA
    global playersB
    data = []

    tima = 10
    timb = 26

    with open('players.csv', 'r')as f:
        rows = csv.reader(f)
        for i, r in enumerate(rows):
            if i > 0:
                if r[-3] != '':
                    if int(r[-3]) == tima and r[-1] == 'False':
                        playersA.append([timb, int(r[0])])
                    elif int(r[-3]) == timb and r[-1] == 'False':
                        playersB.append([tima, int(r[0])])

    with open('p.csv', 'r')as f:
        rows = csv.reader(f)
        for r in rows:
            for p in playersA:
                if p[1] == int(r[0]):
                    p.append(float(r[1]))
                    p.append(float(r[2]))
                    p.append(float(r[3]))
                    p.append(float(r[4]))

            for p in playersB:
                if p[1] == int(r[0]):
                    p.append(float(r[1]))
                    p.append(float(r[2]))
                    p.append(float(r[3]))
                    p.append(float(r[4]))

    for i,p in enumerate(playersA):
        if len(p) != 6:
            del playersA[i]
    for i,p in enumerate(playersB):
        if len(p) != 6:
            del playersB[i]

    with open('game_player_data.csv', 'r')as f:
        rows = csv.reader(f)
        for i, r in enumerate(rows):
            if i == 0:
                data.append([r[3], r[4], r[5], r[6], r[9], r[12], r[23]])
            else:
                if r[-4] == '':
                    if r[5] != '' and r[23] != '':
                        if r[6] == '':
                            r[6] = 0
                        if r[12] == '':
                            r[12] = 0
                        if r[9] == '':
                            r[9] = 0
                        r[5] = round(int(r[5]) / 60, 2)
                        data.append(
                            [r[3], r[4], r[5], r[6], r[9], r[12], r[23]])

    # print(data)
    with open('game_data.csv', 'w')as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow(d)

    dataset_url1 = 'game_data.csv'

    data1 = pd.read_csv(dataset_url1)

    X = data1.drop(["pts"], axis=1)

    y = data1['pts']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=123)

    tree_model = DecisionTreeRegressor()

    tree_model.fit(X_train, y_train)
    joblib.dump(tree_model, 'weather_predictor.pkl')
    print("-" * 48)
    print("\nDone training\n")
    print("-" * 48)


def predict_payer_points():
    global playersA
    del playersA[-1]
    global playersB

    tree_model = joblib.load('player_points_predictor.pkl')
    # # 27
    # # 21

    temp1 = tree_model.predict(playersA)
    temp2 = tree_model.predict(playersB)
    with open('players.csv', 'r')as f:
        rows = csv.reader(f)
        for i, r in enumerate(rows):
            if i > 0:
                for p in playersA:
                    if p[1] == int(r[0]):
                        p.append(r[1])
                for p in playersB:
                    if p[1] == int(r[0]):
                        p.append(r[1])

    for i, t in enumerate(temp1):
        playersA[i].append(t)

    for i, t in enumerate(temp2):
        playersB[i].append(t)

    with open('predictions.csv', 'w')as f:
        writer = csv.writer(f)
        writer.writerow(['opponent_id', 'player_id', 'min_per_game_this_season', 'fg_per_game_this_season',
                         'fg3_per_game_this_season', 'ft_per_game_this_season', 'player_name', 'predicted_pts'])

        for r in playersA:
            writer.writerow(r)
        for r in playersB:
            writer.writerow(r)


if __name__ == "__main__":
    # X is our input variables that will be used to predict y which is our output so points
    # the data in X needs to be converted to numeric values to simplify our process
    train()
    predict_payer_points()
