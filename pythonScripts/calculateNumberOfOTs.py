import csv

def start():

    data = []

    with open('score_by_q.csv', 'r') as file:
        rows = csv.reader(file)
        for i,r in enumerate(rows):
            number_of_ots = None
            if i == 0:
                r.append('number_of_ots')
            else:
                length = len(list(r[1][1:-1].split(',')))
                if length == 4:
                    number_of_ots = 0
                elif len(r[1]) > 4:
                    number_of_ots = length - 4
                r.append(number_of_ots)
            
            data.append(r)

    with open('score_by_q_with_ots.csv', 'w') as file:
        writer = csv.writer(file)
        for d in data:
            writer.writerow(d)

if __name__ == "__main__":
    start()