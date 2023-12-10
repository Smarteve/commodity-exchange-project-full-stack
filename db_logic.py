import sqlite3

from tables import DB_FILE

class DuplicateExchangeError(Exception):
    pass


# Exceptions


def get_db_connection(db_path = DB_FILE):
    return sqlite3.connect(db_path)


def add_exchange(name: str, description: str, currency_sign: str) -> None:
    conn = get_db_connection()
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO Exchanges(name,description,currency_sign) VALUES(?,?,?)",(name,descripition,currency_sign))
        except sqlite3.IntegrityError:
            raise DuplicateExchangeError(f"Exchange with {name} already exists")
   



def view_exchange(name:str) -> str:
    pass 

def delete_exchange(name:str) -> None:
    pass
    





