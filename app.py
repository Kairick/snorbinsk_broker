from service import get_stocks_from_bank, sync_with_db
from sql_service import get_users


def start_task():
    for user in get_users():
        stocks = get_stocks_from_bank(user['token'])
        sync_with_db(stocks, user['id'])


if __name__ == '__main__':
    start_task()