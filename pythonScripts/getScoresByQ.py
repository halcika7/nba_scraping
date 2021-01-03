import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from sys import argv

def start():

    data = []

    with open('boxScoreLinks.csv', 'r') as file:
        rows = csv.reader(file)
        for i,r in enumerate(rows):
            if i > 0:
                if int(r[0]) >= int(argv[1]) and int(r[0]) < int(argv[2]):
                    data.append(r)

    for d in data:
        html = requests.get(d[1])
        a = html.text.replace('<!--', '')
        b = a.replace('-->', '')
        soup = BeautifulSoup(b, 'html.parser')
        away_team_scores = []
        home_team_scores = []
        if soup.select('#line_score'):
            trs = soup.select('#line_score tr')[2:]
            aways = trs[0].select('.center')[:-1]
            homes = trs[1].select('.center')[:-1]

            for i,a in enumerate(aways):
                away_team_scores.append(int(a.get_text()))
                home_team_scores.append(int(homes[i].get_text()))

        with open('score_by_q.csv', 'a') as file:
            writer = csv.writer(file)
            writer.writerow([d[0], away_team_scores, home_team_scores])
                


if __name__ == "__main__":
    start()