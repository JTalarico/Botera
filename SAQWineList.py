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
        pageSize = 100
        self.url = 'https://www.saq.com/webapp/wcs/stores/servlet/SearchDisplay?pageSize='+ str(pageSize) + '&searchTerm=*&catalogId=50000&showOnly=product&beginIndex=0&langId=-1&storeId=20002&a'
        self.wineList = []
        #self.getList()

    def getList(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = soup.findAll('p', attrs={'class': 'nom'})
        desc = soup.findAll('p', attrs={'class': 'desc'})
        flavor = soup.findAll('p', attrs={'class': 'flavor'})
        price = soup.findAll('td', attrs={'class': 'price'})

        for i in range(len(name)):

            try:
                wineFlavor = re.findall('Taste Tag: (.*)" ', flavor[i].find("img"))[0]
            except:
                wineFlavor = 'Unknown'

            wineName = re.findall('details (.*)"', str(name[i]))[0]
            winePrice = re.findall('\$([^\*\n]*)', price[i].text)[0]
            wineRegion = re.findall('\s*(.*),', desc[i].text)[0]
            wineType = desc[i].text.strip().split('\r')[0]

            if ("wine" in wineType) or (wineType == 'Rosé'):
                self.wineList.append({                                            
                                        "name" : wineName,
                                        "flavor" : wineFlavor,
                                        "price" : winePrice,
                                        "region" : wineRegion,
                                        "type" : wineType
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