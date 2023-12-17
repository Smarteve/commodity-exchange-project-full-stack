import db_logic


db_logic.add_exchange("LME", "UK's largest commodity exchange", "£")
db_logic.add_exchange("TOMO", "Japan's largest commodity exchange", "¥")

db_logic.add_currency(
    "us/rmb swap",
    "swap",
    "1 year",
    "2024-01-01,2024-01-02",
    [("LME", 11, "2023-10-10"), ("TOMO", 150, "2023-02-02")],
)
