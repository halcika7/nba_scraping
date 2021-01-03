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

monthly_awards = []
id = 1

def start():
    loadCoaches()

    month('https://www.basketball-reference.com/awards/com.html', 'Coach of the Month')


    with open('monthly_coach_awards.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "coach_id", "season", "month",
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
            coaches = grid.select('div > p > a')
            if not grid.select('div > p > a'):
                coaches = grid.select('[data-desc="'+ month +'"]')

            for coach in coaches:
                coach_id = int(searchCoachByURL(coach['href'])[0])
                conference = None
                if 'Eastern' in coach['data-desc']:
                    conference = 'Eastern'
                elif 'Western' in coach['data-desc']:
                    conference = 'Western'
                
                monthly_awards.append([id, coach_id, season, month, conference, awardType])
                id += 1
                

if __name__ == "__main__":
    start()
