import sqlite3
from datetime import datetime, date
from common.exceptions import DuplicateError, NotFoundError
import common.helper as helper


DB_FILE = "exchange.db"


def get_db_connection(db_path=DB_FILE):
    return sqlite3.connect(db_path,check_same_thread=False)


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


def add_prices(security_id, exchange_price_pairs: list[tuple]) -> None:
    cursor = CONN.cursor()
    for exchange, price, time in exchange_price_pairs:
        exchange_id = helper.get_exchange_id(exchange)
        cursor.execute(
            "INSERT INTO PRICES(security_id,exchange_id,price,time) VALUES(?,?,?,?)",
            (security_id, exchange_id, price, time),
        )
    CONN.commit()


def add_commodity(name: str, unit: str, exchange_price_time_pairs: list[str]) -> None:
    helper.check_valid_exchanges(exchange_price_time_pairs)
    cursor = CONN.cursor()
    try:
        cursor.execute(
            "INSERT INTO Securities(name,type) VALUES(?,?)", (name, "commodity")
        )
    except sqlite3.IntegrityError:
        raise DuplicateError(f"record with commodity {name} already exists")
    security_id = cursor.lastrowid

    cursor.execute("INSERT INTO Commodities(id,unit) VALUES(?,?)", (security_id, unit))

    add_prices(security_id, exchange_price_time_pairs)
    CONN.commit()


def view_commodity(name: str) -> list[str]:
    cursor = (
        CONN.cursor()
    )  # using alias given there are two names in two tables,otherwise one name will overwrite the other

    cursor.execute(
        """
        SELECT unit, Exchanges.name as exchange_name, price,time,currency_sign FROM Securities
            INNER JOIN Commodities ON Securities.id = Commodities.id
            INNER JOIN Prices ON Securities.id = Prices.security_id
            INNER JOIN Exchanges ON Prices.exchange_id = Exchanges.id
            WHERE Securities.name = ?
    """,
        (name,),
    )
    result = cursor.fetchall() #row object result
    #parsing row object 
    price_info = []
    info = []
    for subset in result:
        unit = subset["unit"]
        exchange_name = subset['exchange_name']
        price = subset["price"]
        time = subset["time"]
        currency_sign = subset["currency_sign"]
        price_info.append((exchange_name,price,time,currency_sign))
    info.append(f"the trading info for {name}is: ")
    for exchange_name,price,time,currency_sign in price_info:
        info.append(f"{exchange_name}: {currency_sign}{price} per {unit} at {time}")

    return info


def delete_commodity(name: str) -> None:
    security_id = helper.get_security_id(name)
    cursor = CONN.cursor()
    cursor.execute("DELELE FROM Securities WHERE id=?", (security_id,))
    cursor.execute("DELETE FROM Commodities WHERE id=?", (security_id,))
    cursor.execute("DELETE FROM Prices WHERE security_id=?", (security_id,))

    CONN.commit()


def add_currency(
    name: str,
    type: str,
    tenor: str,
    settlement_dates: str,
    exchange_price_time_pairs: list[tuple],
) -> None:
    helper.check_valid_exchanges(exchange_price_time_pairs)
    cursor = CONN.cursor()
    try:
        cursor.execute(
            "INSERT INTO Securities(name,type) Values(?,?)", (name, "currency")
        )
    except sqlite3.IntegrityError:
        raise DuplicateError(f"currency{name} already existed")

    security_id = cursor.lastrowid

    cursor.execute(
        "INSERT INTO Currencies(id,type,tenor,settlement_dates) VALUES(?,?,?,?)",
        (security_id, type, tenor, settlement_dates),
    )
    add_prices(security_id, exchange_price_time_pairs)
    CONN.commit()


def view_currency(name: str) -> list[str]:
    cursor = CONN.cursor()
    cursor.execute(
        """
        SELECT Currencies.type as currency_type,tenor,settlement_dates,Exchanges.name as exchange_name,price,time,currency_sign FROM Securities
        INNER JOIN Currencies ON Securities.id = Currencies.id 
        INNER JOIN Prices ON Securities.id = Prices.security_id
        INNER JOIN Exchanges ON Prices.exchange_id = Exchanges.id
        WHERE Securities.name=?
""",
        (name,),
    )
    result = cursor.fetchall()

    price_info = []
    info = []
    for subset in result:
        tenor = subset["tenor"]
        settlement_dates = subset["settlement_dates"]
        currency_type = subset["currency_type"]
        exchange_name = subset['exchange_name']
        price = subset["price"]
        time = subset["time"]
        currency_sign = subset["currency_sign"]
        price_info.append((exchange_name,price,time,currency_sign))
    
    info.append(f"{name} is a {currency_type}, it has a tenor of {tenor}, its settlement date is {settlement_dates}") 
    info.append("it's trading info is")
    for exchange_name,price,time,currency_sign in price_info:
        info.append(f"{exchange_name}: {currency_sign}{price} at {time}")
    return info


def delete_currency(name: str) -> None:
    security_id = helper.get_security_id(name)
    cursor = CONN.cursor()
    cursor.execute("DELETE FROM Securites WHERE id=?", (security_id,))
    cursor.execute("DELETE FROM Currencies WHERE id=?", (security_id,))
    cursor.execute("DELETE FROM Prices WHERE security_id=?", (security_id,))
    CONN.commit()
