
import csv
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib
import csv
from sklearn.tree import DecisionTreeRegressor
from searchTeam import searchTeamById

games = []


def train():
    global games
    data = []

    games = [[ 10, 26 ]]

    with open('./csvs/all_game_scores.csv', 'r')as f:
        rows = csv.reader(f)
        for i, r in enumerate(rows):
            if i == 0:
                data.append([r[0], r[1], r[2], r[3], r[4]])
            else:
                data.append([r[0], r[1], r[2], r[3], r[4]])

    with open('game_data.csv', 'w')as f:
        writer = csv.writer(f)
        for d in data:
            writer.writerow(d)

    dataset_url1 = 'game_data.csv'

    data1 = pd.read_csv(dataset_url1)

    X = data1.drop(["id"], axis=1)
    X = X.drop(["home_team_score"], axis=1)
    X = X.drop(["away_team_score"], axis=1)

    y = data1['home_team_score']
    z = data1['away_team_score']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.5, random_state=123)

    x_train, x_test, z_train, z_test = train_test_split(
        X, z, test_size=0.5, random_state=123)

    tree_model = DecisionTreeRegressor()

    tree_model.fit(X_train, y_train)
    joblib.dump(tree_model, 'home_predictor.pkl')

    tree_model.fit(x_train, z_train)
    joblib.dump(tree_model, 'away_predictor.pkl')
    print("-" * 48)
    print("\nDone training\n")
    print("-" * 48)


def predict_game_result():
    global games

    tree_model = joblib.load('home_predictor.pkl')
    tree_model1 = joblib.load('away_predictor.pkl')

    temp1 = tree_model.predict(games)
    print(temp1)
    temp2 = tree_model1.predict(games)
    print(temp2)

    with open('game_predictions.csv', 'a')as f:
        rows = csv.writer(f)
        home_team_name = searchTeamById(games[0][0])[1]
        away_team_name = searchTeamById(games[0][1])[1]
        home_result = round(temp1[0], 2)
        away_result = round(temp2[0], 2)
        rows.writerow([home_team_name, home_result, away_team_name, away_result])


if __name__ == "__main__":
    train()
    predict_game_result()
