import csv
from sys import argv

def start():

    data = []
    id = 1

    with open(argv[1], 'r') as file:
        rows = csv.reader(file)
        for i,row in enumerate(rows):
            if i > 0:
                row[0] = i
                i += 1
            data.append(row)

    with open(argv[1], 'w') as file:
        writer = csv.writer(file)
        for d in data:
            writer.writerow(d)



if __name__ == "__main__":
    start()
