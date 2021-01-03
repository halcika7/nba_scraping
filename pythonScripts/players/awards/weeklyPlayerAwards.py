import csv
from searchPlayer import searchPlayerByURL, loadPlayers
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_experimental_option(
    "excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(
    options=chrome_options,
    executable_path='/Users/harisbeslic/Documents/chrome/chromedriver')

weekly_awards = []
id = 1

def start():
    loadPlayers()

    week('https://www.basketball-reference.com/awards/pow.html', 'Player of the Week')


    with open('weekly_player_awards.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "player_id", "season", "month", "week",
                         "conference", "award_type"])
        for award in weekly_awards:
            writer.writerow(award)


def week(link, awardType):
    global id
    global weekly_awards

    browser.get(link)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    seasons = soup.select('#div_ .data_grid_group')

    for s in seasons:
        season = s.select_one('h3').get_text()
        grids = s.select('div.data_grid_box')
        for grid in grids:
            month = grid.select_one('div.gridtitle').get_text()
            weeks = grid.select('div')[1]
            weeks = weeks.select('p')

            for w in weeks:
                week = w.select_one('strong:first-child').get_text()
                players = w.select('a')

                for player in players:
                    player_id = int(searchPlayerByURL(player['href'])[0])
                    conference = None
                    if 'Eastern' in player['data-desc']:
                        conference = 'Eastern'
                    elif 'Western' in player['data-desc']:
                        conference = 'Western'
                    
                    weekly_awards.append([id, player_id, season, month, week, conference, awardType])
                    id += 1
                

if __name__ == "__main__":
    start()
