import csv

class ParcelPricingSystem:
    def __init__(self):
        self.parcel_table = {}
        self.filename = "parcel_prices.csv"
        self.load_data_from_file()

    def load_data_from_file(self):
        try:
            with open(self.filename, 'r', newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    weight, destination, price = map(float, row)
                    key = (weight, destination)
                    self.parcel_table[key] = price
        except FileNotFoundError:
            print(f"No data file found. Starting with an empty table.")

    def save_data_to_file(self):
        with open(self.filename, 'w', newline='') as file:
            writer = csv.writer(file)
            for key, value in self.parcel_table.items():
                weight, destination = key
                writer.writerow([weight, destination, value])

    def add_price(self):
        weight = float(input("Enter the weight of the parcel (in kg): "))
        destination = input("Enter the destination: ")
        price = float(input("Enter the price of the parcel: "))

        if weight > 3:
            key = (weight, destination)
            self.parcel_table[key] = price
            print(f"Price for {weight}kg parcel to {destination} added successfully.")
            self.save_data_to_file()
        else:
            print("Invalid weight. Price can only be added for parcels weighing more than 3kg.")

    def modify_price(self):
        weight = float(input("Enter the weight of the parcel (in kg): "))
        destination = input("Enter the destination: ")
        new_price = float(input("Enter the new price of the parcel: "))

        key = (weight, destination)
        if key in self.parcel_table and weight > 3:
            self.parcel_table[key] = new_price
            print(f"Price for {weight}kg parcel to {destination} modified successfully.")
            self.save_data_to_file()
        else:
            print("Invalid modification request.")

    def delete_price(self):
        weight = float(input("Enter the weight of the parcel (in kg): "))
        destination = input("Enter the destination: ")

        key = (weight, destination)
        if key in self.parcel_table and weight > 3:
            del self.parcel_table[key]
            print(f"Price for {weight}kg parcel to {destination} deleted successfully.")
            self.save_data_to_file()
        else:
            print("Invalid deletion request.")

    def check_price(self):
        weight = float(input("Enter the weight of the parcel (in kg): "))
        destination = input("Enter the destination: ")

        key = (weight, destination)
        if key in self.parcel_table:
            return self.parcel_table[key]
        else:
            return "Price not found for the given weight and destination."

    def view_all_prices(self):
        print("All Prices:")
        for key, value in self.parcel_table.items():
            weight, destination = key
            print(f"Weight: {weight}kg, Destination: {destination}, Price: {value}")


# Example usage:
system = ParcelPricingSystem()

while True:
    print("\nOptions:")
    print("1. Add price")
    print("2. Modify price")
    print("3. Delete price")
    print("4. Check price")
    print("5. View all prices")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        system.add_price()

    elif choice == "2":
        system.modify_price()

    elif choice == "3":
        system.delete_price()

    elif choice == "4":
        price = system.check_price()
        print(f"Price: {price}")

    elif choice == "5":
        system.view_all_prices()

    elif choice == "6":
        print("Exiting the program.")
        break

    else:
        print("Invalid choice. Please enter a number between 1 and 6.")