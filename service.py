import json

import requests
"https://iss.moex.com/iss/engines/stock/markets/shares/securities/AFLT.json"


def add_new_stock(message, buyer_id):
    stock_data = check_stock(message[1])
    if stock_data is None:
        return None


def check_stock(name):
    result = {}
    response = requests.get(f"https://iss.moex.com/iss/engines/stock/markets/shares/securities/{name}.json")
    stock_data = json.loads(response.text)
    if not stock_data['marketdata']['data']:
        return None
    name = stock_data['securities']['data'][0][2]
    return name
