#!/usr/bin/env python3

import requests 

key = ""
url = "https://yfapi.net/v1/finance/trending/US"

headers = {
    'x-api-key': key
    }

response = requests.get(url, headers=headers)

response_json1 = response.json()

for symbol in response_json1["finance"]["result"][0]["quotes"]:
    symbol = symbol["symbol"]
    url = "https://yfapi.net/v6/finance/quote"
    querystring = {"symbols":symbol}
    response = requests.get(url, headers = headers, params=querystring)
    response_json = response.json()
    for result in response_json["quoteResponse"]["result"]:
        print(f"{result["symbol"]}, 52W High: {result["fiftyTwoWeekHigh"]}, 52W Low: {result["fiftyTwoWeekLow"]}, Current Price: {result["regularMarketPrice"]}")

     
