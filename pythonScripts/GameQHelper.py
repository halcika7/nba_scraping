import csv

def start():

    game_data = []

    with open('all-games.csv', 'r') as file:
        rows = csv.reader(file)
        for i,row in enumerate(rows):
            if i == 0:
                row.insert(5,'away_team_scores')
                row.insert(6, 'home_team_scores')
                row.insert(7, 'number_of_ots')
            game_data.append(row)
    
    with open('score_by_q_with_ots.csv', 'r') as file:
        rows = csv.reader(file)
        for i,row in enumerate(rows):
            if i > 0:
                game_data[i].insert(5,row[1])
                game_data[i].insert(6, row[2])
                game_data[i].insert(7, row[3])

    with open('all_game_data.csv', 'w') as file:
        writer = csv.writer(file)
        for r in game_data:
            writer.writerow(r)



if __name__ == "__main__":
    start()