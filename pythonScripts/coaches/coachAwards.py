import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from searchCoaches import searchCoachByURL, loadCoaches

chrome_options = Options()
chrome_options.add_experimental_option(
    "excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(
    options=chrome_options,
    executable_path='/Users/harisbeslic/Documents/chrome/chromedriver')

coach_awards = []
id = 1


def start():
    loadCoaches()

    awards('https://www.basketball-reference.com/awards/coy.html', 'Coach of the Year')

    with open('coach_awards.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "coach_id", "season", "award"])
        for award in coach_awards:
            writer.writerow(award)


def awards(link, awardType):
    global id
    global coach_awards

    browser.get(link)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    trs = soup.select('#coyNBA > tbody tr')

    for tr in trs:
        if not tr.get('class'):
            url = tr.select_one('[data-stat="coach"] > a').get('href')
            coach_id = int(searchCoachByURL(url)[0])
            season = tr.select_one('[data-stat="season"] > a').get_text()
            coach_awards.append(
                [id, coach_id, season, awardType])
            id += 1


if __name__ == "__main__":
    start()
