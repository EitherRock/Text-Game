class Item:
    def __init__(self, name, searchable, description, price=None, quantity=None, commands=None):
        self.name = name
        self.searchable = searchable
        self.description = description
        self.price = price
        self.quantity = quantity
        self.commands = commands