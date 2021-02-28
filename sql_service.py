import sqlite3
from decouple import config


def connect_db():
    con = sqlite3.connect(config('DATABASE'))
    return con


def init_tables():
    con = connect_db()
    cursor = con.cursor()
    cursor.execute("CREATE TABLE stocks(id integer not null PRIMARY KEY, name text, description text)")
    cursor.execute("CREATE TABLE buyer(id integer not null PRIMARY KEY, name text, user_id text)")
    cursor.execute("CREATE TABLE stocks_price(id integer not null PRIMARY KEY, date datetime, price integer,"
                   "stock_id integer not null,"
                   "buyer_id integer not null,"
                   "FOREIGN KEY (stock_id) REFERENCES stocks(id),"
                   "FOREIGN KEY (buyer_id) REFERENCES buyer(id))")

    con.commit()
    con.close()


