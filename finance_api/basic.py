#!/usr/bin/env python3

import requests 

stocks = []

print("Type (Finish) to submit query") 
while True:
    stock = input("Enter a Stock Symbol: ")

    if stock == "Finish":
        break 
    else:
        stocks += [stock] 

print("Generating Query")
stocks = ", ".join(stocks)
print(stocks)
print("")

key = ""
url = "https://yfapi.net/v6/finance/quote"

headers = {
    'x-api-key': key
    }

querystring = {"symbols":stocks}

response = requests.get(url, headers = headers, params=querystring)

response_json = response.json()

for result in response_json["quoteResponse"]["result"]:
    print(f"Stock Ticker: {result["symbol"]}, Company: {result["longName"]}, Current Market Price: ${result["regularMarketPrice"]:0.2f}") 
