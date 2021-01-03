import csv
import math
import time
from datetime import timedelta

players = []


def loadPlayers():
    global players
    with open('./csvs/players/players.csv', 'r')as f:
        data = csv.reader(f)
        for row in data:
            players.append(row)

    players = players[1:]


def searchPlayerByURL(url):
    searchedPlayer = None
    for player in players:
        if url == player[-4]:
            searchedPlayer = player
            break

    return searchedPlayer

def searchPlayerByID(id):
    searchedPlayer = None
    for player in players:
        if id == player[0]:
            searchedPlayer = player
            break

    return searchedPlayer


if __name__ == "__main__":
    loadPlayers()
