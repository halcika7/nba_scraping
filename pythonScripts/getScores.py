import csv
from bs4 import BeautifulSoup
from bs4.element import Tag
from searchTeam import searchTeamByName
import requests
from datetime import datetime
from sys import argv

games = []
playoffGames = []
boxScoreLinks = []
playoff = False

id = 63313


def start():
    global games
    global playoffGames
    global playoff

    months = ['october', 'november', 'december', 'january',
              'february', 'march', 'april', 'may', 'june']

    URL = 'https://www.basketball-reference.com/leagues/NBA_'
    regularFilePath = './regular/regular-games-'
    playofFilePath = './playoff/playoff-games-'
    years = []

    for year in range(int(argv[1]), int(argv[2])):
        endYear = getEndYear(year)
        startYear = getStartYear(year)
        years.append([year, 'october', startYear, endYear])
        years.append([year, 'november', startYear, endYear])
        years.append([year, 'december', startYear, endYear])
        years.append([year, 'january', startYear, endYear])
        years.append([year, 'february', startYear, endYear])
        years.append([year, 'march', startYear, endYear])
        years.append([year, 'april', startYear, endYear])
        years.append([year, 'may', startYear, endYear])
        years.append([year, 'june', startYear, endYear])
        writeFile('all-games.csv')
        # writeFile(playofFilePath + startYear +
        #           '-' + endYear + '.csv')

    current_year = int(argv[1])
    for data in years:
        if current_year != data[0]:
            current_year = data[0]
            playoff = False

        getGameData(URL+str(data[0])+'_games-' + data[1] + '.html', data[0])
        with open('all-games.csv', 'a') as file:
            writer = csv.writer(file)
            for g in games:
                writer.writerow(g)

        # with open(playofFilePath + data[2] + '-' + data[3] + '.csv', 'a') as file:
        #     writer = csv.writer(file)
        #     for g in playoffGames:
        #         writer.writerow(g)

        games = []
        playoffGames = []

    with open('boxScoreLinks.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "link", "away_team_id",
                         "home_team_id", "season", "playoff", "date"])
        for link in boxScoreLinks:
            writer.writerow(link)


def getGameData(url, year):
    global playoff
    global id

    html_source = requests.get(url)
    soup = BeautifulSoup(html_source.content, 'html.parser')

    if soup.find('h1').get_text() == 'Page Not Found (404 error)':
        return

    season = soup.select_one(
        'ul.hoversmooth > li.index > a > u').get_text()[:7]
    table_rows = soup.select('#schedule > tbody > tr')

    for tr in table_rows:
        try:
            if (type(tr.contents[0]) is Tag and tr.contents[0].get_text() == 'Playoffs') or url == 'https://www.basketball-reference.com/leagues/NBA_1980_games-april.html':
                playoff = True
        except:
            pass

        # try:
        if not tr.get('class'):
            date = tr.select_one('[data-stat="date_game"]').get_text()
            awayTeamName = tr.select_one(
                '[data-stat="visitor_team_name"]').get_text()
            awayTeamId = int(searchTeamByName(awayTeamName)[0])
            awayTeamScore = tr.select_one(
                '[data-stat="visitor_pts"]').get_text()
            homeTeamName = tr.select_one(
                '[data-stat="home_team_name"]').get_text()
            homeTeamId = int(searchTeamByName(homeTeamName)[0])
            homeTeamScore = tr.select_one(
                '[data-stat="home_pts"]').get_text()
            overtime = tr.select_one('[data-stat="overtimes"]').get_text()
            attendance = tr.select_one(
                '[data-stat="attendance"]').get_text()

            if attendance != '':
                attendance = int(attendance.replace(',', ''))

            notes = tr.select_one('[data-stat="game_remarks"]').get_text()
            boxScoreLink = ''

            try:
                boxScoreLink = 'https://www.basketball-reference.com' + tr.select_one(
                    '[data-stat="box_score_text"] > a').get("href")

            except:
                date2 = datetime.strptime(date, '%a, %b %d, %Y')
                month = date2.month
                day = date2.day
                if month < 10:
                    month = '0' + str(month)
                else:
                    month = str(month)

                if day < 10:
                    day = '0' + str(day)
                else:
                    day = str(day)
                homeShortName = searchTeamByName(homeTeamName)[2]

                boxScoreLink = 'https://www.basketball-reference.com/boxscores/' + \
                    str(date2.year) + month + day + \
                    '0' + homeShortName + '.html'

            storeValue = [id, homeTeamId, homeTeamScore, awayTeamId,
                          awayTeamScore, date, overtime, attendance, playoff, season, notes]

            boxScoreLinks.append(
                [id, boxScoreLink, awayTeamId, homeTeamId, season, playoff, date])

            id += 1

            # if playoff:
            #     playoffGames.append(storeValue)
            # else:
            games.append(storeValue)
        # except:
        #     pass


def getEndYear(year):
    return str(year)[2:]


def getStartYear(year):
    year -= 1
    return str(year)


def writeFile(path):
    with open(path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "home_team_id", "home_team_score", "away_team_id",
                         "away_team_score", "date", "overtime", "attendance", "playoff", "season", "notes"])
        # for game in array:
        #     writer.writerow(game)


if __name__ == "__main__":
    start()
