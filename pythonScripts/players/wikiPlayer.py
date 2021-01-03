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

    if sys.argv[1] == 'invalid':
        with open('wikiplayers.csv', 'r') as file:
            reader = csv.reader(file)
            for r in reader:
                if len(r[1]) < 190:
                    with open('invalid.csv', 'a') as file:
                        writer = csv.writer(file)
                        writer.writerow(r)
    else:
        func()

def func():
    with open(sys.argv[1], 'r') as file:
        reader = csv.reader(file)
        number = int(sys.argv[2])
        query = sys.argv[3] #'+basketball+player+image'
        writePath = sys.argv[4] #./images/

        for row in reader:
            name = '+'.join(row[number].split(' '))
            link = 'https://www.google.com/search?q=' + name + query
            browser.get(link)
            html_source = browser.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            wiki_link = ''
            try:
                wiki_link = soup.select_one('a[href*="en.wikipedia"]').get('href')
            except:
                wiki_link = 'https://en.wikipedia.org/wiki/' + '_'.join(row[number].split())


            browser.get(wiki_link)
            html_source = browser.page_source
            soup = BeautifulSoup(html_source, 'html.parser')

            content = soup.select('#mw-content-text > div > p')
            txt = ''
            for p in content:
                txt += p.get_text()

            if ' '.join(txt.split()) == row[number] + ' may refer to:':
                wiki_link = wiki_link + '_(basketball)'
                browser.get(wiki_link)
                html_source = browser.page_source
                soup = BeautifulSoup(html_source, 'html.parser')

                content = soup.select('#mw-content-text > div > p')
                txt = ''
                for p in content:
                    txt += p.get_text()

            
            with open(writePath, 'a') as file:
                writer = csv.writer(file)
                writer.writerow([row[0], ' '.join(txt.split())])


if __name__ == "__main__":
    start()
