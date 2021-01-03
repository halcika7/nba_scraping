import csv
from bs4 import BeautifulSoup
from bs4.element import Tag
import requests
from searchTeam import searchTeamByShortName


def start():
    id = 1
    coaches = []
    coaches_stats_by_season = []

    with open('coachesLinks.csv', 'r')as f:
        data = csv.reader(f)
        for i, row in enumerate(data):
            if i > 0:
                html_source = requests.get(row[2])
                soup = BeautifulSoup(html_source.content, 'html.parser')
                ps = soup.select('#meta div p')
                name = soup.select_one(
                    '#meta div [itemprop="name"]').get_text()
                birth = None
                died = None
                if soup.select_one('#necro-birth'):
                    birth = soup.select_one('#necro-birth').get_text()
                if soup.select_one('#necro-death'):
                    died = soup.select_one('#necro-death').get_text()

                high_school = ''
                college = ''
                currently_coaching = None
                all_teams_coached = []
                for p in ps:
                    txt = " ".join(p.get_text().split())
                    if 'High School: ' in txt:
                        high_school = txt.split('High School: ')[1]
                    elif 'College: ' in txt:
                        college = txt.split('College: ')[1]

                coached_teams = soup.select('#coach-stats > tfoot > tr')

                if row[-1] == False:
                    last_team = soup.select('#coach-stats > tbody > tr')[-1]
                    currently_coaching_team = last_team.select_one(
                        '[data-stat="team_id"] > a').get_text()
                    currently_coaching = int(
                        searchTeamByShortName(currently_coaching_team)[0])

                for team in coached_teams:
                    if not team.get('class') and team.select_one('[data-stat="season"]') and team.select_one('[data-stat="lg_id"]') and team.select_one('[data-stat="lg_id"]').get_text() == "NBA":
                        team_short_name = ''
                        try:
                            team_short_name = team.select_one(
                                '[data-stat="team_id"]').get_text()
                            if team_short_name in ['BRK','NJN,BRK', 'NYN,NJN']:
                                team_short_name = 'NJN'

                            elif team_short_name in ['SFW,GSW', 'PHW', 'SFW']:
                                team_short_name = 'GSW'

                            elif team_short_name in ['TRI', 'STL', 'STL,ATL', 'MLH,STL', 'MLH']:
                                team_short_name = 'ATL'

                            elif team_short_name == 'NOJ':
                                team_short_name = 'UTA'

                            elif team_short_name in ['BLB', 'WSB,WAS', 'BAL', 'CAP,WSB', 'CHZ,BAL', 'WSB', 'CHZ', 'CHP', 'BAL,WSB']:
                                team_short_name = 'WAS'

                            elif team_short_name in ['SEA', 'SEA,OKC']:
                                team_short_name = 'OKC'

                            elif team_short_name in ['FTW', 'FTW,DET']:
                                team_short_name = 'DET'

                            elif team_short_name in ['CHO', 'CHH', 'CHA,CHO', 'CHH,CHA']:
                                team_short_name = 'CHA'

                            elif team_short_name == 'MNL':
                                team_short_name = 'LAL'
                            
                            elif team_short_name in ['SYR', 'SYR,PHI']:
                                team_short_name = 'PHI'
                            
                            elif team_short_name in ['CIN,KCO', 'KCK', 'ROC', 'KCO,KCK,SAC','CIN','ROC,CIN', 'KCO']:
                                team_short_name = 'SAC'

                            elif team_short_name == 'DNN':
                                team_short_name = 'DEN'
                            
                            elif team_short_name in ['BUF', 'SDC,LAC', 'SDC']:
                                team_short_name = 'LAC'

                            elif team_short_name in ['NOP', 'NOK,NOH', 'NOH,NOP']:
                                team_short_name = 'NOH'
                            
                            elif team_short_name == 'SDR':
                                team_short_name = 'HOU'

                            elif team_short_name in ['VAN', 'VAN,MEM']:
                                team_short_name = 'MEM'

                            team_id = int(
                                searchTeamByShortName(team_short_name)[0])
                            all_teams_coached.append(team_id)
                        except:
                            print(team_short_name)
                            print(row[2])
                            print(row[0])
                            print('#####################')
                            # break

                coaches.append([row[0], name, birth, died, high_school, college, row[3],
                                row[4], row[5], row[6], currently_coaching, all_teams_coached, row[1]])

                trs = soup.select('#coach-stats > tbody > tr')

                for tr in trs:
                    if not tr.get('class') and tr.select_one('[data-stat="lg_id"] > a').get_text() == "NBA" and tr.select_one('[data-stat="g"]'):
                        season = tr.select_one(
                            '[data-stat="season"]').get_text()
                        rg = tr.select_one('[data-stat="g"]').get_text()
                        if rg != '':
                            rg = int(tr.select_one('[data-stat="g"]').get_text())

                        rgw = tr.select_one(
                            '[data-stat="wins"]').get_text()
                        if rgw != '':
                            rgw = int(tr.select_one(
                            '[data-stat="wins"]').get_text())

                        rgl = tr.select_one(
                            '[data-stat="losses"]').get_text()
                        if rgl != '':
                            rgl = int(tr.select_one(
                            '[data-stat="losses"]').get_text())

                        rgpercent = tr.select_one(
                            '[data-stat="win_loss_pct"]').get_text()
                        if rgpercent != '':
                            rgpercent = float(tr.select_one(
                            '[data-stat="win_loss_pct"]').get_text())

                        pg = tr.select_one(
                            '[data-stat="g_playoffs"]').get_text()
                        if pg != '':
                            pg = int(tr.select_one(
                            '[data-stat="g_playoffs"]').get_text())

                        pgw = tr.select_one(
                            '[data-stat="wins_playoffs"]').get_text()
                        if pgw != '':
                            pgw = int(tr.select_one(
                            '[data-stat="wins_playoffs"]').get_text())

                        pgl = tr.select_one(
                            '[data-stat="losses_playoffs"]').get_text()
                        if pgl != '':
                            pgl = int(tr.select_one(
                            '[data-stat="losses_playoffs"]').get_text())

                        pgpercent = tr.select_one(
                            '[data-stat="win_loss_pct_playoffs"]').get_text()
                        if pgpercent != '':
                            pgpercent = float(tr.select_one(
                            '[data-stat="win_loss_pct_playoffs"]').get_text())
                        coaches_stats_by_season.append(
                            [id, row[0], season, rg, rgw, rgl, rgpercent, pg, pgw, pgl, pgpercent])
                        id += 1

    with open('coaches.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "name", "birth", "died",
                         "high_school", "college", "started_coaching", "last_coach_season", "years_coaching", "retired", "currently_coaching", "all_teams_coached", "link"])
        for coach in coaches:
            writer.writerow(coach)

    with open('coaches_stats_season.csv', 'w') as file:
        writer = csv.writer(file)
        writer.writerow(["id", "coach_id", "season", "regular_season_games",
                         "regular_season_wins", "regular_season_losses", 'regular_season_win_loss_pct', "playoff_games", "playoff_wins", "playoff_losses", "playoff_win_loss_pct"])
        for stat in coaches_stats_by_season:
            writer.writerow(stat)


if __name__ == "__main__":
    start()
