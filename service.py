import datetime
import json

import requests

from sql_service import get_stocks_from_db

URL = 'https://api-invest.tinkoff.ru/openapi/portfolio'


def get_stocks_from_bank(token):
    raw_data = get_raw_data(token)
    return get_clean_data(raw_data.text)



def get_raw_data(token):
    headers = {"Authorization": f'Bearer {token}'}
    response = requests.get(URL, headers=headers)
    return response


def get_clean_data(raw_data):
    result = []
    json_data = json.loads(raw_data)
    for item in json_data['payload']['positions']:
        result.append(prepare_item(item))

    return result


def prepare_item(item):
    return dict(
        price=get_current_price(item),
        total=item['balance'],
        name=item['ticker'],
        old_price=item['averagePositionPrice']['value'],
        date=datetime.datetime.utcnow()
    )


def get_current_price(item):
    return (item['averagePositionPrice']['value']*item['balance'] + item['expectedYield']['value'])/item['balance']


def sync_with_db(stocks, user_id):
    local_stocks = get_stocks_from_db(user_id)
    compare_stocks(stocks, local_stocks)


def compare_stocks(stocks, local_stocks):
    pass