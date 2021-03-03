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
    cursor.execute("CREATE TABLE buyer(id integer not null PRIMARY KEY, name text, telegram_id text, token text)")
    cursor.execute("CREATE TABLE stock_price(id integer not null PRIMARY KEY,"
                   "date datetime default current_timestamp, price real, wealth_ratio integer, total integer,"
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
    return cursor.fetchall()


def get_stocks_from_db(user_id):
    con = connect_db()
    con.row_factory = dict_factory
    cursor = con.cursor()
    query = f"select * from stock_price where buyer_id = {user_id}"
    cursor.execute(query)
    return cursor.fetchall()