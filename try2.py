from datetime import datetime

class ParcelPriceTable:
    def __init__(self):
        self.prices = {}

    def add_price(self, zone, weight_range, price):
        self.prices[(zone, weight_range)] = price

    def modify_price(self, zone, weight_range, new_price):
        if (zone, weight_range) in self.prices and weight_range[1] > 3:
            self.prices[(zone, weight_range)] = new_price

    def delete_price(self, zone, weight_range):
        if (zone, weight_range) in self.prices and weight_range[1] > 3:
            del self.prices[(zone, weight_range)]

    def get_price(self, zone, weight):
        for (z, weight_range), price in self.prices.items():
            if z == zone and weight_range[0] <= weight <= weight_range[1]:
                return price
        return None

    def view_all_prices(self):
        return self.prices

class Parcel:
    parcel_counter = 10000000

    def __init__(self, receiver_name, address, telephone, zone, weight, price_table):
        self.parcel_number = f'P{Parcel.parcel_counter}'
        Parcel.parcel_counter += 1
        self.receiver_name = receiver_name
        self.address = address
        self.telephone = telephone
        self.zone = zone
        self.weight = weight
        self.price_table = price_table
        self.price = self.calculate_price()

    def calculate_price(self):
        price = self.price_table.get_price(self.zone, self.weight)
        if price is not None:
            return price
        else:
            raise ValueError("Price not found for the given zone and weight.")

    def display_info(self):
        return f"Parcel Number: {self.parcel_number}, Receiver: {self.receiver_name}, " \
               f"Address: {self.address}, Telephone: {self.telephone}, " \
               f"Zone: {self.zone}, Weight: {self.weight} kg, Price: RM{self.price:.2f}"

class Consignment:
    consignment_counter = 10000000

    def __init__(self, customer_name, customer_address, customer_telephone):
        self.consignment_number = Consignment.generate_consignment_number()
        self.date = datetime.now().strftime("%d/%m/%Y")
        self.customer_name = customer_name
        self.customer_address = customer_address
        self.customer_telephone = customer_telephone
        self.parcel_list = []

    @staticmethod
    def generate_consignment_number():
        Consignment.consignment_counter += 1
        return Consignment.consignment_counter

    def add_parcel(self, parcel):
        self.parcel_list.append(parcel)

    def calculate_total_price(self):
        total_price = sum(parcel.price for parcel in self.parcel_list)
        return total_price + (0.08 * total_price)

    def display_info(self):
        consignment_info = f"Consignment Number: {self.consignment_number}\n" \
                           f"Date: {self.date}\n" \
                           f"Customer: {self.customer_name}, Address: {self.customer_address}, " \
                           f"Telephone: {self.customer_telephone}\n"
        parcel_info = "\n".join(parcel.display_info() for parcel in self.parcel_list)
        total_price = self.calculate_total_price()
        return consignment_info + parcel_info + f"\nTotal Price (including 8% service tax): RM{total_price:.2f}"

class Administrator:
    def __init__(self, price_table):
        self.price_table = price_table

    def add_price(self, zone, weight_range, price):
        self.price_table.add_price(zone, weight_range, price)

    def add_price_above_3kg(self, zone):
        price_list = [35.00, 40.00, 45.00, 50.00, 55.00]
        for i, price in enumerate(price_list, start=1):
            weight_range = (3 + i, 3 + i + 1)
            self.price_table.add_price(zone, weight_range, price)

    def modify_price(self, zone, weight_range, new_price):
        self.price_table.modify_price(zone, weight_range, new_price)

    def delete_price(self, zone, weight_range):
        self.price_table.delete_price(zone, weight_range)

    def check_price(self, zone, weight):
        return self.price_table.get_price(zone, weight)

    def view_all_prices(self):
        return self.price_table.view_all_prices()

def main():
    price_table = ParcelPriceTable()
    administrator = Administrator(price_table)

    while True:
        print("\nAdministrator Menu:")
        print("1. Add price for parcels in Table 1")
        print("2. Add price for parcels more than 3kg")
        print("3. Modify price (more than 3kg)")
        print("4. Delete price (more than 3kg)")
        print("5. Check the price of a parcel")
        print("6. View all prices")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            zone = input("Enter zone: ")
            weight_range = tuple(map(float, input("Enter weight range (e.g., 0 1): ").split()))
            price = float(input("Enter price: "))
            administrator.add_price(zone, weight_range, price)
            print("Price added successfully!")
        elif choice == '2':
            zone = input("Enter zone: ")
            administrator.add_price_above_3kg(zone)
            print("Prices added successfully!")
        elif choice == '3':
            zone = input("Enter zone: ")
            weight_range = tuple(map(float, input("Enter weight range (e.g., 4 inf): ").split()))
            new_price = float(input("Enter new price: "))
            administrator.modify_price(zone, weight_range, new_price)
            print("Price modified successfully!")
        elif choice == '4':
            zone = input("Enter zone: ")
            weight_range = tuple(map(float, input("Enter weight range (e.g., 4 inf): ").split()))
            administrator.delete_price(zone, weight_range)
            print("Price deleted successfully!")
        elif choice == '5':
            zone = input("Enter zone: ")
            weight = float(input("Enter weight: "))
            result = administrator.check_price(zone, weight)
            if result is not None:
                print("Price:", result)
            else:
                print("Price not found for the given zone and weight.")
        elif choice == '6':
            print("All Prices:")
            print(administrator.view_all_prices())
        elif choice == '7':
            print("Exiting the Administrator Menu.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
