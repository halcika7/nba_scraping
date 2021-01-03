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

other_plyer_awards = []
id = 1


def start():
    loadPlayers()

    month('https://www.basketball-reference.com/awards/nba_50_greatest.html', '50 Greatest Players', 1996)
    
    month('https://www.basketball-reference.com/awards/nba_silver_anniversary.html', 'NBA Silver Anniversary Team', 1971)

    month('https://www.basketball-reference.com/awards/slam_500_greatest.html', 'SLAM 500 Greatest NBA Players of All Time', 2011)

    month('https://www.basketball-reference.com/awards/simmons_pyramid.html', 'Bill Simmons Hall of Fame Pyramid', 2010)

    month('https://www.basketball-reference.com/awards/nba_35th_anniversary.html', 'NBA 35th Anniversary All-Time Team', 1980)

    other('https://www.basketball-reference.com/awards/tmoy.html', 'Teammate of the Year', 'tmoy_NBA')

    other('https://www.basketball-reference.com/awards/citizenship.html', 'J. Walter Kennedy Citizenship', 'citizenship_NBA')

    other('https://www.basketball-reference.com/awards/cpoy.html', 'Comeback Player of the Year', 'cpoy_NBA')

    other('https://www.basketball-reference.com/awards/tsn_mvp.html', 'Sporting News MVP', 'tsn_mvp_NBA')

    other('https://www.basketball-reference.com/awards/tsn_roy.html', 'Sporting News Rookie of the Year', 'tsn_roy_NBA')


    with open('other_player_awards.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "payer_id", "award", "year"])
        for award in other_plyer_awards:
            writer.writerow(award)


def month(link, awardType, year):
    global id
    global other_plyer_awards

    browser.get(link)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    trs = soup.select('#stats > tbody tr')

    for tr in trs:
        if not tr.get('class'):
            url = tr.select_one('[data-stat="player"] > a').get('href')
            player_id = int(searchPlayerByURL(url)[0])
            other_plyer_awards.append(
                [id, player_id, awardType, year])
            id += 1

def other(link, awardType, tableId):
    global id
    global other_plyer_awards

    browser.get(link)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    trs = soup.select('#' + tableId + ' > tbody tr')

    for tr in trs:
        if not tr.get('class'):
            url = tr.select_one('[data-stat="player"] > a').get('href')
            player_id = int(searchPlayerByURL(url)[0])
            year = int(tr.select_one('[data-stat="season"]').get_text()[:-3])
            other_plyer_awards.append(
                [id, player_id, awardType, year])
            id += 1


if __name__ == "__main__":
    start()
