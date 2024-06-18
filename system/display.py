import sys
sys.path.append("../")
import globals
from collections import OrderedDict
from itertools import zip_longest
from system.command import Command

class Display:
    def __init__(self):
        pass

    def display_commands(self):
        print("Commands:")

        # # Sort the commands dictionary
        # sorted_commands = OrderedDict(sorted(globals.commands.items()))
        # for name, command in sorted_commands.items():
        #     print(f"{name}: {command.description}")
        # print("\n")
        # Sort the commands dictionary
        # Sort the commands dictionary
        sorted_commands = OrderedDict(sorted(globals.commands.items()))

        # Split the commands into two lists
        half = len(sorted_commands) // 2
        commands1 = list(sorted_commands.items())[:half]
        commands2 = list(sorted_commands.items())[half:]

        # Print the commands in two columns

        for (name1, command1), (name2, command2) in zip_longest(commands1, commands2, fillvalue=(None, Command('', ''))):
            if name1 is not None:
                name1 = name1 + ":"
                print(f"{name1:<8} {command1.description:<50}", end="")
            if name2 is not None:
                name2 = name2 + ":"
                print(f"{name2:<8} {command2.description}")
                # print()

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
    
    def display_npc_info(self, npc):
        for attr, value in vars(npc).items():
            if value is not None:
                print(f"{attr.capitalize()}: {value}")
        print("\n")