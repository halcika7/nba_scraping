from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from searchPlayer import loadPlayers, searchPlayerByURL
from searchTeam import searchTeamByName
import csv

chrome_options = Options()
chrome_options.add_experimental_option(
    "excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(
    options=chrome_options,
    executable_path='/Users/harisbeslic/Documents/chrome/chromedriver')

allChampions = []
allAwards = []


def start():
    loadPlayers()

    for year in range(1950, 2020):
        browser.get('https://www.basketball-reference.com/leagues/NBA_' + str(year) + '.html')
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'html.parser')
        season = str(year-1) + '-' + str(year)[-2:]
        getChampions(soup, season)
    
    award('https://www.basketball-reference.com/awards/all_star_mvp.html', 'all_star_mvp_NBA', 'allstar')
    award('https://www.basketball-reference.com/awards/smoy.html', 'smoy_NBA', 'six')
    award('https://www.basketball-reference.com/awards/dpoy.html', 'dpoy_NBA', 'def')
    award('https://www.basketball-reference.com/awards/mip.html', 'mip_NBA', 'mip')
    award('https://www.basketball-reference.com/awards/roy.html', 'roy_NBA', 'rok')
    award('https://www.basketball-reference.com/awards/mvp.html', 'mvp_NBA', 'mvp')
    award('https://www.basketball-reference.com/awards/finals_mvp.html', 'finals_mvp_NBA', 'fmvp')

    allLeagueAward('https://www.basketball-reference.com/awards/all_rookie.html', 'awards_all_rookie', 'All-Rookie ')
    allLeagueAward('https://www.basketball-reference.com/awards/all_defense.html', 'awards_all_defense', 'All-Defensive ')
    allLeagueAward('https://www.basketball-reference.com/awards/all_league.html', 'awards_all_league', 'All-League ')

    with open('champions.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["team_id", "season"])
        for r in allChampions:
            writer.writerow(r)

    with open('awards.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["player_id", "season", "award"])
        for r in allAwards:
            writer.writerow(r)


def getChampions(soup, season):
    global allChampions
    p = soup.select_one('#meta > div:nth-child(2) > p')
    a = p.select_one('a')
    name = a.get_text()
    team_id = int(searchTeamByName(name)[0])
    allChampions.append([team_id, season])

def award(link, id, t):
    global allAwards
    browser.get(link)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    trs = soup.select('table#'+ id +' tbody > tr')

    for tr in trs:
        if not tr.get('class'):
            season = tr.select_one('[data-stat="season"] > a').get_text()
            player_url = tr.select_one('[data-stat="player"] > a').get('href')
            player_id = int(searchPlayerByURL(player_url)[0])
            if t == 'six':
                allAwards.append([player_id, season, 'Sixth Man of the Year'])
            elif t == 'def':
                allAwards.append([player_id, season, 'Defensive Player of the Year'])
            elif t == 'mip':
                allAwards.append([player_id, season, 'Most Improved Player of the Year'])
            elif t == 'rok':
                allAwards.append([player_id, season, 'Rookie of the Year'])
            elif t == 'mvp':
                allAwards.append([player_id, season, 'Most Valuable Player of the Year'])
            elif t == 'fmvp':
                allAwards.append([player_id, season, 'Finals Most Valuable Player'])

def allLeagueAward(link, id, t):
    global allAwards
    browser.get(link)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    trs = soup.select('table#'+ id +' tbody > tr')

    for tr in trs:
        if not tr.get('class'):
            season = tr.select_one('[data-stat="season"] > a').get_text()
            team = tr.select_one('[data-stat="all_team"]').get_text()
            if tr.select_one('[data-stat="lg_id"] > a').get_text() == 'NBA':
                try:
                    player_id_1 = int(searchPlayerByURL(tr.select_one('[data-stat="1"] > a').get('href'))[0])
                    player_id_2 = int(searchPlayerByURL(tr.select_one('[data-stat="2"] > a').get('href'))[0])
                    player_id_3 = int(searchPlayerByURL(tr.select_one('[data-stat="3"] > a').get('href'))[0])
                    player_id_4 = int(searchPlayerByURL(tr.select_one('[data-stat="4"] > a').get('href'))[0])
                    award = t + team + " Team"
                    allAwards.append([player_id_1, season, award])
                    allAwards.append([player_id_2, season, award])
                    allAwards.append([player_id_3, season, award])
                    allAwards.append([player_id_4, season, award])
                    player_id_5s = tr.select('[data-stat="5"] > a')
                    for a in player_id_5s:
                        player_id = int(searchPlayerByURL(a.get('href'))[0])
                        allAwards.append([player_id, season, award])
                except:
                    pass

                try:
                    player_id_1 = int(searchPlayerByURL(tr.select_one('[data-stat="6"] > a').get('href'))[0])
                    player_id_2 = int(searchPlayerByURL(tr.select_one('[data-stat="7"] > a').get('href'))[0])
                    player_id_3 = int(searchPlayerByURL(tr.select_one('[data-stat="8"] > a').get('href'))[0])
                    player_id_4 = int(searchPlayerByURL(tr.select_one('[data-stat="9"] > a').get('href'))[0])
                    award = t + team + " Team"
                    allAwards.append([player_id_1, season, award])
                    allAwards.append([player_id_2, season, award])
                    allAwards.append([player_id_3, season, award])
                    allAwards.append([player_id_4, season, award])
                    player_id_5s = tr.select('[data-stat="10"] > a')
                    for a in player_id_5s:
                        player_id = int(searchPlayerByURL(a.get('href'))[0])
                        allAwards.append([player_id, season, award])
                except:
                    pass

                try:
                    player_id_1 = int(searchPlayerByURL(tr.select_one('[data-stat="11"] > a').get('href'))[0])
                    player_id_2 = int(searchPlayerByURL(tr.select_one('[data-stat="12"] > a').get('href'))[0])
                    player_id_3 = int(searchPlayerByURL(tr.select_one('[data-stat="13"] > a').get('href'))[0])
                    player_id_4 = int(searchPlayerByURL(tr.select_one('[data-stat="14"] > a').get('href'))[0])
                    award = t + team + " Team"
                    allAwards.append([player_id_1, season, award])
                    allAwards.append([player_id_2, season, award])
                    allAwards.append([player_id_3, season, award])
                    allAwards.append([player_id_4, season, award])
                    player_id_5s = tr.select('[data-stat="15"] > a')
                    for a in player_id_5s:
                        player_id = int(searchPlayerByURL(a.get('href'))[0])
                        allAwards.append([player_id, season, award])
                except:
                    pass


if __name__ == "__main__":
    start()
