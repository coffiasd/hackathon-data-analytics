import csv
import pandas as pd
import requests
import json
import os
import tomli
from beautifultable import BeautifulTable
from pathlib import Path

config = tomli.loads(Path("../config.toml").read_text(encoding="utf-8"))
TraitsniperApiKey = config["TraitsniperApiKey"]


def getCollectionDetail(contractAddress):
    url = "https://api.traitsniper.com/v1/collections/"+contractAddress

    headers = {
        "accept": "application/json",
        "x-ts-api-key": TraitsniperApiKey
    }
    response = requests.get(url, headers=headers)

    return json.loads(response.text)


def caculateContractItem(contractAddress, table):
    # get collection detail
    item = getCollectionDetail(contractAddress)

    # read stolen nfts list
    data = pd.read_csv("../data/stolen/lastSalePrice/" +
                       contractAddress+".csv", header=None)
    # caculate items
    num = data.count()
    sum = 0
    for index, row in data.iterrows():
        # print(row[1])
        if row[1] > item["floor_price"]:
            sum += row[1]
        else:
            sum += item["floor_price"]
    table.rows.append([item["nft_name"], contractAddress, item["total_volume"],
                       sum, sum/item["total_volume"], num[0]])


# loop to caculate each item.
table = BeautifulTable()
table.columns.header = ["nft_name", "contract",
                        "total_volume", "total_stolen", "percent", "item_num"]
for name in os.listdir('../data/stolen/lastSalePrice/'):
    caculateContractItem(os.path.splitext(name)[0], table)
print(table)
