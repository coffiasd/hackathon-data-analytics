import csv
import pandas as pd
import requests
import json
import os
from beautifultable import BeautifulTable


def formattedNumber(n):
    return ("{:,}".format(n))


mintInfo = pd.read_csv("../data/spam/mints.csv")
# print(mintInfo.sum())
mint = mintInfo.sum()
total_mints = mint["mint_number_count"]
total_owners = mint["mint_address_count"]
transferInfo = pd.read_csv("../data/spam/transfer.csv")
# print(transferInfo.sum())
transfer = transferInfo.sum()

table = BeautifulTable()
table.columns.header = ["total_mints", "total_owners", "total_transfer"]
table.rows.append([formattedNumber(total_mints),
                   formattedNumber(total_owners), formattedNumber(transfer["transfer"])])
print(table)
