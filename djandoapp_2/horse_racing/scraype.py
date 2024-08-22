# horse_scraper/scrape.py

import requests
from bs4 import BeautifulSoup
import time
import django
from django.utils.dateparse import parse_date

def scrape():
    print("scrape")
    #Django設定の読み込み
    django.setup()

    from .models import RaceResult

    # 取得開始年
    year_start = 2019
    # 取得終了年
    year_end = 2020

    for year in range(year_start, year_end):
        # 競馬場
        l = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10"]
        for w in range(len(l)):
            place = ["札幌", "函館", "福島", "新潟", "東京", "中山", "中京", "京都", "阪神", "小倉"][int(l[w])-1]

            # 開催回数分ループ（6回）
            for z in range(7):
                continueCounter = 0
                # 開催日数分ループ（12日）
                for y in range(13):
                    race_id = f"{year}{l[w]}{'0' if y < 9 else ''}{z+1}{'0' if y < 9 else ''}{y+1}"
                    url1 = f"https://db.netkeiba.com/race/{race_id}"

                    # レース数分ループ（12R）
                    for x in range(12):
                        url = f"{url1}{'0' if x < 9 else ''}{x+1}"
                        current_race_id = f"{race_id}{'0' if x < 9 else ''}{x+1}"

                        try:
                            r = requests.get(url)
                        except requests.exceptions.RequestException as e:
                            print(f"Error: {e}")
                            print("Retrying in 10 seconds...")
                            time.sleep(10)
                            r = requests.get(url)

                        soup = BeautifulSoup(r.content.decode("euc-jp", "ignore"), "html.parser")
                        soup_span = soup.find_all("span")
                        allnum = (len(soup_span) - 6) // 3

                        if allnum < 1:
                            continue

                        for num in range(allnum):
                            soup_txt_l = soup.find_all(class_="txt_l")
                            soup_txt_r = soup.find_all(class_="txt_r")
                            soup_nowrap = soup.find_all("td", nowrap="nowrap", class_=None)
                            soup_tet_c = soup.find_all("td", nowrap="nowrap", class_="txt_c")
                            soup_smalltxt = soup.find_all("p", class_="smalltxt")

                            try:
                                runtime = soup_txt_r[2 + 5 * num].contents[0]
                            except IndexError:
                                runtime = ''
                            try:
                                pas = str(soup_nowrap[3 * num].contents[0])
                            except:
                                pas = ''
                            try:
                                var = soup_nowrap[3 * num + 1].contents[0]
                                weight = int(var.split("(")[0])
                                weight_dif = int(var.split("(")[1][:-1])
                            except ValueError:
                                weight = 0
                                weight_dif = 0

                            try:
                                last = soup_tet_c[6 * num + 3].contents[0].contents[0]
                            except IndexError:
                                last = ''
                            try:
                                pop = soup_span[3 * num + 10].contents[0]
                            except IndexError:
                                pop = ''

                            try:
                                var = soup_span[8]
                                sur = str(var).split("/")[0].split(">")[1][0]
                                rou = str(var).split("/")[0].split(">")[1][1]
                                dis = str(var).split("/")[0].split(">")[1].split("m")[0][-4:]
                                con = str(var).split("/")[2].split(":")[1][1]
                                wed = str(var).split("/")[1].split(":")[1][1]
                            except IndexError:
                                try:
                                    var = soup_span[7]
                                    sur = str(var).split("/")[0].split(">")[1][0]
                                    rou = str(var).split("/")[0].split(">")[1][1]
                                    dis = str(var).split("/")[0].split(">")[1].split("m")[0][-4:]
                                    con = str(var).split("/")[2].split(":")[1][1]
                                    wed = str(var).split("/")[1].split(":")[1][1]
                                except IndexError:
                                    var = soup_span[6]
                                    sur = str(var).split("/")[0].split(">")[1][0]
                                    rou = str(var).split("/")[0].split(">")[1][1]
                                    dis = str(var).split("/")[0].split(">")[1].split("m")[0][-4:]
                                    con = str(var).split("/")[2].split(":")[1][1]
                                    wed = str(var).split("/")[1].split(":")[1][1]

                            detail = str(soup_smalltxt).split(">")[1].split(" ")[1]
                            date = str(soup_smalltxt).split(">")[1].split(" ")[0]
                            clas = str(soup_smalltxt).split(">")[1].split(" ")[2].replace(u'\xa0', u' ').split(" ")[0]
                            title = str(soup.find_all("h1")[1]).split(">")[1].split("<")[0]

                            RaceResult.objects.create(
                                race_id=current_race_id,
                                horse_name=soup_txt_l[4 * num].contents[1].contents[0],
                                jockey_name=soup_txt_l[4 * num + 1].contents[1].contents[0],
                                horse_number=int(soup_txt_r[1 + 5 * num].contents[0]),
                                runtime=runtime,
                                odds=soup_txt_r[3 + 5 * num].contents[0],
                                passing_order=pas,
                                position=num + 1,
                                weight=weight,
                                weight_change=weight_dif,
                                sex=soup_tet_c[6 * num].contents[0][0],
                                age=int(soup_tet_c[6 * num].contents[0][1]),
                                weight_carry=float(soup_tet_c[6 * num + 1].contents[0]),
                                last_3f=last,
                                popularity=pop,
                                race_name=title,
                                race_date=parse_date(date),
                                track=detail,
                                race_class=clas,
                                surface=sur,
                                distance=int(dis),
                                turn=rou,
                                track_condition=con,
                                weather=wed,
                                track_id=w,
                                track_name=place
                            )

                        print(f"{detail}{x + 1}R")

                    if allnum < 1:
                        break

        print("終了")

