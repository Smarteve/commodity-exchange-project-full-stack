import sqlite3
from datetime import datetime, date
from exceptions import DuplicateError, NotFoundError

DB_FILE = "exchange.db"


def get_db_connection(db_path=DB_FILE):
    return sqlite3.connect(db_path)


CONN = get_db_connection()
CONN.row_factory = sqlite3.Row  # return a dict like row object


def add_exchange(name: str, description: str, currency_sign: str) -> None:
    cursor = CONN.cursor()
    try:
        cursor.execute(
            "INSERT INTO Exchanges(name,description,currency_sign) VALUES(?,?,?)",
            (name, description, currency_sign),
        )
    except sqlite3.IntegrityError:
        raise DuplicateError(f"Record with {name} already exists")
    CONN.commit()


def view_exchange(name: str) -> str:
    cursor = CONN.cursor()
    cursor.execute("SELECT name,description FROM Exchanges WHERE name=?", (name,))
    result = cursor.fetchone()
    return result


def delete_exchange(name: str) -> None:
    cursor = CONN.cursor()
    cursor.execute("DELETE FROM Exchanges WHERE name=?", (name,))
    if CONN.total_changes == 0:
        raise NotFoundError(f"record not found in system")
    CONN.commit()


def _check_valid_exchanges(exchange_price_pairs: list[tuple]):
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


def _get_exchange_id(name: str) -> int:
    cursor = CONN.cursor()
    cursor.execute("SELECT id FROM Exchanges WHERE name=?", (name,))
    result = cursor.fetchone()
    return result["id"]


def add_prices(security_id, exchange_price_pairs: list[tuple]) -> None:
    cursor = CONN.cursor()
    for exchange, price, time in exchange_price_pairs:
        exchange_id = _get_exchange_id(exchange)
        time_object = datetime.strptime(time, "%Y-%m-%d").date()
        cursor.execute(
            "INSERT INTO PRICES(security_id,exchange_id,price,time) VALUES(?,?,?,?)",
            (security_id, exchange_id, price, time_object),
        )
    CONN.commit()


def add_commodity(name: str, unit: str, exchange_price_pairs: list[tuple]) -> None:
    _check_valid_exchanges(exchange_price_pairs)
    cursor = CONN.cursor()
    try:
        cursor.execute(
            "INSERT INTO Securities(name,type) VALUES(?,?)", (name, "commodity")
        )
    except sqlite3.IntegrityError:
        raise DuplicateError(f"record with commodity {name} already exists")
    security_id = cursor.lastrowid

    cursor.execute("INSERT INTO Commodities(id,unit) VALUES(?,?)", (security_id, unit))

    add_prices(security_id, exchange_price_pairs)
    CONN.commit()


def view_commodity(name: str) -> str:
    cursor = CONN.cursor()
    cursor.execute(
        """
        SELECT *, Exchanges.name as exchange_name FROM Securities
            INNER JOIN Commodities ON Securities.id = Commodities.id
            INNER JOIN Prices ON Securities.id = Prices.security_id
            INNER JOIN Exchanges ON Prices.exchange_id = Exchanges.id
            WHERE Securities.name = ?
    """,
        (name,),
    )
    security_id = cursor.fetchone()
    return security_id
