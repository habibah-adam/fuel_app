from fuel import Fuel


class Station:

    def __init__(self, brand, name, code, address):
        self.brand = brand
        self.name = name
        self.code = code
        self.address = address
        self.fuel_types = []

    def __repr__(self):
        return f"The Station '{self.brand}' is located:\n{self.address}\nOffers:{self.fuel_types}"

    def add_fuel_type(self, fuel):
        self.fuel_types.append(fuel)

