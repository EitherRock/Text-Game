import random
from inventory import Inventory

class Location:
    def __init__(self, name, description, items=None, enemies=None, npcs=None, commands=None, connected_locations=None):
        self.name = name
        self.description = description
        self.inventory = Inventory(items=items)
        self.enemies = enemies
        self.npcs = npcs
        self.times_visited = 0
        self.commands = commands
        self.connected_locations = connected_locations
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def enemy_encounter(self):
        # Check for enemy encounters
        if self.enemies:
            if random.random() < 0.5:  # 50% chance of an enemy encounter
                enemy = random.choice(self.enemies)
                print(f"You encounter a {enemy.name}!")
                enemy.fight()

                
        return None


class ShopLocation(Location):
    def __init__(self, name, description, items=None, enemies=None, npcs=None, commands=None, connected_locations=None):
        super().__init__(name, description, items, enemies, npcs, commands, connected_locations)
        self.inventory = items

    def display_inventory(self):
        print("Available items in the shop:")
        for item in self.inventory:
            print(item)