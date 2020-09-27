class Fuel:

    def __init__(self, fuel_type, fuel_name, price):
        self.fuel_type = fuel_type
        self.fuel_name = fuel_name
        self.price = price

    def __repr__(self):
        return f"{self.fuel_name} : {self.price}"
