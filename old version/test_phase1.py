import unittest
from datetime import date
from project_phase1 import Main, Exchange, Commodity, Currency


class AddingCommodityTest(unittest.TestCase):
    def setUp(self):
        self.main = Main()
        self.exchange = Exchange("TestExchange", "A test exchange", "$")
        self.commodity = Commodity("Gold", "ounces", [])
        self.currency = Currency("USD", [], "spot", [date.today()], "2 years")

    def test_add_exchange(self):
        self.main.add_exchange("TestExchange", "A test exchange", "$")
        self.assertIn("TestExchange", self.main.exchange_dict)
        self.assertIsInstance(self.main.exchange_dict["TestExchange"], Exchange)

    def test_add_commodity(self):
        self.main.add_commodity(self.commodity)
        self.assertIn("Gold", self.main.commodity_dict)

    def test_add_currency(self):
        self.main.add_currency(self.currency)
        self.assertIn("USD", self.main.currency_dict)

    def test_remove_currency(self):
        self.main.add_currency(self.currency)
        self.main.remove_currency("USD")
        self.assertNotIn("USD", self.main.currency_dict)

    def test_remove_exchange(self):
        self.main.add_exchange("TestExchange", "A test exchange", "$")
        self.main.remove_exchange("TestExchange")
        self.assertNotIn("TestExchange", self.main.exchange_dict)

    def test_remove_commodity(self):
        self.main.add_commodity(self.commodity)
        self.main.remove_commodity("Gold")
        self.assertNotIn("Gold", self.main.commodity_dict)


if __name__ == "__main__":
    unittest.main()
