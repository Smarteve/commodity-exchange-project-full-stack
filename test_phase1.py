import unittest 
import project_phase1

class AddingCommodityTest(unittest.TestCase):
    
    def test_add_exchange(self):
        app = project_phase1.Main()
        app.add_exchange("TOMO", "Japan's largest commodity futures exchanges", "¥")
        self.assertIn("TOMO",app.exchange_dict)
        self.assertIsInstance(app.exchange_dict["TOMO"],project_phase1.Exchange)

    def test_add_commodity(self):
        app = project_phase1.Main()
      

        app.add_exchange("TOMO", "Japan's largest commodity futures exchanges", "¥")
        app.add_commodity(project_phase1.Commodity("Gold", "kg",[]))
        self.assertIn("Gold", app.commodity_dict)

    def test_remove_exchange(self):
        app = project_phase1.Main()
        app.add_exchange("TOMO", "Japan's largest commodity futures exchanges", "¥")
        app.remove_exchange("TOMO")
        self.assertNotIn("TOMO", app.exchange_dict)

    def test_remove_commodity(self):
        app = project_phase1.Main()
        app.add_exchange("TOMO", "Japan's largest commodity futures exchanges", "¥")
        app.add_commodity(project_phase1.Commodity("Gold", "kg",[]))
        app.remove_commodity("Gold")
        self.assertNotIn("Gold", app.commodity_dict)
    

if __name__ == "__main__":
    unittest.main()
