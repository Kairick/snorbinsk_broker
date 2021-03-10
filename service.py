import datetime
import json

import requests

from brocker import send_message
from sql_service import get_stocks_from_db, save_changes_to_db, add_to_db, del_from_db

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
        date=datetime.datetime.now()
    )


def get_current_price(item):
    return (item['averagePositionPrice']['value']*item['balance'] + item['expectedYield']['value'])/item['balance']


def sync_with_db(stocks, user):
    local_stocks = get_stocks_from_db(user['id'])
    compare_stocks(stocks, local_stocks, user)


def compare_stocks(stocks, local_stocks, user):
    stocks_names = set([stock.get('name') for stock in stocks])
    local_stocks_names = set([local_stock.get('name') for local_stock in local_stocks])
    update_stocks(set.intersection(stocks_names, local_stocks_names), stocks, local_stocks, user)
    add_stocks(set.difference(stocks_names, local_stocks_names), stocks, user)
    del_stocks(set.difference(local_stocks_names, stocks_names), user)


def add_stocks(names, stocks, user):
    for name in names:
        add_to_db(get_stock(name, stocks), name, user['id'])


def del_stocks(names, user):
    for name in names:
        del_from_db(name, user['id'])


def ready_to_sell(user, cur_local_stock):
    p = cur_local_stock['price']
    ev = cur_local_stock['new_price']
    x = user['wealth_ratio']
    f = (x/100*1.003*p + 0.87261*p)/0.86739
    return True if ev > f else False


def update_stocks(names, stocks, local_stocks, user):
    for name in names:
        cur_stock = get_stock(name, stocks)
        cur_local_stock = get_stock(name, local_stocks)
        if cur_stock['total'] != cur_local_stock['total']:
            if cur_local_stock['total'] < cur_stock['total']:
                cur_local_stock['price'] = (cur_stock['price'] + cur_local_stock['price']) / 2
            cur_local_stock['total'] = cur_stock['total']
            save_changes_to_db(cur_local_stock)
        cur_local_stock['new_price'] = cur_stock['price']
        if ready_to_sell(user, cur_local_stock):
            send_message(user['telegram_id'], cur_local_stock['name'], cur_local_stock['new_price'])


def get_stock(name, stocks):
    return [stock for stock in stocks if stock['name'] == name][0]
