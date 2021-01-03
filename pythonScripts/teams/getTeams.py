import csv
import time
from bs4 import BeautifulSoup
import requests

teams = []


def start():
    getTeams('https://www.basketball-reference.com/teams/')
    getInactiveTeams('https://www.basketball-reference.com/teams/')

    with open('./csvs/teams.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["team_id", "team_name", "short_name", "years", "total_games",
                         "total_wins", "total_losses", "win_loss_percentage", "champions", "other_names", "link", "active"])
        for team in teams:
            writer.writerow(team)


def getTeams(url):
    html_source = requests.get(url)
    soup = BeautifulSoup(html_source.content, 'html.parser')
    time.sleep(1)
    all_table_rows = soup.select('#teams_active > tbody > tr')
    for index, tr in enumerate(all_table_rows):
        tr["data-row"] = index

    table_rows = soup.select('#teams_active > tbody > tr.full_table')

    data_indexes = [tr.get('data-row') for tr in all_table_rows]

    i = 0
    j = 1

    for index, tr in enumerate(table_rows):
        name = tr.select_one('th[data-stat="franch_name"]').get_text()
        teamlink = tr.select_one('th[data-stat="franch_name"] a').get('href')
        other_names = []
        i += 1
        if all_table_rows[i].get('class')[0] == 'full_table':
            other_names.append(name)
        else:
            while all_table_rows[i].get('class')[0] != 'full_table':
                other_name = all_table_rows[i].select_one(
                    '[data-stat="team_name"]').get_text()
                other_names.append(other_name)
                i += 1
                if i == len(all_table_rows):
                    break
        short_name = tr.select_one('a').get('href')[7:10]
        years = tr.select_one('td[data-stat="years"]').get_text()
        totalGames = tr.select_one('td[data-stat="g"]').get_text()
        totalWins = tr.select_one('td[data-stat="wins"]').get_text()
        totalLosses = tr.select_one('td[data-stat="losses"]').get_text()
        winLossPercentage = tr.select_one(
            'td[data-stat="win_loss_pct"]').get_text()
        champions = tr.select_one(
            'td[data-stat="years_league_champion"]').get_text()
        storeValue = [j, name, short_name, years, totalGames,
                      totalWins, totalLosses, winLossPercentage, champions, other_names, teamlink, True]

        teams.append(storeValue)
        j += 1


def getInactiveTeams(url):
    global teams
    html_source = requests.get(url)
    soup = BeautifulSoup(html_source.content, 'html.parser')
    time.sleep(1)
    all_table_rows = soup.select('#teams_defunct > tbody > tr')
    for index, tr in enumerate(all_table_rows):
        tr["data-row"] = index

    table_rows = soup.select('#teams_defunct > tbody > tr.full_table')
    data_indexes = [tr.get('data-row') for tr in all_table_rows]

    i = 0

    for index, tr in enumerate(table_rows):
        name = tr.select_one('th[data-stat="franch_name"]').get_text()
        teamlink = tr.select_one('th[data-stat="franch_name"] a').get('href')
        other_names = []
        i += 1
        if i < 44:
            if all_table_rows[i].get('class')[0] == 'full_table':
                other_names.append(name)
            else:
                while all_table_rows[i].get('class')[0] != 'full_table':
                    other_name = all_table_rows[i].select_one(
                        '[data-stat="team_name"]').get_text()
                    other_names.append(other_name)
                    i += 1
                    if i == len(all_table_rows):
                        break
            short_name = tr.select_one('a').get('href')[7:10]
            years = tr.select_one('td[data-stat="years"]').get_text()
            totalGames = tr.select_one('td[data-stat="g"]').get_text()
            totalWins = tr.select_one('td[data-stat="wins"]').get_text()
            totalLosses = tr.select_one('td[data-stat="losses"]').get_text()
            winLossPercentage = tr.select_one(
                'td[data-stat="win_loss_pct"]').get_text()
            champions = tr.select_one(
                'td[data-stat="years_league_champion"]').get_text()
            storeValue = [len(teams)+1, name, short_name, years, totalGames,
                          totalWins, totalLosses, winLossPercentage, champions, other_names, teamlink, False]

            teams.append(storeValue)


if __name__ == "__main__":
    start()
