import random
from inventory import Inventory
from combat import Combat
import globals as globals

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
                encounter_enemies = []  # List of enemies for the encounter

                for enemy_name in self.enemies:
                    enemy = globals.npcs.get(enemy_name)  # Look up the NPC object by name
                    if enemy is not None:
                        encounter_enemies.append(enemy)
                    else:
                        print(f"Error: NPC '{enemy_name}' not found.")
            
                if encounter_enemies:
                    num_enemies = len(encounter_enemies)
                    print(f"You encounter {num_enemies} enemies!")
                    globals.game_display.process_player_input(continue_text=True)
                    globals.combat = Combat(globals.player, encounter_enemies)
                    globals.combat.start()

                    # Reset the break_loop flag
                    globals.break_loop = False

        return None


class ShopLocation(Location):
    def __init__(self, name, description, items=None, enemies=None, npcs=None, commands=None, connected_locations=None):
        super().__init__(name, description, items, enemies, npcs, commands, connected_locations)
        self.inventory = items

    def display_inventory(self):
        print("Available items in the shop:")
        for item in self.inventory:
            print(item)