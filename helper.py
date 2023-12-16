import sqlite3
from datetime import datetime, date
from exceptions import DuplicateError, NotFoundError


DB_FILE = "exchange.db"


def get_db_connection(db_path=DB_FILE):
    return sqlite3.connect(db_path)


CONN = get_db_connection()
CONN.row_factory = sqlite3.Row  # return a dict like row object



def check_valid_exchanges(exchange_price_pairs: list[tuple]):
    missing_exchanges = []
    cursor = CONN.cursor()
    for tup in exchange_price_pairs:
        exchange = tup[0]
        cursor.execute("SELECT * FROM Exchanges WHERE name=?", (exchange,))
        result = cursor.fetchone()
        if not result:
            missing_exchanges.append(exchange)
    if missing_exchanges:
        raise NotFoundError(
            f"following exchanges {','.join(missing_exchanges)} not found, pls add exchanges first"
        )


def get_exchange_id(name: str) -> int:
    cursor = CONN.cursor()
    cursor.execute("SELECT id FROM Exchanges WHERE name=?", (name,))
    result = cursor.fetchone()
    return result["id"] 

def get_security_id(name:str) -> int:
    cursor = CONN.cursor()
    cursor.execute("SELECT id from Securities WHERE name=?",(name,) )
    result = cursor.fetchone()
    if not result:
        raise NotFoundError(f"commodity {name} not found")
    return result["id"] 