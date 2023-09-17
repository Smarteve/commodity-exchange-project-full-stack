

from datetime import datetime,date
exchange_dict = {} # key exchange name, value exchange object 
commodity_dict= {} # key commodity name, value commodity object

class Exchange:
    def __init__(self,name,description,currency_sign):
        self.name = name
        self.description = description
        self.currency_sign = currency_sign
        self.commodities = [] # a list of commodity names
        
  
    def __str__(self):
        if self.commodities: # when add exchange, only requires administrator to add name and intro first, if no commodities at first then dont display
            return f"{self.name} is {self.description}."\
            f"The list of the commodities currently trading in {self.name} is {','.join(self.commodities)}."
        else:
            return f"{self.name} is {self.description}."

class Commodity:
    def __init__(self,name,unit):
        self.name = name 
        self.unit = unit  
        self.exchanges = [] # a list of exchange names
        self.price = {} # key price object, value exchange name    

    def __str__(self):
        all_prices = list(self.price.keys())
        last_traded_price = max(all_prices, key = lambda price: price.time)
        last_traded_exchange = self.price[last_traded_price]
        currency_sign = exchange_dict[last_traded_exchange].currency_sign
        info = []
        info.append(f"{self.name} is traded at {','.join(self.exchanges)}.")
        info.append(f"It is last traded at {currency_sign}{last_traded_price.value} in {last_traded_exchange} per {self.unit}.")
        info.append(f"The full trading info is:")
        for price in all_prices:
            info.append(str(price))
        return "\n".join(info)
    
class Price:
    def __init__(self,commodity,exchange,time,value):
        self.commodity = commodity 
        self.exchange = exchange
        self.time = time
        self.value = value
       
    def __str__(self):
        currency_sign = exchange_dict[self.exchange].currency_sign
        return f"{currency_sign}{self.value} at {self.exchange} at {self.time}"

    
def parse_time(time):
    time_object = datetime.strptime(time,"%Y-%m-%d")
    return time_object.date()  # print only date

def add_exchange(name,description,currency_sign):
    if name in exchange_dict:
        print("exchange already existed, add a new exchange")
        return
    else:
        new_exchange = Exchange(name,description,currency_sign)
        exchange_dict[name] = new_exchange

def add_commodity():
    commodity_name = input("What is the name of the commodity you want to add? ")
    #check if commodity exist
    if commodity_name in commodity_dict:
        print(f"{commodity_name} already existed, pls enter a new commodity")
        return    
    unit = input("What is the unit of the commodity? ")
    new_commodity = Commodity(commodity_name,unit)
    # check if all exchanges are added first
    exchange_name = input(f"what is the exchange {commodity_name} is traded at(comma separated if multiple): ")
    missing_exchanges = []
    exchange_list = exchange_name.split(",")
    for exchange in exchange_list:
            if exchange not in exchange_dict:
                missing_exchanges.append(exchange)
    if missing_exchanges:
        print(f"{','.join(missing_exchanges)} not in exchange system, pls add exchange first")
        return
    # add exchange, price
    for exchange in exchange_list:       
        new_commodity.exchanges.append(exchange)
        time = input(f"Enter the last traded time in {exchange}(yyyy-mm-dd): ")
        formatted_time = parse_time(time)
        price = float(input(f"Enter the price of last trade in {exchange}: "))
        new_price = Price(commodity_name,exchange,formatted_time,price)
        new_commodity.price[new_price] = exchange #update self.price dictionary under Commodity class
        exchange_dict[exchange].commodities.append(commodity_name)# update self.commodities under Exchange class
    commodity_dict[commodity_name] = new_commodity # update main commodity dic
    print(f"Thanks for adding {commodity_name}")

def view_exchange(name):
    print(exchange_dict[name]) if name in exchange_dict else print(f"{name} does not exist")

def view_commodity(name): 
    print(commodity_dict[name]) if name in commodity_dict else print('commodity not found')

def remove_exchange(name):
    #delete from exchange main dic 
    if name in exchange_dict:
        del exchange_dict[name]
        print(f"{name} has been removed from exchanges")
    else:
        print("exchange not found")

def remove_commodity(name): 
    # delete from the main commodity dict 
    if name in commodity_dict:
        del commodity_dict[name]
        print(f"{name} has been removed from commodities")
    else:
        print("commodity not found")



add_exchange("TOMO","Japan's largest commodity futures exchanges","¥")
print("Welcome, treasure hunters")
while True:
    print("-----")
    print("choose your action: ")
    print("1 Add an exchange")
    print("2 Add a commodity") 
    print("3 View an exchange")
    print("4 View an commodity")
    print("5 Remove an exchange")
    print("6 Remove a commodity")
    print("7 Exit")
    print("-----")
    action = input("please choose a number: ")
    if action == "1":
        exchange_name = input("What's the name of the exchange you want to add? ")
        description= input(f"What's the descripition of the exchange? {exchange_name} is: ")
        currency_sign =  input(f"what's the primary currency of the exchange? choose from ¥,$,£ and yuan: ")
        add_exchange(exchange_name,description,currency_sign)
        print(f"Thanks for adding {exchange_name}")

    if action == "2":
        add_commodity()

    if action == "3":
        commodity_name = input("Which exchange do you want to view? ")
        view_exchange(commodity_name)
    if action == "4":
        commodity_name = input("Which commodity do you want to view? ")
        view_commodity(commodity_name)
    if action == "5":
        commodity_name = input("Enter the exchange you want to remove: ")
        remove_exchange(commodity_name)
    if action == "6":
        commodity_name = input("Enter the commodity you want to remove: ")
        remove_commodity(commodity_name)
    if action == "7":
        break 




      


         
    
