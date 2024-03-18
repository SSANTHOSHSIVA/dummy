import csv
import pandas as pd

class Buyer:
    def __init__(self, username, tr_id_buyer, ip_address, latitude, longitude, timestamp, buyer_old_bal, pay_amt):
        self.username = username
        self.tr_id_buyer = tr_id_buyer
        self.ip_address = ip_address
        self.latitude = latitude
        self.longitude = longitude
        self.timestamp = timestamp
        self.buyer_old_bal = float(buyer_old_bal)  # Converting to float
        self.pay_amt = float(pay_amt)  # Converting to float

    def display_info(self):
        print(" ")
        print("Buyer")
        print(f" Username: {self.username}")
        print(f" Old Amount: {self.buyer_old_bal}")
        print(f" IP Address: {self.ip_address}\n")

class Shopkeeper:
    def __init__(self, name, tr_id_shop, ip_addr_shop, req_amt, latitude, longitude, shop_old_bal):
        self.name = name
        self.tr_id_shop = tr_id_shop
        self.ip_addr_shop = ip_addr_shop
        self.req_amt = float(req_amt)  # Converting to float
        self.latitude = latitude
        self.longitude = longitude
        self.shop_old_bal = float(shop_old_bal)  # Converting to float

    def display_info(self):
        print("Shopkeeper")
        print(f" Username: {self.name}")
        print(f" Old Amount: {self.shop_old_bal}")
        print(f" IP Address: {self.ip_addr_shop}\n")

class Transaction_details:
    def __init__(self, buyer, shopkeeper):
        self.buyer = buyer
        self.shopkeeper = shopkeeper

    def display(self):
        print("After Transaction")

        check_new_bal = self.buyer.buyer_old_bal - self.shopkeeper.req_amt
        check_new_sbal = self.shopkeeper.shop_old_bal + self.shopkeeper.req_amt
        check_new_bal1 = self.buyer.buyer_old_bal - self.buyer.pay_amt
        check_new_sbal1 = self.shopkeeper.shop_old_bal + self.buyer.pay_amt
        
        if check_new_sbal == check_new_sbal1 or check_new_bal == check_new_bal1:
            print("NO MONEY LOSS")
        else:
            print("MONEY LOSS")

        print("After Transaction")

        self.Buyer_new_bal = self.buyer.buyer_old_bal - self.buyer.pay_amt
        print(f"Buyer New Balance: {self.Buyer_new_bal}")

        self.Shop_new_bal = self.buyer.pay_amt + self.shopkeeper.shop_old_bal
        print(f"Shopkeeper New Balance: {self.Shop_new_bal}")

        return "NO MONEY LOSS" if check_new_sbal == check_new_sbal1 or check_new_bal == check_new_bal1 else "MONEY LOSS"

# Function to read data from CSV file and create instances of Buyer and Shopkeeper
def read_csv(filename, class_type):
    instances = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        # Skip the first row (header)
        next(reader)
        for row in reader:
            if class_type == Buyer:
                # Extracting the first 8 columns for Buyer class
                instance = class_type(*row[:8])
            elif class_type == Shopkeeper:
                # Extracting the first 7 columns for Shopkeeper class
                instance = class_type(*row[:7])
            instances.append(instance)
    return instances

# Read data from CSV files
buyer_instances = read_csv('algorithm\a__buyer.csv', Buyer)
shopkeeper_instances = read_csv('algorithm\b__shopkeeper.csv', Shopkeeper)

# Initialize count
output_count = 0

# Create a list to store transaction details
transaction_details_list = []

# Process each row individually
for buyer_instance, shopkeeper_instance in zip(buyer_instances, shopkeeper_instances):
    # Display buyer and shopkeeper information
    buyer_instance.display_info()
    shopkeeper_instance.display_info()
    
    # Process transaction details
    transaction = Transaction_details(buyer_instance, shopkeeper_instance)
    output_count += 1  # Increment count for each row processed
    transaction_status = transaction.display()
    
    # Append transaction details to the list
    transaction_details_list.append({
        'Buyer Username': buyer_instance.username,
        'Old Buyer Balance': buyer_instance.buyer_old_bal,
        'Buyer IP Address': buyer_instance.ip_address,
        'Shopkeeper Username': shopkeeper_instance.name,
        'Old Shopkeeper Balance': shopkeeper_instance.shop_old_bal,
        'Shopkeeper IP Address': shopkeeper_instance.ip_addr_shop,
        'Transaction Result': transaction_status,
        'New Buyer Balance': transaction.Buyer_new_bal,
        'New Shopkeeper Balance': transaction.Shop_new_bal
    })

# Output total count
print("Total rows processed:", output_count)

# Convert transaction details list to a DataFrame
df = pd.DataFrame(transaction_details_list)

# Save the DataFrame to an Excel file
df.to_excel('transaction_details.xlsx', index=False)

print("Transaction details saved to transaction_details.xlsx")