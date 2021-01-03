import csv
from bs4 import BeautifulSoup
import requests
from sys import argv

def start():

    # with open('team_game_data.csv', 'w') as file:
    #     writer = csv.writer(file)
    #     writer.writerow(['id', 'game_id', 'team_id', 'minutes_played', 'fg', 'fga', 'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb', 'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'plus_minus', 'pts'])

    game_data = []

    id = 1

    with open('./csvs/other/boxScoreLinks.csv', 'r') as file:
        rows = csv.reader(file)
        for i,row in enumerate(rows):
            if i > 0:
                if int(row[0]) >= int(argv[1]) and int(row[0]) < int(argv[2]):
                    html_source = requests.get(row[1])
                    soup = BeautifulSoup(html_source.content, 'html.parser')

                    if soup.select('table[id*="game-basic"]'):

                        [away_mp, home_mp] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="mp"]')
                        away_mp = int(away_mp.get_text())
                        home_mp = int(home_mp.get_text())

                        [away_fg, home_fg] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fg"]')
                        away_fg = away_fg.get_text()
                        home_fg = home_fg.get_text()
                        if away_fg != '':
                            away_fg = int(away_fg)
                        if home_fg != '':
                            home_fg = int(home_fg)

                        [away_fga, home_fga] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fga"]')
                        away_fga = away_fga.get_text()
                        home_fga = home_fga.get_text()
                        if away_fga != '':
                            away_fga = int(away_fga)
                        if home_fga != '':
                            home_fga = int(home_fga)
                        
                        [away_fg_pct, home_fg_pct] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fg_pct"]')
                        away_fg_pct = away_fg_pct.get_text()
                        home_fg_pct = home_fg_pct.get_text()
                        if away_fg_pct != '':
                            away_fg_pct = float(away_fg_pct)
                        if home_fg_pct != '':
                            home_fg_pct = float(home_fg_pct)

                        away_fg3 = None
                        home_fg3 = None
                        if soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fg3"]'):
                            [away_fg3, home_fg3] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fg3"]')
                            away_fg3 = away_fg3.get_text()
                            home_fg3 = home_fg3.get_text()
                            if away_fg3 != '':
                                away_fg3 = int(away_fg3)
                            if home_fg3 != '':
                                home_fg3 = int(home_fg3)
                        
                        away_fg3a = None
                        home_fg3a = None
                        if soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fg3a"]'):
                            [away_fg3a, home_fg3a] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fg3a"]')
                            away_fg3a = away_fg3a.get_text()
                            home_fg3a = home_fg3a.get_text()
                            if away_fg3a != '':
                                away_fg3a = int(away_fg3a)
                            if home_fg3a != '':
                                home_fg3a = int(home_fg3a)

                        away_fg3_pct = None
                        home_fg3_pct = None
                        if soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fg3_pct"]'):
                            [away_fg3_pct, home_fg3_pct] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fg3_pct"]')
                            away_fg3_pct = away_fg3_pct.get_text()
                            home_fg3_pct = home_fg3_pct.get_text()
                            if away_fg3_pct != '':
                                away_fg3_pct = float(away_fg3_pct)
                            if home_fg3_pct != '':
                                home_fg3_pct = float(home_fg3_pct)

                        [away_ft, home_ft] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="ft"]')
                        away_ft = away_ft.get_text()
                        home_ft = home_ft.get_text()
                        if away_ft != '':
                            away_ft = int(away_ft)
                        if home_ft != '':
                            home_ft = int(home_ft)

                        [away_fta, home_fta] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="fta"]')
                        away_fta = away_fta.get_text()
                        home_fta = home_fta.get_text()
                        if away_fta != '':
                            away_fta = int(away_fta)
                        if home_fta != '':
                            home_fta = int(home_fta)

                        [away_ft_pct, home_ft_pct] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="ft_pct"]')
                        away_ft_pct = away_ft_pct.get_text()
                        home_ft_pct = home_ft_pct.get_text()
                        if away_ft_pct != '':
                            away_ft_pct = float(away_ft_pct)
                        if home_ft_pct != '':
                            home_ft_pct = float(home_ft_pct)

                        [away_orb, home_orb] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="orb"]')
                        away_orb = away_orb.get_text()
                        home_orb = home_orb.get_text()
                        if away_orb != '':
                            away_orb = int(away_orb)
                        if home_orb != '':
                            home_orb = int(home_orb)

                        [away_drb, home_drb] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="drb"]')
                        away_drb = away_drb.get_text()
                        home_drb = home_drb.get_text()
                        if away_drb != '':
                            away_drb = int(away_drb)
                        if home_drb != '':
                            home_drb = int(home_drb)

                        [away_trb, home_trb] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="trb"]')
                        away_trb = away_trb.get_text()
                        home_trb = home_trb.get_text()
                        if away_trb != '':
                            away_trb = int(away_trb)
                        if home_trb != '':
                            home_trb = int(home_trb)

                        [away_ast, home_ast] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="ast"]')
                        away_ast = away_ast.get_text()
                        home_ast = home_ast.get_text()
                        if away_ast != '':
                            away_ast = int(away_ast)
                        if home_ast != '':
                            home_ast = int(home_ast)

                        [away_stl, home_stl] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="stl"]')
                        away_stl = away_stl.get_text()
                        home_stl = home_stl.get_text()
                        if away_stl != '':
                            away_stl = int(away_stl)
                        if home_stl != '':
                            home_stl = int(home_stl)

                        [away_blk, home_blk] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="blk"]')
                        away_blk = away_blk.get_text()
                        home_blk = home_blk.get_text()
                        if away_blk != '':
                            away_blk = int(away_blk)
                        if home_blk != '':
                            home_blk = int(home_blk)

                        [away_tov, home_tov] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="tov"]')
                        away_tov = away_tov.get_text()
                        home_tov = home_tov.get_text()
                        if away_tov != '':
                            away_tov = int(away_tov)
                        if home_tov != '':
                            home_tov = int(home_tov)

                        [away_pf, home_pf] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="pf"]')
                        away_pf = away_pf.get_text()
                        home_pf = home_pf.get_text()
                        if away_pf != '':
                            away_pf = int(away_pf)
                        if home_pf != '':
                            home_pf = int(home_pf)

                        away_plus_minus = None
                        home_plus_minus = None
                        if soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="plus_minus"]'):
                            [away_plus_minus, home_plus_minus] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="plus_minus"]')
                            away_plus_minus = away_plus_minus.get_text()
                            home_plus_minus = home_plus_minus.get_text()
                            if away_plus_minus != '':
                                away_plus_minus = int(away_plus_minus)
                            if home_plus_minus != '':
                                home_plus_minus = int(home_plus_minus)

                        [away_pts, home_pts] = soup.select('table[id*="game-basic"] > tfoot > tr [data-stat="pts"]')
                        away_pts = away_pts.get_text()
                        home_pts = home_pts.get_text()
                        if away_pts != '':
                            away_pts = int(away_pts)
                        if home_pts != '':
                            home_pts = int(home_pts)
                        
                        with open('team_game_data.csv', 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow([id, row[0], row[2], away_mp, away_fg, away_fga, away_fg_pct, away_fg3, away_fg3a, away_fg3_pct, away_ft, away_fta, away_ft_pct, away_orb, away_drb, away_trb, away_ast, away_stl, away_blk, away_tov, away_pf, away_plus_minus, away_pts])

                        id += 1

                        with open('team_game_data.csv', 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow([id, row[0], row[3], home_mp, home_fg, home_fga, home_fg_pct, home_fg3, home_fg3a, home_fg3_pct, home_ft, home_fta, home_ft_pct, home_orb, home_drb, home_trb, home_ast, home_stl, home_blk, home_tov, home_pf, home_plus_minus, home_pts])

                        id += 1

            if i > int(argv[2]):
                break


if __name__ == "__main__":
    start()