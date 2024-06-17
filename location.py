class Location:
    def __init__(self, name, description, items=None, enemies=None, npcs=None, commands=None, connected_locations=None):
        self.name = name
        self.description = description
        self.inventory = items
        self.enemies = enemies
        self.npcs = npcs
        self.commands = commands
        self.connected_locations = connected_locations


class ShopLocation(Location):
    def __init__(self, name, description, items=None, enemies=None, npcs=None, commands=None, connected_locations=None):
        super().__init__(name, description, items, enemies, npcs, commands, connected_locations)
        self.inventory = items

    def display_inventory(self):
        print("Available items in the shop:")
        for item in self.inventory:
            print(item)