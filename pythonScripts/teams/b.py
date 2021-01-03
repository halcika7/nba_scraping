import csv
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from bs4.element import Tag
from searchTeam import searchTeamByName
from time import sleep

chrome_options = Options()
chrome_options.add_experimental_option(
    "excludeSwitches", ["ignore-certificate-errors"])
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--headless')

browser = webdriver.Chrome(
    options=chrome_options,
    executable_path='/Users/harisbeslic/Documents/chrome/chromedriver')


def start():
    URL = 'https://www.basketball-reference.com/leagues/NBA_'

    # Team Per Game Stats
    team_per_game_stats = []
    id1 = 1
    # Opponent Per Game Stats
    opponent_per_game_stats = []
    id2 = 1
    # Team Stats
    team_season_stats = []
    id3 = 1
    # Opponent Stats
    opponent_season_stats = []
    id4 = 1
    # Team Per 100 Poss Stats
    team_per_100_poss_stast = []
    id5 = 1
    # Opponent Per 100 Poss Stats
    opponent_per_100_poss_stats = []
    id6 = 1
    # Miscellaneous Stats
    miscellaneous_stats = []
    id7 = 1
    # Team Shooting
    team_season_shooting = []
    id8 = 1
    # Opponent Shooting
    opponent_season_shooting = []
    id9 = 1

    for year in range(1950, 2021):
        season = getStartYear(year) + '-' + getEndYear(year)
        url = URL + str(year) + '.html'

        browser.get(url)
        html_source = browser.page_source
        soup = BeautifulSoup(html_source, 'html.parser')

        if soup.select_one('#team-stats-per_game'):
            trs = soup.select('#team-stats-per_game tbody > tr')
            try:
                for tr in trs:
                    if not tr.get('class'):
                        data = helperOne(tr, id1, season)
                        id1 += 1
                        team_per_game_stats.append(data)
            except:
                print(season)
                print(url)
                print('id1')
                break

        if soup.select_one('#opponent-stats-per_game'):
            trs = soup.select('#opponent-stats-per_game tbody > tr')
            try:
                for tr in trs:
                    if not tr.get('class'):
                        data = helperTwo(tr, id2, season)
                        id2 += 1
                        opponent_per_game_stats.append(data)
            except:
                print(season)
                print(url)
                print('id2')
                break

        if soup.select_one('#team-stats-base'):
            trs = soup.select('#team-stats-base tbody > tr')
            try:
                for tr in trs:
                    if not tr.get('class'):
                        data = helperOne(tr, id3, season)
                        id3 += 1
                        team_season_stats.append(data)
            except:
                print(season)
                print(url)
                print('id3')
                break

        if soup.select_one('#opponent-stats-base'):
            trs = soup.select('#opponent-stats-base tbody > tr')
            try:
                for tr in trs:
                    if not tr.get('class'):
                        data = helperTwo(tr, id4, season)
                        id4 += 1
                        opponent_season_stats.append(data)
            except:
                print(season)
                print(url)
                print('id4')
                break

        if soup.select_one('#team-stats-per_poss'):
            trs = soup.select('#team-stats-per_poss tbody > tr')
            try:
                for tr in trs:
                    if not tr.get('class'):
                        data = helperOne(tr, id5, season)
                        id5 += 1
                        team_per_100_poss_stast.append(data)
            except:
                print(season)
                print(url)
                print('id5')
                break

        if soup.select_one('#opponent-stats-per_poss'):
            trs = soup.select('#opponent-stats-per_poss tbody > tr')
            try:
                for tr in trs:
                    if not tr.get('class'):
                        data = helperTwo(tr, id6, season)
                        id6 += 1
                        opponent_per_100_poss_stats.append(data)
            except:
                print(season)
                print(url)
                print('id6')
                break

        if soup.select_one('#misc_stats'):
            trs = soup.select('#misc_stats tbody > tr')
            try:
                for tr in trs:
                    if not tr.get('class'):
                        data = helperThree(tr, id7, season)
                        id7 += 1
                        miscellaneous_stats.append(data)
            except:
                print(season)
                print(url)
                print('id7')
                break

        if soup.select_one('#team_shooting'):
            trs = soup.select('#team_shooting tbody > tr')
            try:
                for tr in trs:
                    if not tr.get('class'):
                        data = helperFour(tr, id8, season)
                        id8 += 1
                        team_season_shooting.append(data)
            except:
                print(season)
                print(url)
                print('id8')
                break

        if soup.select_one('#opponent_shooting'):
            trs = soup.select('#opponent_shooting tbody > tr')
            try:
                for tr in trs:
                    if not tr.get('class'):
                        data = helperFive(tr, id9, season)
                        id9 += 1
                        opponent_season_shooting.append(data)
            except:
                print(season)
                print(url)
                print('id9')
                break

    writeFile('team_per_game_stats.csv', team_per_game_stats, 0)
    writeFile('opponent_per_game_stats.csv', opponent_per_game_stats, 0)
    writeFile('team_season_stats.csv', team_season_stats, 0)
    writeFile('opponent_season_stats.csv', opponent_season_stats, 0)
    writeFile('team_per_100_poss_stast.csv', team_per_100_poss_stast, 0)
    writeFile('opponent_per_100_poss_stats.csv',
              opponent_per_100_poss_stats, 0)

    writeFile('miscellaneous_stats.csv', miscellaneous_stats, 1)
    writeFile('team_season_shooting.csv', team_season_shooting, 2)
    writeFile('opponent_season_shooting.csv', opponent_season_shooting, 2)


def helperOne(row, id, season):
    team_id = int(searchTeamByName(row.select_one('[data-stat="team_name"] > a').get_text())[0])
    g = toIntOrFloat(row, '[data-stat="g"]')
    mp = toIntOrFloat(row, '[data-stat="mp"]')
    fg = toIntOrFloat(row, '[data-stat="fg"]')
    fga = toIntOrFloat(row, '[data-stat="fga"]')
    fg_pct = toIntOrFloat(row, '[data-stat="fg_pct"]')
    fg3 = toIntOrFloat(row, '[data-stat="fg3"]')
    fg3a = toIntOrFloat(row, '[data-stat="fg3a"]')
    fg3_pct = toIntOrFloat(row, '[data-stat="fg3_pct"]')
    fg2 = toIntOrFloat(row, '[data-stat="fg2"]')
    fg2a = toIntOrFloat(row, '[data-stat="fg2a"]')
    fg2_pct = toIntOrFloat(row, '[data-stat="fg2_pct"]')
    ft = toIntOrFloat(row, '[data-stat="ft"]')
    fta = toIntOrFloat(row, '[data-stat="fta"]')
    ft_pct = toIntOrFloat(row, '[data-stat="ft_pct"]')
    orb = toIntOrFloat(row, '[data-stat="orb"]')
    drb = toIntOrFloat(row, '[data-stat="drb"]')
    trb = toIntOrFloat(row, '[data-stat="trb"]')
    ast = toIntOrFloat(row, '[data-stat="ast"]')
    stl = toIntOrFloat(row, '[data-stat="stl"]')
    blk = toIntOrFloat(row, '[data-stat="blk"]')
    tov = toIntOrFloat(row, '[data-stat="tov"]')
    pf = toIntOrFloat(row, '[data-stat="pf"]')
    pts = toIntOrFloat(row, '[data-stat="pts"]')

    return [id, team_id, season, g, mp, fg, fga, fg_pct, fg3, fg3a, fg3_pct, fg2, fg2a, fg2_pct, ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, tov, pf, pts]


def helperTwo(row, id, season):
    team_id = int(searchTeamByName(row.select_one('[data-stat="team_name"] > a').get_text())[0])
    g = toIntOrFloat(row, '[data-stat="g"]')
    mp = toIntOrFloat(row, '[data-stat="mp"]')
    fg = toIntOrFloat(row, '[data-stat="opp_fg"]')
    fga = toIntOrFloat(row, '[data-stat="opp_fga"]')
    fg_pct = toIntOrFloat(row, '[data-stat="opp_fg_pct"]')
    fg3 = toIntOrFloat(row, '[data-stat="opp_fg3"]')
    fg3a = toIntOrFloat(row, '[data-stat="opp_fg3a"]')
    fg3_pct = toIntOrFloat(row, '[data-stat="opp_fg3_pct"]')
    fg2 = toIntOrFloat(row, '[data-stat="opp_fg2"]')
    fg2a = toIntOrFloat(row, '[data-stat="opp_fg2a"]')
    fg2_pct = toIntOrFloat(row, '[data-stat="opp_fg2_pct"]')
    ft = toIntOrFloat(row, '[data-stat="opp_ft"]')
    fta = toIntOrFloat(row, '[data-stat="opp_fta"]')
    ft_pct = toIntOrFloat(row, '[data-stat="opp_ft_pct"]')
    orb = toIntOrFloat(row, '[data-stat="opp_orb"]')
    drb = toIntOrFloat(row, '[data-stat="opp_drb"]')
    trb = toIntOrFloat(row, '[data-stat="opp_trb"]')
    ast = toIntOrFloat(row, '[data-stat="opp_ast"]')
    stl = toIntOrFloat(row, '[data-stat="opp_stl"]')
    blk = toIntOrFloat(row, '[data-stat="opp_blk"]')
    tov = toIntOrFloat(row, '[data-stat="opp_tov"]')
    pf = toIntOrFloat(row, '[data-stat="opp_pf"]')
    pts = toIntOrFloat(row, '[data-stat="opp_pts"]')

    return [id, team_id, season, g, mp, fg, fga, fg_pct, fg3, fg3a, fg3_pct, fg2, fg2a, fg2_pct, ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, tov, pf, pts]


def helperThree(row, id, season):
    # id team_id season age wins losses wins_pyth losses_pyth mov sos srs off_rtg def_rtg net_rtg pace fta_per_fga_pct fg3a_per_fga_pct ts_pct efg_pct tov_pct orb_pct ft_rate opp_efg_pct opp_tov_pct drb_pct opp_ft_rate arena_name attendance attendance_per_g
    team_id = int(searchTeamByName(row.select_one(
        '[data-stat="team_name"] > a').get_text())[0])
    age = toIntOrFloat(row, '[data-stat="age"]')
    wins = toIntOrFloat(row, '[data-stat="wins"]')
    losses = toIntOrFloat(row, '[data-stat="g"]')
    wins_pyth = toIntOrFloat(row, '[data-stat="wins_pyth"]')
    losses_pyth = toIntOrFloat(row, '[data-stat="losses_pyth"]')
    mov = toIntOrFloat(row, '[data-stat="mov"]')
    sos = toIntOrFloat(row, '[data-stat="sos"]')
    srs = toIntOrFloat(row, '[data-stat="srs"]')
    off_rtg = toIntOrFloat(row, '[data-stat="off_rtg"]')
    def_rtg = toIntOrFloat(row, '[data-stat="def_rtg"]')
    net_rtg = toIntOrFloat(row, '[data-stat="net_rtg"]')
    pace = toIntOrFloat(row, '[data-stat="pace"]')
    fta_per_fga_pct = toIntOrFloat(row, '[data-stat="fta_per_fga_pct"]')
    fg3a_per_fga_pct = toIntOrFloat(row, '[data-stat="fg3a_per_fga_pct"]')
    ts_pct = toIntOrFloat(row, '[data-stat="ts_pct"]')
    efg_pct = toIntOrFloat(row, '[data-stat="efg_pct"]')
    tov_pct = toIntOrFloat(row, '[data-stat="tov_pct"]')
    orb_pct = toIntOrFloat(row, '[data-stat="orb_pct"]')
    ft_rate = toIntOrFloat(row, '[data-stat="ft_rate"]')
    opp_efg_pct = toIntOrFloat(row, '[data-stat="opp_efg_pct"]')
    opp_tov_pct = toIntOrFloat(row, '[data-stat="opp_tov_pct"]')
    drb_pct = toIntOrFloat(row, '[data-stat="drb_pct"]')
    opp_ft_rate = toIntOrFloat(row, '[data-stat="opp_ft_rate"]')
    arena_name = row.select_one('[data-stat="arena_name"]').get_text()
    attendance = toIntOrFloat(row, '[data-stat="attendance"]')
    attendance_per_g = toIntOrFloat(row, '[data-stat="attendance_per_g"]')

    return [id, team_id, season, age, wins, losses, wins_pyth, losses_pyth, mov, sos, srs, off_rtg, def_rtg, net_rtg, pace, fta_per_fga_pct, fg3a_per_fga_pct, ts_pct, efg_pct, tov_pct, orb_pct, ft_rate, opp_efg_pct, opp_tov_pct, drb_pct, opp_ft_rate, arena_name, attendance, attendance_per_g]


def helperFour(row, id, season):
    # 'id', 'team_id', 'season', 'g', 'mp' 'fg_pct', avg_dist, fg2a_ct_fga, pct_fga_00_03, pct_fga_03_10, pct_fga_10_16, pct_fga_16_xx, fg3a_pct_fga, fg2_pct, fg_pct_00_03, fg_pct_03_10, fg_pct_10_16, fg_pct_16_xx, fg3_pct, fg2_pct_ast, pct_fg2_dunk, fg2_dunk, pct_fg2_layup, fg2_layup, fg3_pct_ast, pct_fg3a_corner, fg3_pct_corner, fg3a_heave, fg3_heave
    team_id = int(searchTeamByName(row.select_one(
        '[data-stat="team_name"] > a').get_text())[0])
    g = toIntOrFloat(row, '[data-stat="g"]')
    mp = toIntOrFloat(row, '[data-stat="mp"]')
    fg_pct = toIntOrFloat(row, '[data-stat="fg_pct"]')
    avg_dist = toIntOrFloat(row, '[data-stat="avg_dist"]')
    fg2a_ct_fga = toIntOrFloat(row, '[data-stat="fg2a_ct_fga"]')
    pct_fga_00_03 = toIntOrFloat(row, '[data-stat="pct_fga_00_03"]')
    pct_fga_03_10 = toIntOrFloat(row, '[data-stat="pct_fga_03_10"]')
    pct_fga_10_16 = toIntOrFloat(row, '[data-stat="pct_fga_10_16"]')
    pct_fga_16_xx = toIntOrFloat(row, '[data-stat="pct_fga_16_xx"]')
    fg3a_pct_fga = toIntOrFloat(row, '[data-stat="fg3a_pct_fga"]')
    fg2_pct = toIntOrFloat(row, '[data-stat="fg2_pct"]')
    fg_pct_00_03 = toIntOrFloat(row, '[data-stat="fg_pct_00_03"]')
    fg_pct_03_10 = toIntOrFloat(row, '[data-stat="fg_pct_03_10"]')
    fg_pct_10_16 = toIntOrFloat(row, '[data-stat="fg_pct_10_16"]')
    fg_pct_16_xx = toIntOrFloat(row, '[data-stat="fg_pct_16_xx"]')
    fg3_pct = toIntOrFloat(row, '[data-stat="fg3_pct"]')
    fg2_pct_ast = toIntOrFloat(row, '[data-stat="fg2_pct_ast"]')
    pct_fg2_dunk = toIntOrFloat(row, '[data-stat="pct_fg2_dunk"]')
    fg2_dunk = toIntOrFloat(row, '[data-stat="fg2_dunk"]')
    pct_fg2_layup = toIntOrFloat(row, '[data-stat="pct_fg2_layup"]')
    fg2_layup = toIntOrFloat(row, '[data-stat="fg2_layup"]')
    fg3_pct_ast = toIntOrFloat(row, '[data-stat="fg3_pct_ast"]')
    pct_fg3a_corner = toIntOrFloat(row, '[data-stat="pct_fg3a_corner"]')
    fg3_pct_corner = toIntOrFloat(row, '[data-stat="fg3_pct_corner"]')
    fg3a_heave = toIntOrFloat(row, '[data-stat="fg3a_heave"]')
    fg3_heave = toIntOrFloat(row, '[data-stat="fg3_heave"]')

    return [id, team_id, season, g, mp, fg_pct, avg_dist, fg2a_ct_fga, pct_fga_00_03, pct_fga_03_10, pct_fga_10_16, pct_fga_16_xx,  fg3a_pct_fga, fg2_pct, fg_pct_00_03, fg_pct_03_10, fg_pct_10_16, fg_pct_16_xx, fg3_pct, fg2_pct_ast, pct_fg2_dunk, fg2_dunk, pct_fg2_layup, fg2_layup, fg3_pct_ast, pct_fg3a_corner, fg3_pct_corner, fg3a_heave, fg3_heave]


def helperFive(row, id, season):
    # 'id', 'team_id', 'season', 'g', 'mp' 'fg_pct', avg_dist, fg2a_ct_fga, pct_fga_00_03, pct_fga_03_10, pct_fga_10_16, pct_fga_16_xx, fg3a_pct_fga, fg2_pct, fg_pct_00_03, fg_pct_03_10, fg_pct_10_16, fg_pct_16_xx, fg3_pct, fg2_pct_ast, pct_fg2_dunk, fg2_dunk, pct_fg2_layup, fg2_layup, fg3_pct_ast, pct_fg3a_corner, fg3_pct_corner, fg3a_heave, fg3_heave
    team_id = int(searchTeamByName(row.select_one(
        '[data-stat="team_name"] > a').get_text())[0])
    g = toIntOrFloat(row, '[data-stat="g"]')
    mp = toIntOrFloat(row, '[data-stat="mp"]')
    fg_pct = toIntOrFloat(row, '[data-stat="opp_fg_pct"]')
    avg_dist = toIntOrFloat(row, '[data-stat="opp_avg_dist"]')
    fg2a_ct_fga = toIntOrFloat(row, '[data-stat="opp_fg2a_ct_fga"]')
    pct_fga_00_03 = toIntOrFloat(row, '[data-stat="opp_pct_fga_00_03"]')
    pct_fga_03_10 = toIntOrFloat(row, '[data-stat="opp_pct_fga_03_10"]')
    pct_fga_10_16 = toIntOrFloat(row, '[data-stat="opp_pct_fga_10_16"]')
    pct_fga_16_xx = toIntOrFloat(row, '[data-stat="opp_pct_fga_16_xx"]')
    fg3a_pct_fga = toIntOrFloat(row, '[data-stat="opp_fg3a_pct_fga"]')
    fg2_pct = toIntOrFloat(row, '[data-stat="opp_fg2_pct"]')
    fg_pct_00_03 = toIntOrFloat(row, '[data-stat="opp_fg_pct_00_03"]')
    fg_pct_03_10 = toIntOrFloat(row, '[data-stat="opp_fg_pct_03_10"]')
    fg_pct_10_16 = toIntOrFloat(row, '[data-stat="opp_fg_pct_10_16"]')
    fg_pct_16_xx = toIntOrFloat(row, '[data-stat="opp_fg_pct_16_xx"]')
    fg3_pct = toIntOrFloat(row, '[data-stat="opp_fg3_pct"]')
    fg2_pct_ast = toIntOrFloat(row, '[data-stat="opp_fg2_pct_ast"]')
    pct_fg2_dunk = toIntOrFloat(row, '[data-stat="opp_pct_fg2_dunk"]')
    fg2_dunk = toIntOrFloat(row, '[data-stat="opp_fg2_dunk"]')
    pct_fg2_layup = toIntOrFloat(row, '[data-stat="opp_pct_fg2_layup"]')
    fg2_layup = toIntOrFloat(row, '[data-stat="opp_fg2_layup"]')
    fg3_pct_ast = toIntOrFloat(row, '[data-stat="opp_fg3_pct_ast"]')
    pct_fg3a_corner = toIntOrFloat(row, '[data-stat="opp_pct_fg3a_corner"]')
    fg3_pct_corner = toIntOrFloat(row, '[data-stat="opp_fg3_pct_corner"]')
    fg3a_heave = toIntOrFloat(row, '[data-stat="opp_fg3a_heave"]')
    fg3_heave = toIntOrFloat(row, '[data-stat="opp_fg3_heave"]')

    return [id, team_id, season, g, mp, fg_pct, avg_dist, fg2a_ct_fga, pct_fga_00_03, pct_fga_03_10, pct_fga_10_16, pct_fga_16_xx,  fg3a_pct_fga, fg2_pct, fg_pct_00_03, fg_pct_03_10, fg_pct_10_16, fg_pct_16_xx, fg3_pct, fg2_pct_ast, pct_fg2_dunk, fg2_dunk, pct_fg2_layup, fg2_layup, fg3_pct_ast, pct_fg3a_corner, fg3_pct_corner, fg3a_heave, fg3_heave]


def toIntOrFloat(row, path):
    value = None
    try:
        value = row.select_one(path).get_text()
        if value != '':
            try:
                value = int(value)
            except ValueError:
                value = float(value)
    except:
        pass

    return value


def writeFile(path, data, idx):
    headers = [
        ['id', 'team_id', 'season', 'g', 'mp', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'fg2',
            'fg2a', 'fg2_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts'],
        ['id', 'team_id', 'season', 'age', 'wins', 'losses', 'wins_pyth', 'losses_pyth', 'mov', 'sos', 'srs', 'off_rtg', 'def_rtg', 'net_rtg', 'pace', 'fta_per_fga_pct',
            'fg3a_per_fga_pct', 'ts_pct', 'efg_pct', 'tov_pct', 'orb_pct', 'ft_rate', 'opp_efg_pct', 'opp_tov_pct', 'drb_pct', 'opp_ft_rate', 'arena_name', 'attendance', 'attendance_per_g'],
        ['id', 'team_id', 'season', 'g', 'mp' 'fg_pct', 'avg_dist', 'fg2a_ct_fga', 'pct_fga_00_03', 'pct_fga_03_10', 'pct_fga_10_16', 'pct_fga_16_xx', 'fg3a_pct_fga', 'fg2_pct', 'fg_pct_00_03', 'fg_pct_03_10',
            'fg_pct_10_16', 'fg_pct_16_xx', 'fg3_pct', 'fg2_pct_ast', 'pct_fg2_dunk', 'fg2_dunk', 'pct_fg2_layup', 'fg2_layup', 'fg3_pct_ast', 'pct_fg3a_corner', 'fg3_pct_corner', 'fg3a_heave', 'fg3_heave']
    ]
    with open(path, 'w') as file:
        writer = csv.writer(file)
        writer.writerow(headers[idx])

        for d in data:
            writer.writerow(d)


def getEndYear(year):
    return str(year)[2:]


def getStartYear(year):
    year -= 1
    return str(year)


if __name__ == "__main__":
    start()
