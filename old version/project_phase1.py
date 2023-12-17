"""
update3

add ABC classes, update unittest 

"""
from abc import ABC, abstractmethod
from typing import Dict
from datetime import datetime, date


class Security(ABC):
    def __init__(self, name: str, prices: list["Price"]):
        self.name = name
        self.prices = prices

    @abstractmethod
    def get_exchange_list(self):
        pass


class Main:
    def __init__(self):
        self.exchange_dict: Dict[
            str, "Exchange"
        ] = {}  # key exchange name, value exchange object
        self.commodity_dict: Dict[
            str, "Commodity"
        ] = {}  # key commodity name, value commodity object
        self.currency_dict: Dict[
            str, "Currency"
        ] = {}  # key currency name, value currency object

    def add_exchange(self, name: str, description: str, currency_sign: str) -> None:
        if name in self.exchange_dict:
            print("exchange already existed, add a new exchange")
            return
        else:
            new_exchange = Exchange(name, description, currency_sign)
            self.exchange_dict[name] = new_exchange

    def add_commodity(self, commodity: "Commodity") -> None:
        # check if commodity exist
        if commodity.name in self.commodity_dict:
            raise ValueError(
                f"{commodity.name} already existed, pls enter a new commodity"
            )
        self.commodity_dict[commodity.name] = commodity

    def add_currency(self, currency: "Currency") -> None:
        if currency.name in self.currency_dict:
            raise ValueError(
                "f{currency.name} already existed, pls enter a new currency"
            )
        self.currency_dict[currency.name] = currency

    def _missing_exchanges_list(self, exchange_list: list[str]) -> list[str]:
        return [
            exchange for exchange in exchange_list if exchange not in self.exchange_dict
        ]

    def view_exchange(self, name: str) -> str:
        print(self.exchange_dict[name]) if name in self.exchange_dict else print(
            f"{name} does not exist"
        )

    def view_commodity(self, name: str) -> str:
        print(self.commodity_dict[name]) if name in self.commodity_dict else print(
            "commodity not found"
        )

    def view_currency(self, name: str) -> str:
        print(self.currency_dict[name]) if name in self.currency_dict else print(
            "commodity not found"
        )

    def remove_exchange(self, name: str) -> None:
        # delete from exchange main dic
        if name in self.exchange_dict:
            del self.exchange_dict[name]
        else:
            print("exchange not found")
        # delete from commodity.prices
        for commodity in list(self.commodity_dict.values()):
            for price in commodity.prices:
                if price.exchange.name == name:
                    commodity.prices.remove(price)
        print(f"{name} has been removed from exchanges")

    def remove_commodity(self, name: str) -> None:
        # delete from the main commodity dict
        if name in self.commodity_dict:
            del self.commodity_dict[name]
        else:
            print("commodity not found")
        # delete from exchange.commodity list
        for exchange in list(self.exchange_dict.values()):
            for commodity in exchange.commodities:
                if commodity == name:
                    exchange.commodities.remove(commodity)
        print(f"{name} has been removed from commodities")

    def remove_currency(self, name: str) -> None:
        # delete from the main currency dict
        if name in self.currency_dict:
            del self.currency_dict[name]
        else:
            print("currency not found")
        # delete from exchange.currency list
        for exchange in list(self.exchange_dict.values()):
            for currency in exchange.currencies:
                if currency == name:
                    exchange.currencies.remove(currency)
        print(f"{name} has been removed from currencies")

    def get_exchange(self, name: str) -> "Exchange":
        return self.exchange_dict[name]

    def get_commodity(self, name: str) -> "Commodity":
        return self.commodity_dict[name]


def _parse_time(time) -> date:
    time_object = datetime.strptime(time, "%Y-%m-%d")
    return time_object.date()  # print only date


class Exchange:
    def __init__(self, name: str, description: str, currency_sign: str):
        self.name = name
        self.description = description
        self.currency_sign = currency_sign
        self.commodities = []  # a list of commodity names
        self.currencies = []  # a list of currency names

    def __str__(self):
        if (
            self.commodities
        ):  # when add exchange, only requires administrator to add name and intro first, if no commodities at first then dont display
            return (
                f"{self.name} is {self.description}."
                f"The list of the commodities currently trading in {self.name} is {','.join(self.commodities)}."
            )
        else:
            return f"{self.name} is {self.description}."

    def add_commodity(self, name: str) -> None:
        self.commodities.append(name)

    def add_currency(self, name: str) -> None:
        self.currencies.append(name)


class Commodity(Security):
    def __init__(self, name: str, unit: str, prices: list["Price"]):
        super().__init__(name, prices)
        self.unit = unit

    def get_exchange_list(self) -> list[str]:
        return [price.exchange.name for price in self.prices]

    def __str__(self):
        last_traded_price = max(self.prices, key=lambda price: price.time)
        last_traded_exchange = last_traded_price.exchange
        currency_sign = last_traded_exchange.currency_sign
        info = []
        info.append(f"{self.name} is traded at {','.join(self.get_exchange_list())}.")
        info.append(
            f"It is last traded at {currency_sign}{last_traded_price.value} in {last_traded_exchange.name} per {self.unit}."
        )
        info.append(f"The full trading info is:")
        for price in self.prices:
            info.append(str(price))
        return "\n".join(info)


class Currency(Security):
    def __init__(
        self,
        name: str,
        prices: list["Price"],
        type: str,
        settlement_dates: list[date],
        tenor: str,
    ):
        super().__init__(name, prices)
        self.type = type
        self.settlement_dates: list[date] = settlement_dates
        self.tenor = tenor

    def get_exchange_list(self) -> list[str]:
        return [price.exchange.name for price in self.prices]

    def __str__(self) -> str:
        settlement_dates_str = ", ".join(
            [d.strftime("%Y-%m-%d") for d in self.settlement_dates]
        )
        return f"{self.name} ({self.type}) is traded at {','.join(self.get_exchange_list())} with settlement dates {settlement_dates_str} and tenor {self.tenor}."


class Price:
    def __init__(self, exchange: Exchange, time: date, value: float):
        self.exchange: Exchange = exchange
        self.time = time
        self.value = value

    def __str__(self):
        currency_sign = self.exchange.currency_sign
        return f"{currency_sign}{self.value} at {self.exchange.name} at {self.time}"


if __name__ == "__main__":
    main = Main()
    main.add_exchange("TOMO", "Japan's largest commodity futures exchanges", "¥")
    print("Welcome")
    while True:
        print("-----")
        print("choose your action: ")
        print("1 Add an exchange")
        print("2 Add a commodity")
        print("3 Add a currency")
        print("4 View an exchange")
        print("5 View an commodity")
        print("6 View a currency")
        print("7 Remove an exchange")
        print("8 Remove a commodity")
        print("9 Remove a currency")
        print("10 Exit")
        print("-----")
        action = input("please choose a number (1 to 7): ")
        if action == "1":
            exchange_list = input("What's the name of the exchange you want to add? ")
            description = input(
                f"What's the descripition of the exchange? {exchange_list} is: "
            )
            currency_sign = input(
                f"what's the primary currency of the exchange? choose from ¥,$,£ and yuan: "
            )
            main.add_exchange(exchange_list, description, currency_sign)
            print(f"Thanks for adding {exchange_list}")

        if action == "2":
            # add new commodity
            name = input("What is the name of the commodity you want to add? ")
            unit = input("What is the unit of the commodity? ")
            exchange_list = input(
                f"what is the exchange {name} is traded at(comma separated if multiple): "
            ).split(",")
            prices = []

            if missing_exchanges := main._missing_exchanges_list(exchange_list):
                print(
                    f"Missing exchanges: {','.join(missing_exchanges)},pls add missing exchange first"
                )
                continue

            for exchange in exchange_list:
                time = _parse_time(
                    input(f"Enter the last traded time in {exchange}(yyyy-mm-dd): ")
                )
                price = float(input(f"Enter the price of last trade in {exchange}: "))
                prices.append(Price(main.get_exchange(exchange), time, price))
            try:
                main.add_commodity(Commodity(name, unit, prices))
            except ValueError as e:
                print(e)
                continue
            main.get_exchange(exchange).add_commodity(
                name
            )  # update self.commodities under Exchange class
            print(f"Thanks for adding {name}")
        if action == "3":
            # add new currency
            name = input("What is the name of the currency you want to add? ")
            settlement_dates_str = input(
                "What is the settlement date of the commodity (yyyy-mm-dd)? comma separated if multiple "
            ).split(",")
            settlement_dates = [_parse_time(time) for time in settlement_dates_str]
            type = input(
                "what is the type of this currency, choose from spot/forward/swap "
            )
            tenor = input(
                "what is the tenor of this currency (example: 3 years or 18 months) "
            )
            exchange_list = input(
                f"what is the exchange {name} is traded at(comma separated if multiple): "
            ).split(",")
            prices = []

            if missing_exchanges := main._missing_exchanges_list(exchange_list):
                print(
                    f"Missing exchanges: {','.join(missing_exchanges)},pls add missing exchange first"
                )
                continue
            for exchange in exchange_list:
                time = _parse_time(
                    input(f"Enter the last traded time in {exchange}(yyyy-mm-dd): ")
                )
                price = float(input(f"Enter the price of last trade in {exchange}: "))
                prices.append(Price(main.get_exchange(exchange), time, price))
            try:
                main.add_currency(Currency(name, prices, type, settlement_dates, tenor))
            except ValueError as e:
                print(e)
                continue
            main.get_exchange(exchange).add_currency(
                name
            )  # update self.currencies under Exchange class
            print(f"Thanks for adding {name}")

        if action == "4":
            name = input("Which exchange do you want to view? ")
            main.view_exchange(name)
        if action == "5":
            name = input("Which commodity do you want to view? ")
            main.view_commodity(name)
        if action == "6":
            name = input("Which currency do you want to view? ")
            main.view_currency(name)
        if action == "7":
            name = input("Enter the exchange you want to remove: ")
            main.remove_exchange(name)
        if action == "8":
            name = input("Enter the commodity you want to remove: ")
            main.remove_commodity(name)
        if action == "9":
            name = input("Enter the currency you want to remove: ")
            main.remove_currency(name)
        if action == "10":
            break
