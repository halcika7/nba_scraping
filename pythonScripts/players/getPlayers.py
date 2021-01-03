import csv
from bs4 import BeautifulSoup
from searchTeam import searchTeamByName, searchTeamByShortName
import requests

links = []


def start():
    global links

    with open('links.csv', 'rt')as f:
        data = csv.reader(f)
        for row in data:
            links.append(row)

    links = links[1:]

    for link in links:
        getPlayerData(link)


def getPlayerData(url):
    html = requests.get(url[1])
    soup = BeautifulSoup(html.content, 'html.parser')
    team_ids = soup.select('#per_game > tfoot > tr [data-stat=team_id]')
    div = soup.select_one(
        '#meta > div[itemtype="https://schema.org/Person"]')

    teams = []
    fullName = ''
    name = ''
    current_team_id = ''
    birth_place = ''
    birth_date = ''
    height = ''
    weight = ''
    playerUrl = '/'.join(url[1].split('/')[-3:])
    retired = url[3]
    name = div.select_one('h1').get_text().strip()
    injury = False

    for team_id in team_ids:
        shortName = team_id.get_text()
        if searchTeamByShortName(shortName) != None:
            teams.append(int(searchTeamByShortName(shortName)))

    if div.select_one('p:nth-child(2) > strong').get_text().strip() == 'Pronunciation':
        fullName = div.select_one(
            'p:nth-child(3) > strong').get_text().strip()
    else:
        fullName = div.select_one(
            'p:nth-child(2) > strong').get_text().strip()

    try:
        height = div.select_one('span[itemprop="height"]').get_text()
    except:
        pass

    try:
        weight = div.select_one('span[itemprop="weight"]').get_text()[:-2]
    except:
        pass

    try:
        birth_date = div.select_one('#necro-birth > a:first-child').get_text().strip(
        ) + " " + div.select_one('#necro-birth > a:nth-child(2)').get_text().strip()
    except:
        pass

    try:
        find_current_team = div.select_one(
            '[href*="/2020.html"]').get_text()
        current_team_id = searchTeamByName(find_current_team)[0]
        if len(teams) == 0 and current_team_id:
            teams.append(current_team_id)
    except:
        pass

    try:
        birth_place = div.select_one(
            'span[itemprop="birthPlace"]').get_text().strip()[3:]
    except:
        pass

    if soup.select_one('#injury'):
        injury = True

    with open('players.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([url[0], name, fullName, url[2], height, weight,
                         birth_date, birth_place, retired, playerUrl, current_team_id, teams, injury])


if __name__ == "__main__":
    start()
