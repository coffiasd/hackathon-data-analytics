import requests
import json
import csv
import tomli
from pathlib import Path

config = tomli.loads(Path("../config.toml").read_text(encoding="utf-8"))
AlchemyApiKey = config["AlchemyApiKey"]

# currentContractAddress = "0x60e4d786628fea6478f785a6d7e704777c86a7c6"
list = [
    "0xed5af388653567af2f388e6224dc7c4b3241c544",
    "0x49cf6f5d44e70224e2e23fdcdd2c053f30ada28b",
    "0x23581767a106ae21c074b2276d25e5c3e136a68b",
    "0x394e3d3044fc89fcdd966d3cb35ac0b32b0cda91",
    "0xbd3531da5cf5857e7cfaa92426877b022e612cf8",
]

# get the tokenID lists from alchemy api getNFTsForCollection.


def fetchCollection(contractAddress, startToken):
    query_params = {
        "contractAddress": contractAddress,
        "withMetadata": False,
        "limit": 100,
        "startToken": startToken
    }
    url = "https://eth-mainnet.g.alchemy.com/nft/v2/"+AlchemyApiKey+"/getNFTsForCollection"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers, params=query_params)
    resp_dict = json.loads(response.text)
    # create an csv handle
    with open('../data/'+contractAddress+'.csv', 'a+', newline='') as f:
        # create the csv writer
        writer = csv.writer(f)
        # writer.writerow(["tokenID"])
        for item in resp_dict["nfts"]:
            # write a row to the csv file
            writer.writerow([int(item["id"]["tokenId"], 16)])
    if "nextToken" in resp_dict:
        # return resp_dict["nextToken"]
        fetchCollection(currentContractAddress, resp_dict["nextToken"])
    else:
        return None


# fetchCollection(currentContractAddress, "")
for currentContractAddress in list:
    fetchCollection(currentContractAddress, "")
