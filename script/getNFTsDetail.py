import cloudscraper
import pandas as pd
import json
import time
import csv

contract = "0x23581767a106ae21c074b2276d25e5c3e136a68b"

scraper = cloudscraper.create_scraper()
data = pd.read_csv("../data/stolen/tokenIDs/"+contract+".csv")
contract_list = data[['tokenID']]
for index,row in contract_list.iterrows():
    url = 'https://api.traitsniper.com/api/projects/proof-moonbirds/nfts?token_id='+str(row.tokenID)
    resp = scraper.get(url).text
    resp_dict = json.loads(resp)
    with open("../data/stolen/lastSalePrice/"+resp_dict["contract_address"]+".csv",'a+',newline='') as f:
            writer = csv.writer(f)
            writer.writerow([resp_dict["nfts"][0]["token_id"],resp_dict["nfts"][0]["price"]["last_sale_price"]])
    time.sleep(2.5)