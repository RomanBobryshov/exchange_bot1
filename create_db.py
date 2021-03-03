import sqlite3


con = sqlite3.connect('exchange_bot.db')
with con:
    con.execute("""
        CREATE TABLE EXCHANGE (
            base TEXT,
            rate TEXT,
            time NUMERIC
        );
    """)

