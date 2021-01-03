import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import sys

chrome_options = Options()
chrome_options.add_experimental_option(
    "excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(
    options=chrome_options,
    executable_path='/Users/harisbeslic/Documents/chrome/chromedriver')

def start():
    with open('./csvs/coaches/coaches.csv', 'r') as file:
        rows = csv.reader(file)
        for i,row in enumerate(rows):
            if i > 234:
                link = 'https://www.google.com/search?q=' + row[1] + '+backetball+coach'
                browser.get(link)
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, 'html.parser')

                wiki_link = soup.select_one('a[href*="en.wikipedia"]').get('href')

                browser.get(wiki_link)
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, 'html.parser')

                content = soup.select('#mw-content-text > div > p')
                txt = ''
                for p in content:
                    txt += p.get_text()
                
                with open('wiki_coaches.csv', 'a') as file:
                    writer = csv.writer(file)
                    writer.writerow([row[0], ' '.join(txt.split())])



if __name__ == "__main__":
    start()
