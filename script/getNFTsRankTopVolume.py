import requests
import json
import csv
import pandas as pd
import time
import tomli
from pathlib import Path


config = tomli.loads(Path("../config.toml").read_text(encoding="utf-8"))
TraitsniperApiKey = config["TraitsniperApiKey"]

# get top 100 nfts sort by total_volume.


def getNftsRankTopVolume(page):
    url = "https://api.traitsniper.com/v1/collections?page=" + \
        str(page)+"&limit=100&sort_total_volume=desc"

    headers = {
        "accept": "application/json",
        "x-ts-api-key": TraitsniperApiKey
    }

    response = requests.get(url, headers=headers)
    resp_dict = json.loads(response.text)
    with open('../data/RankNFTS.csv', 'a+', newline='', encoding="utf-8") as f:
        # create the csv writer
        writer = csv.writer(f)
        for item in resp_dict["collections"]:
            writer.writerow([item["nft_name"], item["supply"], item["total_volume"],
                             item["num_owners"], item["contract_address"]])

# get stolen nfts marked by opensea with param contract address.


def getStolenNftsByContract(contractAddress):
    url = "https://api.traitsniper.com/v1/collections/"+contractAddress+"/stolen_nfts"

    headers = {
        "accept": "application/json",
        "x-ts-api-key": TraitsniperApiKey
    }

    response = requests.get(url, headers=headers)
    # print(response.text)
    resp_dict = json.loads(response.text)
    if "stolen_nfts" not in resp_dict:
        return

    if len(resp_dict["stolen_nfts"]) == 0:
        return
    with open('../data/stolen/'+contractAddress+'.csv', 'a+', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(["tokenID"])
        for item in resp_dict["stolen_nfts"]:
            writer.writerow([item["token_id"]])

# getRankTop100
# for i in range(1,24):
#     getNftsRankTopVolume(i)


data = pd.read_csv("../data/RankNFTS.csv")
contract_list = data[['contract_address']]
for index, row in contract_list.iterrows():
    time.sleep(2.5)
    getStolenNftsByContract(row.contract_address)
