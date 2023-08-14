'''
four main dictionaries to store data
1 exchange_dict = {} main exchange dict with key exchange name, value exchange object 
2 commodity_dict= {} main commodity dict with key commodity name, value commodity object
3 self.exchanges under Commodity class,  self.commodities under Exchange class for reference to each other.
when delete exchange and commodity needs to delete both main dict and reference dict.
4 price object is stored in self.price under Commodity class as a child-parent relationship 

'''


from datetime import datetime
exchange_dict = {} # key exchange name, value exchange object 
commodity_dict= {} # key commodity name, value commodity object

class Exchange:
    def __init__(self,name,description):
        self.name = name
        self.description = description
        self.commodities = {}   # put self.commodities as a dictionary, key is commodity name, value commodity object
  
    def __str__(self):
        if self.commodities: # when add exchange, only requires administrator to add name and intro first, if no commodities at first then dont display
            return f"{self.name} is {self.description}."\
            f"The list of the commodities currently trading in {self.name} is {','.join(self.commodities.keys())}."
        else:
            return f"{self.name} is {self.description}."

class Commodity:
    def __init__(self,name,unit):
        self.name = name 
        self.unit = unit  
        self.exchanges = {} # key exchange name, value exchange object 
        self.price = {} # key exchange name, value price object 
       

    def __str__(self):
        price_strings = [str(price_instance) for price_instance in self.price.values()]
        last_traded = max(self.price.values(), key = lambda price: price.time)
        return f"{self.name} is traded at {','.join(self.exchanges.keys())}.\n"\
        f"It is last traded at {str(last_traded)} per {self.unit}.\n"\
        f"The full trading info is {','.join(price_strings)}."

    
class Price:
    def __init__(self,commodity,exchange,time,value):
        self.commodity = commodity 
        self.exchange = exchange
        self.time = time
        self.value = value
                            
    def __str__(self):
        return f"{self.value} at {self.exchange} at {self.time}"

def parse_time(time):
    time_object = datetime.strptime(time,"%Y-%m-%d")
    return time_object

def add_exchange(name,description):
    if name in exchange_dict:
        print("exchange already existed, add a new exchange")
        return
    else:
        new_exchange = Exchange(name,description)
        exchange_dict[name] = new_exchange

def add_commodity():
    while True:
            commodity_name = input("What is the name of the commodity you want to add? ")
            if commodity_name in commodity_dict:
                print(f"{commodity_name} already existed, pls enter a new commodity")
            else:
                break        
    unit = input("What is the unit of the commodity? ")
    commodity_instance = Commodity(commodity_name,unit)
    exchange_name = input(f"what is the exchange {commodity_name} is traded at(comma separated if multiple): ")
    missing_exchanges = []
    exchange_list = exchange_name.split(",")
    for item in exchange_list:
            if item not in exchange_dict:
                missing_exchanges.append(item)
    if missing_exchanges:
        print(f"{','.join(missing_exchanges)} not in exchange system, pls add exchange first")
        return
    for item in exchange_list:       
        commodity_instance.exchanges[item] = exchange_dict[item]
        time = input(f"Enter the last traded time in {item}(yyyy-mm-dd): ")
        formatted_time = parse_time(time)
        price = float(input(f"Enter the price of last trade in {item}: "))
        price_instance = Price(commodity_name,item,formatted_time,price)
        commodity_instance.price[item] = price_instance #update self.price dictionary under Commodity class
        exchange_dict[item].commodities[commodity_name] = commodity_instance # update self.commodities under Exchange class
        commodity_dict[commodity_name] = commodity_instance # update main commodity dic
    print(f"Thanks for adding {commodity_name}")

def view_exchange(name):
    print(exchange_dict[name]) if name in exchange_dict else print(f"{name} does not exist")

def view_commodity(name): 
    print(commodity_dict[name]) if name in commodity_dict else print('commodity not found')
    # list comprehension 
    # get commodity object from commodity_dict 

def remove_exchange(name):
    # delete two things, delete from exchange main dic, and self.exchange dict from Commodity class
    if name in exchange_dict:
        del exchange_dict[name]
        for commodity_obj in commodity_dict.values():
            if name in commodity_obj.exchanges:
                del commodity_obj.exchanges[name]
        print(f"{name} has been removed from exchanges")
    else:
        print("exchange not found")

def remove_commodity(name): 
    # delete two things, the main commodity dict, and self.commodity dict from Exchange class 
    if name in commodity_dict:
        del commodity_dict[name]
        for exchange_instance in exchange_dict.values():
            if name in exchange_instance.commodities:
                del exchange_instance.commodities[name]
        print(f"{name} has been removed from commodities")
    else:
        print("commodity not found")



add_exchange("TOMO","Japan's largest commodity futures exchanges")
print("Welcome user")
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
        add_exchange(exchange_name,description)
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



      


         
    
