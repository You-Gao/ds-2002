#!/usr/bin/env python3

import requests 
import pandas as pd 

stock = input("Enter a Stock Symbol: ")

print("""
Select modules from:
    - summaryDetail
    - assetProfile
    - fundProfile
    - financialData
    - defaultKeyStatistics
    - calendarEvents
    - incomeStatementHistory
    - incomeStatementHistoryQuarterly
    - cashflowStatementHistory
    - balanceSheetHistory
    - earnings
    - earningsHistory
    - insiderHolders
    - cashflowStatementHistory
    - cashflowStatementHistoryQuarterly
    - insiderTransactions
    - secFilings
    - indexTrend
    - sectorTrend
    - earningsTrend
    - netSharePurchaseActivity
    - upgradeDowngradeHistory
    - institutionOwnership
    - recommendationTrend
    - balanceSheetHistory
    - balanceSheetHistoryQuarterly
    - fundOwnership
    - majorDirectHolders
    - majorHoldersBreakdown
    - price
    - quoteType
    - esgScores
""")

modules = ["financialData","summaryDetail"]
print("Type (Done) to finish selection")
while True:
    module = input("Enter the name of the module from above: ")
    if module == "Done":
        break 
    else:
        modules += [module] 

key = ""
url = "https://yfapi.net/v11/finance/quoteSummary"
url = url + "/" + stock

headers = {
    'x-api-key': key
    }

modules_query = ",".join(modules)
querystring = {"modules":modules_query}

response = requests.get(url, headers = headers, params=querystring)

response_json = response.json()

df = pd.DataFrame(pd.json_normalize(response_json["quoteSummary"]["result"],sep="_"))

print(f"52W High: {df['summaryDetail_fiftyTwoWeekHigh_fmt'].iloc[0]}")
print(f"52W Low: {df['summaryDetail_fiftyTwoWeekLow_fmt'].iloc[0]}")
print(f"ROA: {df['financialData_returnOnAssets_fmt'].iloc[0]}")

for module in modules[2:]:
    print(f"Outputs for {module}:")
    for col in df.columns:
        if col.startswith(module):
            print(f"{col}: {df[col].iloc[0]}")
