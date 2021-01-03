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

monthly_awards = []
id = 1

def start():
    loadPlayers()

    month('https://www.basketball-reference.com/awards/pom.html', 'Player of the Month')
    month('https://www.basketball-reference.com/awards/rom.html', 'Rookie of the Month')


    with open('monthly_player_awards.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "player_id", "season", "month",
                         "conference", "award_type"])
        for award in monthly_awards:
            writer.writerow(award)


def month(link, awardType):
    global id
    global monthly_awards

    browser.get(link)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    seasons = soup.select('#div_ .data_grid_group')

    for s in seasons:
        season = s.select_one('h3').get_text()
        grids = s.select('.data_grid_box')
        for grid in grids:
            month = grid.select_one('.gridtitle').get_text()
            players = grid.select('div > p > a')
            players2 = grid.select('div > a')
            if not grid.select('div > p > a'):
                players = grid.select('[data-desc="'+ month +'"]')

            for player in players:
                player_id = int(searchPlayerByURL(player['href'])[0])
                conference = None
                if 'Eastern' in player['data-desc']:
                    conference = 'Eastern'
                elif 'Western' in player['data-desc']:
                    conference = 'Western'
                
                monthly_awards.append([id, player_id, season, month, conference, awardType])
                id += 1
                

if __name__ == "__main__":
    start()
