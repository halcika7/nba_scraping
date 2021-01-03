import csv
import math
import time
from datetime import timedelta

coaches = []


def loadCoaches():
    global coaches
    with open('./csvs/coaches/coaches.csv', 'r')as f:
        data = csv.reader(f)
        for row in data:
            coaches.append(row)

    coaches = coaches[1:]


def searchCoachByURL(url):
    searchedoach = None
    for coach in coaches:
        if url == coach[-1]:
            searchedoach = coach
            break

    return searchedoach


if __name__ == "__main__":
    loadCoaches()
