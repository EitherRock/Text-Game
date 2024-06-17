class Item:
    def __init__(self, name, description, health=None, price=None, quantity=None, inventory=None, commands=None):
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity
        self.inventory = inventory
        self.commands = commands