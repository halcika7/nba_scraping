import csv
from bs4 import BeautifulSoup
import requests


def start():

    i = 26669
    j = 22767
            
    with open('links.csv', 'r') as file:
        reader = csv.reader(file)

        for row in reader:
            html = requests.get(row[1])
            a = html.text.replace('<!--', '')
            b = a.replace('-->', '')
            soup = BeautifulSoup(b, 'html.parser')

            if soup.select_one('#per_minute'):
                per_minute_trs = soup.select('#per_minute tbody > tr')
                for tr in per_minute_trs:
                    if tr.select_one('[data-stat="lg_id"]').get_text() == 'NBA':
                        season = tr.select_one('[data-stat="season"] > a').get_text()
                        total_games = ''
                        try:
                            total_games = tr.select_one('[data-stat="g"]').get_text()
                            if total_games != '':
                                total_games = int(total_games)
                        except:
                            pass

                        games_started= ''
                        try:
                            games_started = tr.select_one('[data-stat="gs"]').get_text()
                            if games_started != '':
                                games_started = int(games_started)
                        except:
                            pass

                        minutes_played = ''
                        try:
                            minutes_played = tr.select_one('[data-stat="mp"]').get_text()
                            if minutes_played != '':
                                minutes_played = float(minutes_played)
                        except:
                            pass

                        fg = ''
                        try:
                            fg = tr.select_one('[data-stat="fg_per_mp"]').get_text()
                            if fg != '':
                                fg = float(fg)
                        except:
                            pass

                        fga = ''                    
                        try:
                            fga = tr.select_one('[data-stat="fga_per_mp"]').get_text()
                            if fga != '':
                                fga = float(fga)
                        except:
                            pass

                        fgp = ''                  
                        try:
                            fgp = tr.select_one('[data-stat="fg_pct"]').get_text()
                            if fgp != '':
                                fgp = float(fgp)
                        except:
                            pass                             

                        fg3 = ''
                        fg3a = ''
                        fg3p = ''
                        fg2 = ''
                        fg2a = ''
                        fg2p = ''

                        try:
                            fg3 = tr.select_one('[data-stat="fg3_per_mp"]').get_text()
                            if fg3 != '':
                                fg3 = float(fg3)
                        except:
                            pass

                        try:
                            fg3a = tr.select_one('[data-stat="fg3a_per_mp"]').get_text()
                            if fg3a != '':
                                fg3a = float(fg3a)
                        except:
                            pass

                        try:
                            fg3p = tr.select_one('[data-stat="fg3_pct"]').get_text()
                            if fg3p != '':
                                fg3p = float(fg3p)
                        except:
                            pass

                        try:
                            fg2 = tr.select_one('[data-stat="fg2_per_mp"]').get_text()
                            if fg2 != '':
                                fg2 = float(fg2)
                        except:
                            pass

                        try:
                            fg2a = tr.select_one('[data-stat="fg2a_per_mp"]').get_text()
                            if fg2a != '':
                                fg2a = float(fg2a)
                        except:
                            pass

                        try:
                            fg2p = tr.select_one('[data-stat="fg2_pct"]').get_text()
                            if fg2p != '':
                                fg2p = float(fg2p)
                        except:
                            pass

                        ft = ''
                        try:
                            ft = tr.select_one('[data-stat="ft_per_mp"]').get_text()
                            if ft != '':
                                ft = float(ft)
                        except:
                            pass

                        fta = ''
                        try:
                            fta = tr.select_one('[data-stat="fta_per_mp"]').get_text()
                            if fta != '':
                                fta = float(fta)
                        except:
                            pass

                        ftp = ''
                        try:
                            ftp = tr.select_one('[data-stat="ft_pct"]').get_text()
                            if ftp != '':
                                ftp = float(ftp)
                        except:
                            pass

                        orb = ''
                        try:
                            orb = tr.select_one('[data-stat="orb_per_mp"]').get_text()
                            if orb != '':
                                orb = float(orb)
                        except:
                            pass

                        drb = ''
                        try:
                            drb = tr.select_one('[data-stat="drb_per_mp"]').get_text()
                            if drb != '':
                                drb = float(drb)
                        except:
                            pass

                        trb = ''
                        try:
                            trb = tr.select_one('[data-stat="trb_per_mp"]').get_text()
                            if trb != '':
                                trb = float(trb)
                        except:
                            pass

                        ast = ''
                        try:
                            ast = tr.select_one('[data-stat="ast_per_mp"]').get_text()
                            if ast != '':
                                ast = float(ast)
                        except:
                            pass

                        stl = ''
                        try:
                            stl = tr.select_one('[data-stat="stl_per_mp"]').get_text()
                            if stl != '':
                                stl = float(stl)
                        except:
                            pass

                        blk = ''
                        try:
                            blk = tr.select_one('[data-stat="blk_per_mp"]').get_text()
                            if blk != '':
                                blk = float(blk)
                        except:
                            pass

                        tov = ''
                        try:
                            tov = tr.select_one('[data-stat="tov_per_mp"]').get_text()
                            if tov != '':
                                tov = float(tov)
                        except:
                            pass

                        pf = ''
                        try:
                            pf = tr.select_one('[data-stat="pf_per_mp"]').get_text()
                            if pf != '':
                                pf = float(pf)
                        except:
                            pass

                        pts = ''
                        try:
                            pts = tr.select_one('[data-stat="pts_per_mp"]').get_text()
                            if pts != '':
                                pts = float(pts)
                        except:
                            pass
                        
                        with open('player_data_per_36_min.csv', 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow([i,row[0],season, total_games, games_started, minutes_played, fg, fga, fgp, fg3,fg3a,fg3p,fg2,fg2a,fg2p,ft,fta,ftp,orb,drb,trb,ast,stl,blk,tov,pf,pts])
                        
                        i += 1

            if soup.select_one('#per_poss'):
                per_poss_trs = soup.select('#per_poss  tbody > tr')
                for tr in per_poss_trs:
                    if tr.select_one('[data-stat="lg_id"]').get_text() == 'NBA':
                        season = tr.select_one('[data-stat="season"] > a').get_text()
                        total_games = ''
                        try:
                            total_games = tr.select_one('[data-stat="g"]').get_text()
                            if total_games != '':
                                total_games = int(total_games)
                        except:
                            pass

                        games_started= ''
                        try:
                            games_started = tr.select_one('[data-stat="gs"]').get_text()
                            if games_started != '':
                                games_started = int(games_started)
                        except:
                            pass

                        minutes_played = ''
                        try:
                            minutes_played = tr.select_one('[data-stat="mp"]').get_text()
                            if minutes_played != '':
                                minutes_played = float(minutes_played)
                        except:
                            pass

                        fg = ''
                        try:
                            fg = tr.select_one('[data-stat="fg_per_poss"]').get_text()
                            if fg != '':
                                fg = float(fg)
                        except:
                            pass

                        fga = ''                    
                        try:
                            fga = tr.select_one('[data-stat="fga_per_poss"]').get_text()
                            if fga != '':
                                fga = float(fga)
                        except:
                            pass

                        fgp = ''                  
                        try:
                            fgp = tr.select_one('[data-stat="fg_pct"]').get_text()
                            if fgp != '':
                                fgp = float(fgp)
                        except:
                            pass                             

                        fg3 = ''
                        fg3a = ''
                        fg3p = ''
                        fg2 = ''
                        fg2a = ''
                        fg2p = ''

                        try:
                            fg3 = tr.select_one('[data-stat="fg3_per_poss"]').get_text()
                            if fg3 != '':
                                fg3 = float(fg3)
                        except:
                            pass

                        try:
                            fg3a = tr.select_one('[data-stat="fg3a_per_poss"]').get_text()
                            if fg3a != '':
                                fg3a = float(fg3a)
                        except:
                            pass

                        try:
                            fg3p = tr.select_one('[data-stat="fg3_pct"]').get_text()
                            if fg3p != '':
                                fg3p = float(fg3p)
                        except:
                            pass

                        try:
                            fg2 = tr.select_one('[data-stat="fg2_per_poss"]').get_text()
                            if fg2 != '':
                                fg2 = float(fg2)
                        except:
                            pass

                        try:
                            fg2a = tr.select_one('[data-stat="fg2a_per_poss"]').get_text()
                            if fg2a != '':
                                fg2a = float(fg2a)
                        except:
                            pass

                        try:
                            fg2p = tr.select_one('[data-stat="fg2_pct"]').get_text()
                            if fg2p != '':
                                fg2p = float(fg2p)
                        except:
                            pass

                        ft = ''
                        try:
                            ft = tr.select_one('[data-stat="ft_per_poss"]').get_text()
                            if ft != '':
                                ft = float(ft)
                        except:
                            pass

                        fta = ''
                        try:
                            fta = tr.select_one('[data-stat="fta_per_poss"]').get_text()
                            if fta != '':
                                fta = float(fta)
                        except:
                            pass

                        ftp = ''
                        try:
                            ftp = tr.select_one('[data-stat="ft_pct"]').get_text()
                            if ftp != '':
                                ftp = float(ftp)
                        except:
                            pass

                        orb = ''
                        try:
                            orb = tr.select_one('[data-stat="orb_per_poss"]').get_text()
                            if orb != '':
                                orb = float(orb)
                        except:
                            pass

                        drb = ''
                        try:
                            drb = tr.select_one('[data-stat="drb_per_poss"]').get_text()
                            if drb != '':
                                drb = float(drb)
                        except:
                            pass

                        trb = ''
                        try:
                            trb = tr.select_one('[data-stat="trb_per_poss"]').get_text()
                            if trb != '':
                                trb = float(trb)
                        except:
                            pass

                        ast = ''
                        try:
                            ast = tr.select_one('[data-stat="ast_per_poss"]').get_text()
                            if ast != '':
                                ast = float(ast)
                        except:
                            pass

                        stl = ''
                        try:
                            stl = tr.select_one('[data-stat="stl_per_poss"]').get_text()
                            if stl != '':
                                stl = float(stl)
                        except:
                            pass

                        blk = ''
                        try:
                            blk = tr.select_one('[data-stat="blk_per_poss"]').get_text()
                            if blk != '':
                                blk = float(blk)
                        except:
                            pass

                        tov = ''
                        try:
                            tov = tr.select_one('[data-stat="tov_per_poss"]').get_text()
                            if tov != '':
                                tov = float(tov)
                        except:
                            pass

                        pf = ''
                        try:
                            pf = tr.select_one('[data-stat="pf_per_poss"]').get_text()
                            if pf != '':
                                pf = float(pf)
                        except:
                            pass

                        pts = ''
                        try:
                            pts = tr.select_one('[data-stat="pts_per_poss"]').get_text()
                            if pts != '':
                                pts = float(pts)
                        except:
                            pass

                        ortg = ''
                        try:
                            ortg = tr.select_one('[data-stat="off_rtg"]').get_text()
                            if ortg != '':
                                ortg = float(ortg)
                        except:
                            pass
                        drtg = ''
                        try:
                            drtg = tr.select_one('[data-stat="def_rtg"]').get_text()
                            if drtg != '':
                                drtg = float(drtg)
                        except:
                            pass
                        
                        with open('player_data_per_100_poss.csv', 'a') as file:
                            writer = csv.writer(file)
                            writer.writerow([j,row[0],season, total_games, games_started, minutes_played, fg, fga, fgp, fg3,fg3a,fg3p,fg2,fg2a,fg2p,ft,fta,ftp,orb,drb,trb,ast,stl,blk,tov,pf,pts,ortg,drtg])
                        
                        j += 1


if __name__ == "__main__":
    start()
