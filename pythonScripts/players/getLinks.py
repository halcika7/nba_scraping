import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import datetime

chrome_options = Options()
chrome_options.add_experimental_option(
    "excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(
    options=chrome_options,
    executable_path='/Users/harisbeslic/Documents/chrome/chromedriver')

links = []

id = 1


def start():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
               'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'y', 'z']
    URL = 'https://www.basketball-reference.com/players/'

    for letter in letters:
        getPlayers(URL + letter + '/')

    with open('links.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["ID", 'Link', "Position","Retired"])
        for link in links:
            writer.writerow(link)

    browser.quit()


def getPlayers(url):
    global id
    browser.get(url)
    html_source = browser.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    for tr in soup.select('#players > tbody > tr.thead'): 
        tr.decompose()
    table_rows = soup.select('#players > tbody > tr')

    for tr in table_rows:
        try:
            link = 'https://www.basketball-reference.com' + tr.select_one('[data-stat="player"] a').get('href')
            position = tr.select_one('[data-stat="pos"]').get_text()
            retired = False
            now = datetime.datetime.now()
            if int(tr.select_one('[data-stat="year_max"]').get_text()) < now.year:
                retired = True
            links.append([id, link, position, retired])
            id += 1
        except:
            break


if __name__ == "__main__":
    start()
