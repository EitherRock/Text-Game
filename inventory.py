import globals

class Inventory:
    def __init__(self, items=None, capacity=None):
        self.items = items or []
        self.capacity = capacity

    def __str__(self):
        return "Inventory"
    
    def __repr__(self):
        return "Inventory"
    
    def add(self, item):
        if self.capacity is None:
            self.items.append(item)
                              
        else: 
            if len(self.items) < self.capacity:
                self.items.append(item)
            else:
                print("Inventory is full.")
    
    def remove(self, item):
        if item in self.items:
            self.items.remove(item)
            print(f"{item.name} removed from inventory.")
        else:
            print(f"{item.name} is not in inventory.")
    
    def increase_capacity(self, amount):
        self.capacity += amount
        print(f"Inventory capacity increased by {amount}.")
    
    def take(self, player, item):
        # if self.owner:
        #     print(f"You take the {self.name}.")
        #     self.owner.inventory.add(self)
        # else:
        #     print(f"You take the {self.name}.")
        if item in self.items:
            player.inventory.add(item)
            self.items.remove(item)
            return f"{item.name} added to inventory."
    
    def drop(self, item):
        if item in globals.player.inventory.items:
            self.items.append(item)
            globals.player.inventory.remove(item)
            globals.player.location.inventory.add(item)
            return f"{item.name} dropped."
        else:
            return f"{item.name} is not in inventory."
        