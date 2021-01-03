import csv
from bs4 import BeautifulSoup
from searchPlayer import searchPlayerByURL, loadPlayers
import requests

def start():
    all_star_game_data = []
    all_star_player_data = []
    id = 1

    loadPlayers()

    with open('./csvs/all-star/allstar_links.csv', 'r') as file:
        rows = csv.reader(file)
        for row in rows:
            if row[-1] != 'allstar_link':
                html_source = requests.get(row[-1])
                soup = BeautifulSoup(html_source.content, 'html.parser')

                [a, b] = soup.select('#line_score tr')[2:]
                a_tds = a.select('td')
                b_tds = b.select('td')
                team_1_name = a_tds[0].get_text()
                team_1_score = int(a_tds[-1].get_text())
                team_2_name = b_tds[0].get_text()
                team_2_score = int(b_tds[-1].get_text())

                a_tds = a_tds[1:-1]
                b_tds = b_tds[1:-1]

                if len(team_1_name.split(' ')) == 2:
                    team_1_name = team_1_name.split(' ')[1]

                if len(team_2_name.split(' ')) == 2:
                    team_2_name = team_2_name.split(' ')[1]

                team_a_by_q = []
                team_b_by_q = []

                for x in a_tds:
                    team_a_by_q.append(int(x.get_text()))

                for x in b_tds:
                    team_b_by_q.append(int(x.get_text()))

                all_star_game_data.append(
                    [row[0], row[1], row[2], team_1_name, team_1_score, team_2_name, team_2_score, team_a_by_q, team_b_by_q])

                players_1_trs = soup.select(
                    '#' + team_1_name + ' > tbody > tr')
                players_2_trs = soup.select(
                    '#' + team_2_name + ' > tbody > tr')
                reserve = False

                for p in players_1_trs:
                    if p.get('class') == ['thead']:
                        reserve = True
                    if not p.get('class'):
                        values = extract_values(p, id, row[0], reserve)
                        id += 1
                        all_star_player_data.append(values)
                
                reserve = False

                for p in players_2_trs:
                    if p.get('class') == ['thead']:
                        reserve = True
                    if not p.get('class'):
                        values = extract_values(p, id, row[0], reserve)
                        id += 1
                        all_star_player_data.append(values)

    with open('all_star_game_data.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "season", "location", 'team_1_name', 'team_1_score', 'team_2_name', 'team_2_score', 'team_a_by_q', 'team_b_by_q'])
        for r in all_star_game_data:
            writer.writerow(r)

    with open('all_star_player_data.csv', 'w') as file:
        writer = csv.writer(file)
        header = "id, game_id, player_id, minutes, fg, fga, fg_pct, fg3, fg3a, fg3_pct, ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, tov, pf, pts, reserve".split(',')
        writer.writerow(header)
        for r in all_star_player_data:
            writer.writerow(r)


def extract_values(p, i, game_id, reserve):
    url = p.select_one('[data-stat="player"] > a').get('href')
    player_id = int(searchPlayerByURL(url)[0])
    minutes = min_to_sec(p.select_one('[data-stat="mp"]').get_text())
    fg = to_int(p.select_one('[data-stat="fg"]').get_text())
    fga = to_int(p.select_one('[data-stat="fga"]').get_text())
    fg_pct = to_float(p.select_one('[data-stat="fg_pct"]').get_text())

    fg3 = to_int(p.select_one('[data-stat="fg3"]').get_text())
    fg3a = to_int(p.select_one('[data-stat="fg3a"]').get_text())
    fg3_pct = to_float(p.select_one('[data-stat="fg3_pct"]').get_text())

    ft = to_int(p.select_one('[data-stat="ft"]').get_text())
    fta = to_int(p.select_one('[data-stat="fta"]').get_text())
    ft_pct = to_float(p.select_one('[data-stat="ft_pct"]').get_text())

    orb = to_int(p.select_one('[data-stat="orb"]').get_text())
    drb = to_int(p.select_one('[data-stat="drb"]').get_text())
    trb = to_int(p.select_one('[data-stat="trb"]').get_text())
    ast = to_int(p.select_one('[data-stat="ast"]').get_text())
    stl = to_int(p.select_one('[data-stat="stl"]').get_text())
    blk = to_int(p.select_one('[data-stat="blk"]').get_text())
    tov = to_int(p.select_one('[data-stat="tov"]').get_text())
    pf = to_int(p.select_one('[data-stat="pf"]').get_text())
    pts = to_int(p.select_one('[data-stat="pts"]').get_text())

    return [i, game_id, player_id, minutes, fg, fga, fg_pct, fg3, fg3a, fg3_pct, ft, fta, ft_pct, orb, drb, trb, ast, stl, blk, tov, pf, pts, reserve]


def min_to_sec(value):
    if value != '':
        [minutes, seconds] = value.split(':')
        return (int(minutes) * 60) + int(seconds)

    return ''


def to_int(value):
    if value != '':
        return int(value)
    return value


def to_float(value):
    if value != '':
        return float(value)
    return value


if __name__ == "__main__":
    start()
