import pandas as pd
import requests
import tomli
from pathlib import Path
import json
import time
import csv

config = tomli.loads(Path("../config.toml").read_text(encoding="utf-8"))
AlchemyApiKey = config["AlchemyApiKey"]
BlockVisionApiKey = config["BlockVisionApiKey"]


def getSpamTotalTransfer(contractAddress):
    url = "https://api.blockvision.org/v1/"+BlockVisionApiKey

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "nft_contractStats",
        "params": {
            "blockNumber": 0,
            "contractAddress": contractAddress
        }
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    resp_dict = json.loads(response.text)
    if "result" not in resp_dict:
        return -1
    return resp_dict["result"]["totalTransfer"]


with open("../data/spam/transfer.csv", "a+", newline='') as f:
    writer = csv.writer(f)
    # read spam contracts list.
    list = pd.read_csv("../data/spam/spamContracts.csv")
    contract_list = list[['spamContract']]
    for index, row in contract_list.iterrows():
        if index < 1246:
            continue
        total = getSpamTotalTransfer(row.spamContract)
        print(row.spamContract, total)
        writer.writerow([row.spamContract, total])
        time.sleep(0.2)
