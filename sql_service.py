import datetime
import sqlite3
from decouple import config


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def connect_db():
    con = sqlite3.connect(config('DATABASE'))
    return con


def init_tables():
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("CREATE TABLE buyer(id integer not null PRIMARY KEY, name text, "
                   "wealth_ratio integer, telegram_id text, token text)")
    cursor.execute("CREATE TABLE stock_price(id integer not null PRIMARY KEY, name text,"
                   "date datetime default , price real, total integer,"
                   "buyer_id integer not null,"
                   "FOREIGN KEY (buyer_id) REFERENCES buyer(id))")

    con.commit()
    con.close()


def get_users():
    con = connect_db()
    con.row_factory = dict_factory
    cursor = con.cursor()
    query = f"select * from buyer"
    cursor.execute(query)
    result = cursor.fetchall()
    con.commit()
    con.close()
    return result


def get_stocks_from_db(user_id):
    con = connect_db()
    con.row_factory = dict_factory
    cursor = con.cursor()
    query = f"select * from stock_price where buyer_id = {user_id}"
    cursor.execute(query)
    result = cursor.fetchall()
    con.commit()
    con.close()
    return result


def save_changes_to_db(item):
    con = connect_db()
    cursor = con.cursor()
    query = "update stock_price set price = '{0}', " \
            "total = '{1}', date = '{2}'" \
            " where name = '{3}'".format(item['price'], item['total'], datetime.datetime.now(), item['name'])

    cursor.execute(query)
    con.commit()
    con.close()


def add_to_db(stocks, name, user_id):
    con = connect_db()
    cursor = con.cursor()
    query = "insert into stock_price (name, price, total, buyer_id)" \
            " values ('{0}', '{1}', '{2}', '{3}')".format(name, stocks['old_price'], int(stocks['total']), user_id)
    cursor.execute(query)
    con.commit()
    con.close()


def del_from_db(name, user_id):
    con = connect_db()
    cursor = con.cursor()
    query = "delete from stock_price where name = '{0}' and buyer_id = '{1}'".format(name, user_id)
    cursor.execute(query)
    con.commit()
    con.close()
