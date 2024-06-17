class Location:
    def __init__(self, name, description, items, enemies, commands, connected_locations):
        self.name = name
        self.description = description
        self.inventory = items
        self.enemies = enemies
        self.commands = commands
        self.connected_locations = connected_locations