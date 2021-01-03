import csv
import json

def start():
    array = []
    csvfile = open('./csvs/gamePlayerData.csv', 'r')
    jsonfile = open('./json/gamePlayerData.json', 'w')

    fieldnames = ("id","game_id","team_id","oponent_team_id","player_id","player_name","minutes","FGM","FGA","FGP","FG3M","FG3A","FG3P","FTM","FTA","FTP","ORB","DRB","TRB","AST","STL","BLK","TOV","PF","PTS","plus_minus","reason_not_to_play","reserve","season","playoff")
    reader = csv.DictReader( csvfile, fieldnames)
    for row in reader:
        array.append(row)

    json.dump(array, jsonfile)

if __name__ == "__main__":
    start()
