import requests
import pandas as pd

class VivinoAPI:

    def __init__(self, wineList):
        self.wineList = wineList

        for i in range(1, 100):
            try:
                r = requests.get("https://www.vivino.com/api/explore/explore",
                    params = {
                        "currency_code":"CAD",
                        "min_rating":"3",
                        "order_by":"price",
                        "order":"asc",
                        "page": 1,
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

            execpt:
                # BREAK
        df = pd.DataFrame(results,columns=['Winery','Wine','Rating','num_review'])
        writer = pd.ExcelWriter('vivino_wine_list.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()
