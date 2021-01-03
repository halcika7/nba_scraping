import csv
from bs4 import BeautifulSoup
import requests

players = []

url = 'https://www.basketball-reference.com'

tima = 10
timb = 26

with open('players.csv', 'r')as f:
    rows = csv.reader(f)
    for i,r in enumerate(rows):
        if i > 0 and r[-3] != '' and r[-1] == 'False':
            if int(r[-3]) == tima or int(r[-3]) == timb:
                players.append([int(r[0]), url + r[-4]])



for i,player in enumerate(players):

    html = requests.get(player[1])
    soup = BeautifulSoup(html.content, 'html.parser')
    if soup.select_one('#per_game'):
        tr = soup.select('#per_game tbody tr')[-1]

        minutes = tr.select_one('[data-stat="mp_per_g"]').get_text()
        fg = tr.select_one('[data-stat="fg_per_g"]').get_text()
        fg3 = tr.select_one('[data-stat="fg3_per_g"]').get_text()
        ft = tr.select_one('[data-stat="ft_per_g"]').get_text()
        player_id = player[0]

        with open('p.csv', 'a')as f:
            rows = csv.writer(f)
            rows.writerow([player_id, minutes, fg, fg3, ft])

