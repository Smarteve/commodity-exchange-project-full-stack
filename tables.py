import sqlite3
DB_FILE = "exchange.db"
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()


cursor.execute(
    """CREATE TABLE Exchanges(
               id INT PRIMARY KEY,
               name VARCHAR(255) UNIQUE,
               description TEXT,
               currency_sign VARCHAR(10)
)

"""
)

cursor.execute('''CREATE TABLE Securities(
    id INT PRIMARY KEY,
    name VARCHAR(225) UNIQUE,
    type VARCHAR(10)
)
''')


cursor.execute('''CREATE TABLE Commodities(
    id INT PRIMARY KEY,
    unit TEXT, 
    FOREIGN KEY (id) REFERENCES Securities(id)
)
''')
 
cursor.execute('''CREATE TABLE Currencies(
    id INT PRIMARY KEY,
    type VARCHAR(50),
    tenor VARCHAR(20), 
    settlement_dates DATE,
    FOREIGN KEY (id) REFERENCES Securities(id)
)
''')

cursor.execute('''CREATE TABLE Prices(
    id INT PRIMARY KEY,
    security_id INT,
    exchange_id INT,
    price DECIMAL(10,2),
    time DATE,
    FOREIGN KEY (security_id) REFERENCES Securities(id),
    FOREIGN KEY (exchange_id) REFERENCES Exchanges(id)
)
''')