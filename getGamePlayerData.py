import csv
from bs4 import BeautifulSoup
from searchPlayer import loadPlayers, searchPlayerByURL
import requests
import sys

boxScores = []

filepath = './csvs/gamePlayerData/gamePlayerData' + sys.argv[1] + '.csv'


def start():
    loadPlayers()

    global boxScores
    with open('./csvs/other/boxScoreLinks.csv', 'r')as f:
        data = csv.reader(f)
        for row in data:

            if row[4] == sys.argv[1]:
                boxScores.append(row)

    with open(filepath,"a+") as f:
        writer = csv.writer(f)
        writer.writerow(['Game ID','Team ID', 'Oponent Team ID','Player ID','Minutes','FGM','FGA','FGP','FG3M','FG3A','FG3P','FTM','FTA','FTP','ORB','DRB','TRB','AST','STL','BLK','TOV','PF','PTS','PLUS MINUS','Reason not to play','Reserve','Season','Playoff'])

    for bs in boxScores:
        getData(bs)


def getData(bsData):
    html = requests.get(bsData[1])
    if html.text == '':
        return
    soup = BeautifulSoup(html.content, 'html.parser')
    all_tables = soup.select('table[id$=game-basic]')
    homeTeamRows = all_tables[1].select('tbody > tr')
    awayTeamRows = all_tables[0].select('tbody > tr')
    homeReserves = False
    awayReserves = False

    for row in homeTeamRows:
        if row.get('class'):
            homeReserves = True
        else:
            pData = getRowData(row)
            if pData != False:
                pData.insert(0, bsData[0])
                pData.insert(1, bsData[3])
                pData.insert(2, bsData[2])
                pData.append(homeReserves)
                pData.append(bsData[4])
                pData.append(bsData[-2])
                appendRow(pData)

    for row in awayTeamRows:

        if row.get('class'):
            awayReserves = True
        else:
            pData = getRowData(row)
            if pData != False:
                pData.insert(0, bsData[0])
                pData.insert(1, bsData[2])
                pData.insert(2, bsData[3])
                pData.append(awayReserves)
                pData.append(bsData[4])
                pData.append(bsData[-2])
                appendRow(pData)


def appendRow(data):
    with open(filepath, 'a') as file:
        writer = csv.writer(file)
        writer.writerow(data)


def getRowData(row):
    linkPlayer = row.select_one('[data-stat="player"] a').get('href')
    player = searchPlayerByURL(linkPlayer)
    if not player[0]:
        return False
    playerId = player[0]
    if row.select_one('[data-stat="reason"]'):
        return [playerId, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', row.select_one('[data-stat="reason"]').get_text()]
    minutes = row.select_one('[data-stat="mp"]').get_text()
    fgm = row.select_one('[data-stat="fg"]').get_text()
    fga = row.select_one('[data-stat="fga"]').get_text()
    fgperc = row.select_one('[data-stat="fg_pct"]').get_text()
    fg3m = ''
    if row.select_one('[data-stat="fg3"]'):
        fg3m = row.select_one('[data-stat="fg3"]').get_text()
    fg3a = ''
    if row.select_one('[data-stat="fg3a"]'):
        fg3a = row.select_one('[data-stat="fg3a"]').get_text()
    fg3perc = ''
    if row.select_one('[data-stat="fg3_pct"]'):
        fg3perc = row.select_one('[data-stat="fg3_pct"]').get_text()
    ftm = row.select_one('[data-stat="ft"]').get_text()
    fta = row.select_one('[data-stat="fta"]').get_text()
    ftperc = row.select_one('[data-stat="ft_pct"]').get_text()
    oreb = row.select_one('[data-stat="orb"]').get_text()
    dreb = row.select_one('[data-stat="drb"]').get_text()
    treb = row.select_one('[data-stat="trb"]').get_text()
    ast = row.select_one('[data-stat="ast"]').get_text()
    stl = row.select_one('[data-stat="stl"]').get_text()
    blk = row.select_one('[data-stat="blk"]').get_text()
    tov = row.select_one('[data-stat="tov"]').get_text()
    pf = row.select_one('[data-stat="pf"]').get_text()
    pts = row.select_one('[data-stat="pts"]').get_text()
    plus_minus = ''
    if row.select_one('[data-stat="plus_minus"]'):
        plus_minus = row.select_one('[data-stat="plus_minus"]').get_text()

    return [playerId, minutes, fgm, fga, fgperc, fg3m, fg3a, fg3perc, ftm, fta, ftperc, oreb, dreb, treb, ast, stl, blk, tov, pf, pts, plus_minus, '']


if __name__ == "__main__":
    start()
