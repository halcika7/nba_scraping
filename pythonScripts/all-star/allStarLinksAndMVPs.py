import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from searchPlayer import searchPlayerByURL, loadPlayers

chrome_options = Options()
chrome_options.add_experimental_option(
    "excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(
    options=chrome_options,
    executable_path='/Users/harisbeslic/Documents/chrome/chromedriver')

allstar_links = []
allstar_mvps = []
id = 69
mvp_id = 73


def start():
    global id
    global mvp_id
    global allstar_links
    global allstar_mvps

    loadPlayers()

    browser.get('https://www.basketball-reference.com/allstar/')
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    trs = soup.select('#all_star_games_nba > tbody tr')

    for tr in trs:
        if not tr.get('class') and tr['data-row'] != '0':
            tds = tr.select('td')
            year = int(tds[0].select_one('a').get_text())
            season = str(year - 1) + '-' + str(year)[-2:]
            allstar_link = 'https://www.basketball-reference.com' + tds[4].select_one('a').get('href')
            location = tds[-1].get_text()
            mvps = tds[5].select('a')
            for m in mvps:
                url = m['href']
                player_id = int(searchPlayerByURL(url)[0])
                allstar_mvps.append([mvp_id, id, player_id, season])
                mvp_id -= 1
            
            allstar_links.append([id, season, location, allstar_link])
            id -= 1

    with open('allstar_links.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "season", "location", "allstar_link"])
        for award in allstar_links:
            writer.writerow(award)

    with open('allstar_mvps.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "game_id", "player_id", "season"])
        for award in allstar_mvps:
            writer.writerow(award)


if __name__ == "__main__":
    start()
