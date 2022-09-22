import requests
import json
import tomli
import csv
from pathlib import Path
import pandas as pd
import time

config = tomli.loads(Path("../config.toml").read_text(encoding="utf-8"))
AlchemyApiKey = config["AlchemyApiKey"]
BlockVisionApiKey = config["BlockVisionApiKey"]


def getSpamContract():
    url = "https://eth-mainnet.g.alchemy.com/nft/v2/"+AlchemyApiKey+"/getSpamContracts"

    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    resp_dict = json.loads(response.text)
    # load this list to out csv data.
    with open('../data/spam/spamContracts.csv', 'a+', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        writer.writerow(["spamContract"])
        for item in resp_dict:
            # write a row to the csv file
            writer.writerow([item])


def spamMintInformation(contractAddress, page):
    url = "https://api.blockvision.org/v1/"+BlockVisionApiKey

    headers = {
        'Content-Type': 'application/json'
    }
    payload = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "nft_mints",
        "params": {
            "contractAddress": contractAddress,
            "pageSize": 50,
            "pageIndex": page,
        }
    }

    response = requests.request("POST", url, headers=headers, json=payload)
    # print(response.text)
    resp_dict = json.loads(response.text)
    if "result" not in resp_dict:
        return 0
    if "total" not in resp_dict["result"]:
        return 0
    return resp_dict["result"]["total"]


def spamOwnerInformation(contractAddress):
    url = "https://eth-mainnet.g.alchemy.com/nft/v2/"+AlchemyApiKey + \
        "/getOwnersForCollection?contractAddress=" + \
        contractAddress+"&withTokenBalances=false"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    resp_dict = json.loads(response.text)
    data = pd.DataFrame({"ownerAddresses": resp_dict["ownerAddresses"]})
    print(data.ownerAddresses.nunique())

    return len(resp_dict["ownerAddresses"])

# step1 get spam contracts list.
# getSpamContract()

# set mint csv header.
with open("../data/spam/mints.csv", "a+", newline='') as f:
    writer = csv.writer(f)
    writer.writerow(["contract", "mint_number_count", "mint_address_count"])
    f.close()


# read spam contracts list.
list = pd.read_csv("../data/spam/spamContracts.csv")

contract_list = list[['spamContract']]
for index, row in contract_list.iterrows():
    # step2 caculate each contract's mint information.
    print(row.spamContract)
    ret = spamMintInformation(
        row.spamContract, 1)

    distinctCount = spamOwnerInformation(row.spamContract)

    with open("../data/spam/mints.csv", "a+", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(
            [row.spamContract, ret, distinctCount])