import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import requests
import sys

chrome_options = Options()
chrome_options.add_experimental_option(
    "excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(
    options=chrome_options,
    executable_path='/Users/harisbeslic/Documents/chrome/chromedriver')

players = []


def start():

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
            anchors = soup.select('#hdtb-msb-vis a')
            for anchor in anchors:
                if anchor.get_text() == 'Slike':
                    link2 = anchor.get('href')
                    browser.get('https://www.google.com'+link2)
                    html_source = browser.page_source
                    soup = BeautifulSoup(html_source, 'html.parser')
                    image_url = soup.select_one('#islrg img').get('data-iurl')
                    img_data = requests.get(image_url).content
                    with open(writePath + row[0] + '.jpg', 'wb') as handler:
                        handler.write(img_data)
                    break


if __name__ == "__main__":
    start()
