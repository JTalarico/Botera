import requests
import pandas as pd

class VivinoAPI:

    def __init__(self, wineList):
        self.wineList = wineList
        self.vivino_wine_list = []
        for i in range(1, 4):
            r = requests.get("https://www.vivino.com/api/explore/explore",
                params = {
                    "currency_code":"CAD",
                    "min_rating":"3",
                    "page": i,
                },
                headers= {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
                }
            )
            results = [
                (
#                       t["vintage"]["wine"]["winery"]["name"], 
                    t["vintage"]["wine"]["name"],
                    t["vintage"]["year"],
                    t["vintage"]["statistics"]["ratings_average"],
                    t["vintage"]["statistics"]["ratings_count"]
                )
                for t in r.json()["explore_vintage"]["matches"]
            ]
            self.vivino_wine_list.append(results)
            print(self.vivino_wine_list)
            print(len(results))
            print(i)
        df = pd.DataFrame(self.vivino_wine_list,columns=['Wine','Year','Rating','num_review'])
        writer = pd.ExcelWriter('vivino_wine_list.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()

'''
        for i in range(1, 2):
            try:
                r = requests.get("https://www.vivino.com/api/explore/explore",
                    params = {
                        "currency_code":"CAD",
                        "min_rating":"3",
                        "order_by":"price",
                        "order":"asc",
                        "page": ,
                        "price_range_max":"200",
                        "price_range_min":"0"
                    },
                    headers= {
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0"
                    }
                )
                results = [
                    (
                        t["vintage"]["wine"]["winery"]["name"], 
                        f'{t["vintage"]["wine"]["name"]} {t["vintage"]["year"]}',
                        t["vintage"]["statistics"]["ratings_average"],
                        t["vintage"]["statistics"]["ratings_count"]
                    )
                    for t in r.json()["explore_vintage"]["matches"]
                ]
                self.vivino_wine_list.append(results)
            except:
                break
'''
