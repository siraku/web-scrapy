import requests
import pandas as pd
from bs4 import BeautifulSoup
import pymongo
from pymongo import MongoClient

if __name__ == "__main__":
    company_name = []
    company_ticker = []
    URL = "https://www.advfn.com/nyse/newyorkstockexchange.asp?companies=A"
    page = requests.get(URL)
    # print(page.text)
    bs = BeautifulSoup(page.text, 'html.parser')
    odd_rows = bs.find_all('tr', attrs={'class': 'ts0'})
    even_rows = bs.find_all('tr', attrs={'class': 'ts1'})
    for i in odd_rows:
        row = i.find_all('td')
        company_name.append(row[0].text.strip())
        company_ticker.append(row[1].text.strip())
    #         set data
    data = pd.DataFrame(columns=['company_name', 'company_ticker'])
    data['company_name'] = company_name
    data['company_ticker'] = company_ticker
    print(data)
    #     clean data
    data = data[data['company_name'] != '']

    # save data to DB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['stock_company']
    compay = db['Company']

    data.reset_index(inplace=True)
    data_dic = data.to_dict('records')
    compay.insert_many(data_dic)
