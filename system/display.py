import sys
sys.path.append("../")
import globals
from collections import OrderedDict

class Display:
    def __init__(self):
        pass

    def display_commands(self):
        print("Commands:")

        # Sort the commands dictionary
        sorted_commands = OrderedDict(sorted(globals.commands.items()))
        for name, command in sorted_commands.items():
            print(f"{name}: {command.description}")
        print("\n")
    
    def always_display(self):
        print("+--------------------------------------+")
        # self.display_player_info()
        # self.display_dynamic_info(self.player.location.description)
        self.display_location()
        self.display_commands()

    def display_player_info(self):
        print(f"Player name: {globals.player.name}")
        print(f"health: {globals.player.health}")
        print("\n")
    
    def display_location(self):
        print(f"Location: {globals.player.location['name']}")
        print("\n")
    
    def display_location_info(self):
        print(f"Location: {globals.player.location['name']}")
        print(f"Description: {globals.player.location['description']}")
        print("\n")

    def display_dynamic_info(self, info):
        print(info)
        print("\n")

    def display_combat_info(self, player, enemy):
        print(f"{player.name} health: {player.health}")
        print(f"{enemy.name} health: {enemy.health}")
        print("\n")