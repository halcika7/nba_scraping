import csv

def loadData():
    link = 'game_player_data.csv'
    datas = []
    with open(link, 'r')as f:
        data = csv.reader(f)
        for i,row in enumerate(data):
            if i > 0:
                minutes = 0
                seconds = 0
                if ':' in row[5]:
                    [minutes, seconds] = row[5].split(':')
                    minutes = int(minutes) * 60
                    seconds = int(seconds)
                    row[5] = minutes + seconds
                
            datas.append(row)

    with open(link, 'w')as f:
        writer = csv.writer(f)

        for d in datas:
            writer.writerow(d)
    


if __name__ == "__main__":
    loadData()
