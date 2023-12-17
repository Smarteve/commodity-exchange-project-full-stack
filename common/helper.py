import sqlite3
from datetime import datetime, date
from collections import defaultdict
from common.exceptions import DuplicateError, NotFoundError


DB_FILE = "exchange.db"


def get_db_connection(db_path=DB_FILE):
    return sqlite3.connect(db_path, check_same_thread=False)


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


def get_security_id(name: str) -> int:
    cursor = CONN.cursor()
    cursor.execute("SELECT id from Securities WHERE name=?", (name,))
    result = cursor.fetchone()
    if not result:
        raise NotFoundError(f"commodity {name} not found")
    return result["id"]


def get_exchange_list() -> list[str]:
    cursor = CONN.cursor()
    cursor.execute("SELECT name from Exchanges")
    result = cursor.fetchall()
    exchange_list = [exchange["name"] for exchange in result]
    return exchange_list


def get_security_traded_in_exchange(name: str) -> dict[str:str]:
    cursor = CONN.cursor()
    cursor.execute(
        """
        SELECT Securities.name as security_name,Securities.type as security_type FROM Exchanges
        INNER JOIN Prices ON Exchanges.id = Prices.exchange_id
        INNER JOIN Securities ON Prices.security_id = Securities.id
        WHERE Exchanges.name =?

""",
        (name,),
    )
    result = cursor.fetchall()
    exchange_dict = defaultdict(list)

    for row in result:
        exchange_dict[row["security_type"]].append(row["security_name"])
    return exchange_dict


def is_valid_username_password(username, password):
    cursor = CONN.cursor()
    cursor.execute(
        "SELECT * FROM User WHERE username=? and password=?", (username, password)
    )
    user = cursor.fetchone()
    if user:
        return True
    return False


def is_valid_username(username):
    cursor = CONN.cursor()
    cursor.execute("SELECT * FROM User WHERE username=?", (username,))
    user = cursor.fetchone()

    if user:
        return False
    return True


def add_user(username, password):
    cursor = CONN.cursor()
    cursor.execute(
        "INSERT INTO User(username,password) VALUES (?,?)", (username, password)
    )
    CONN.commit()
