from inventory import Inventory
class Item:
    def __init__(self, name, description, equipable=None, stackable=None, health=None, price=None, quantity=None, commands=None, owner=None):
        self.name = name
        self.description = description
        self.health = health
        self.price = price
        self.stackable = stackable
        self.quantity = quantity
        self.commands = commands
        self.owner = owner
        self.equipable = equipable

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    

class Container(Item):
    def __init__(self, name, description, equipable=None, stackable=None, locked=None, health=None, price=None, quantity=None, items=None, commands=None, capacity=None):
        super().__init__(name, description, equipable, stackable, health, price, quantity, commands)
        self.capacity = capacity
        self.inventory = Inventory(items=items)
        self.locked = locked
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name

    def open(self):
        if self.locked:
            print(f"The {self.name} is locked.")
            return
        if not self.inventory:
            print(f"The {self.name} is empty.")
            return
        print(f"The {self.name} contains:")
        for item in self.inventory:
            print(item)
    
    def unlock(self):
        if self.locked:
            self.locked = False
            print(f"The {self.name} has been unlocked.")
        else:
            print(f"The {self.name} is already unlocked.")

