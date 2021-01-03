import csv
from bs4 import BeautifulSoup
from bs4.element import Tag
from searchTeam import searchTeamByName
import requests


def start():
    id = 1
    coaches = []
    html_source = requests.get('https://www.basketball-reference.com/coaches/NBA_stats.html')
    soup = BeautifulSoup(html_source.content, 'html.parser')
    all_trs = soup.select('#coaches > tbody tr', class_=None)
    for tr in all_trs:
        if not tr.get('class'):
            link = tr.select_one('[data-stat="coach"] > a').get('href')
            full_link = 'https://www.basketball-reference.com' + tr.select_one('[data-stat="coach"] > a').get('href')
            started = int(tr.select_one('[data-stat="year_min"]').get_text())
            year_max = int(tr.select_one('[data-stat="year_max"]').get_text())
            years_coaching = int(tr.select_one('[data-stat="years"]').get_text())
            retired = False
            if year_max < 2020:
                retired = True
            coaches.append([id, link, full_link, started, year_max, years_coaching, retired])
            id += 1
    
    with open('coachesLinks.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "link", "full_link",
                         "started_coaching", "last_coach_season", "years_coaching", "retired"])
        for coach in coaches:
            writer.writerow(coach)

if __name__ == "__main__":
    start()
