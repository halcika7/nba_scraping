import csv

def start():
    data = []

    with open('links.csv', 'r') as file:
        rows = csv.reader(file)
        for i,row in enumerate(rows):
            data.append(row)
    
    with open('./csvs/players/players.csv', 'r') as file:
        rows = csv.reader(file)
        j = 0
        for i,row in enumerate(rows):
            if i > 4795:
                data[j][1] = data[j][1] + row[9]
                j += 1
    
    with open('links.csv', 'w') as file:
        rows = csv.writer(file)
        for d in data:
            rows.writerow(d)


if __name__ == "__main__":
    start()