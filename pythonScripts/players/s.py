import csv

def start():
    id = 1
    data = []

    with open('game_player_data.csv', 'w')as f:
        writer = csv.writer(f)
        writer.writerow(['id','game_id','team_id','opponent_team_id','player_id','minutes','fg','fga','fgp','fg3','fg3a','fg3p','ft','fta','ftp','orb','drb','trb','ast','stl','blk','tov','pf','pts','plus_minus','reason_not_to_play','reserve','season','playoff'])

    for year in range(1950, 2021):
        path = './csvs/gamePlayerData/gamePlayerData'+ str(year-1)+ '-' + str(year)[2:] + '.csv'

        with open(path, 'r')as f:
            rows = csv.reader(f)
            for i,r in enumerate(rows):
                if i > 0:
                    with open('game_player_data.csv', 'a')as f:
                        writer = csv.writer(f)
                        r.insert(0, id)
                        writer.writerow(r)
                        id += 1

    

if __name__ == "__main__":
    start()