import sqlite3

DB_FILE = "exchange.db"


def main():
    print("Creating tables")
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE Exchanges(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name VARCHAR(255) UNIQUE,
                description TEXT,
                currency_sign VARCHAR(10)
    )

    """
    )

    cursor.execute(
        """CREATE TABLE Securities(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(225) UNIQUE,
        type VARCHAR(10)
    )
    """
    )

    cursor.execute(
        """CREATE TABLE Commodities(
        id INTEGER PRIMARY KEY,
        unit TEXT, 
        FOREIGN KEY (id) REFERENCES Securities(id)
    )
    """
    )

    cursor.execute(
        """CREATE TABLE Currencies(
        id INTEGER PRIMARY KEY,
        type VARCHAR(50),
        tenor VARCHAR(20), 
        settlement_dates DATE,
        FOREIGN KEY (id) REFERENCES Securities(id)
    )
    """
    )

    cursor.execute(
        """CREATE TABLE Prices(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        security_id INT,
        exchange_id INT,
        price DECIMAL(10,2),
        time DATE,
        FOREIGN KEY (security_id) REFERENCES Securities(id),
        FOREIGN KEY (exchange_id) REFERENCES Exchanges(id)
    )
    """
    )

    cursor.execute(
        """
        CREATE TABLE User(
        username TEXT PRIMARY KEY,
        password TEXT
        
        )
"""
    )


if __name__ == "__main__":
    main()
