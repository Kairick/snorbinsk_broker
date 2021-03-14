from service import get_all_stocks, get_stock_history
from sql_service import get_token


def start_analys():
    token = get_token()
    stocks = get_all_stocks(token)
    for stock in stocks:
        get_stock_history(stock)



if __name__ == '__main__':
    start_analys()