import unittest 
from unittest.mock import patch 
from main_module import Exchange,Commodity,add_commodity

class AddingCommodityTest(unittest.TestCase):
    def setUp(self): 
        global exchange_dict,commodity_dict
        exchange_dict = {"TOMO": Exchange("TOMO", "Japan's largest exchange", "¥")}
        commodity_dict = {}

    def test_commodity_exists(self):
        commodity_dict["gold"] = Commodity("gold","ounce")
        self.assertTrue(_commodity_exist("gold"))
        self.assertFalse(_commodity_exist("silver"))
    
    def test_missing_exchange_list(self):
        self.assertEqual(_missing_exchanges_list(["TOMO"]),[])
        self.assertEqual(_missing_exchanges_list(["TOMO","NYSE"]),["NYSE"])

    @patch('builtins.input',side_effect = ["2023-10-01", "1500"])
    def test_add_commodity_to_system(self,mock_input):
        _add_commodity_to_system("gold","ounce",["TOMO"])
        self.assertIn("gold",commodity_dict)
        self.assertIn("gold",exchange_dict["TOMO"].commodities)


if __name__ == "__main__":
    unittest.main()