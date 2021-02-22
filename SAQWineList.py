import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import json
import re
import pandas as pd
import xlsxwriter

"""
Class to retrieve and store all entries from SAQ wine selection.
Done using webscraper.
"""

class SAQWineList:

    def __init__(self):
        pageSize = 10
        self.url = 'https://www.saq.com/en/products/wine?product_list_limit=' + str(pageSize)
        self.wineList = []

    def getList(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        raw_wine_data = soup.findAll('div', attrs={'class': 'product-item-info'})

        for i in range(len(raw_wine_data)):
            name = raw_wine_data[i].find('a', attrs={'class': 'product-item-link'}).get_text().strip()

            try:
               year = re.findall('\W{2,}(\d{4})', name)[0]
            except:
                year = ''

            if(year):
                name = re.findall('(.*?)\W{2,}\d{4}', name)[0]

            description = raw_wine_data[i].find('strong', attrs={'class': 'product product-item-identity-format'}).get_text().strip()
            color = re.findall('^(.*?)\W{2,}', description)[0]
            region = re.findall('\W{2,}([A-Z]\w+.*)', description)[0]
            size_tuple = re.findall('(\d+)\W{2,}([mlL]+)', description)[0]
            price = raw_wine_data[i].find('span', attrs={'data-price-type': 'finalPrice'}).get_text().strip()
            img_url = raw_wine_data[i].find('img', attrs={'class': 'product-image-photo'})['data-src']
            try:
                img_url = re.findall('(.*)\?', img_url)[0]
            except:
                img_url = ''

            if(size_tuple[1] == 'L'):
                price_per_ml = float(price[1:]) / (int(size_tuple[0]) * 1000)
            else:
                price_per_ml = float(price[1:]) / int(size_tuple[0])

            self.wineList.append({                                            
                                    "name" : name,
                                    "year" : year,
                                    "price" : price,
                                    "size" : ' '.join(size_tuple),
                                    "region" : region,
                                    "type" : color,
                                    "price_per_ml" : price_per_ml,
                                    "img_url" : img_url
                                })

    def printList(self):
        print(self.wineList)

    def writeToExcel(self):
        if not self.wineList:
            self.getList()

        df = pd.DataFrame(self.wineList)
        writer = pd.ExcelWriter('saq_wine_list.xlsx', engine='xlsxwriter')
        df.to_excel(writer, sheet_name='Sheet1')
        writer.save()