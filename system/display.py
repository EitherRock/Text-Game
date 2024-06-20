import sys
import os
sys.path.append("../")
import globals
from collections import OrderedDict
from itertools import zip_longest
from system.command import Command, util
import textwrap

class Display:
    def __init__(self):
        pass

    def display_commands(self, show_parameters=True):
        # Get the width of the terminal
        width = os.get_terminal_size().columns

        # Print the top border of the box
        print("+" + "-" * (width - 2) + "+")

        # Print the title of the box
        title = " COMMANDS "
        print("|" + title.center(width - 2) + "|")

        # Print a separator
        print("+" + "-" * (width - 2) + "+")

        # Group the commands by their tags
        player_commands = {name: command for name, command in globals.commands.items() if command.tag == 'player'}
        system_commands = {name: command for name, command in globals.commands.items() if command.tag == 'system'}
        equipped_commands = {name: command for name, command in globals.commands.items() if command.tag == 'equipped'}

        # Print the subheaders
        print("|" + " Player ".center((width - 4) // 3, " ") + "|" + " System ".center((width - 4) // 3, " ") + "|" + " Equipped ".center((width - 4) // 3, " ") + "|")

        # Print a separator
        print("+" + "-" * (width - 2) + "+")

        # Print the commands in three columns
        for (name1, command1), (name2, command2), (name3, command3) in zip_longest(player_commands.items(), system_commands.items(), equipped_commands.items(), fillvalue=(None, Command('', '', '', lambda: None))):
            row = ""
            if name1 is not None and command1 is not None:
                row += f"{name1.center((width - 4) // 3, ' ') + '|'}"
            else:
                row += " " * ((width - 4) // 3) + "|"
            
            if name2 is not None and command2 is not None:
                row += f"{name2.center((width - 4) // 3, ' ') + '|'}"
            else:
                row += " " * ((width - 4) // 3) + "|"
            if name3 is not None and command3 is not None:
                row += f"{name3.center((width - 4) // 3, ' ')}"
            else:
                row += " " * ((width - 4) // 3)
            print("|" + row + "|")

        # Print the bottom border of the box
        print("+" + "-" * (width - 2) + "+")
        print("\n")
        
    
    def always_display(self):
        width = os.get_terminal_size().columns
        print("-" * width)
        # self.display_player_info()
        # self.display_dynamic_info(self.player.location.description)
        self.display_location()
        self.display_commands()

    def display_player_info(self):
        for attr, value in vars(globals.player).items():
            if attr == "inventory":
                if value is not None:
                    value = [str(item) for item in value.items]
            if value is not None:
                print(f"{attr.capitalize()}: {value}")
    
    def display_location(self):
        print(f"Location: {globals.player.location.name}")
        print("\n")
    
    def display_location_info(self):
        for attr, value in vars(globals.player.location).items():
            if attr == "inventory":
                if value is not None:
                    value = [str(item) for item in value.items]
            if value is not None:
                print(f"{attr.capitalize()}: {value}")
    
    def display_item_info(self, item):
        for attr, value in vars(item).items():
            if attr == "inventory":
                if value is not None:
                    value = [str(item) for item in value.items]
            if value is not None:
                print(f"{attr.capitalize()}: {value}")

    def display_dynamic_info(self, info):
        print(info)
        print("\n")

    def display_combat_info(self, player, enemy):
        print(f"{player.name} health: {player.health}")
        print(f"{enemy.name} health: {enemy.health}")
        print("\n")
    
    def display_npc_info(self, npc):
        for attr, value in vars(npc).items():
            if attr == "dialogue_tree":
                continue
            if attr == "inventory":
                if value is not None:
                    value = [str(item) for item in value.items]
            if value is not None:
                print(f"{attr.capitalize()}: {value}")
    
    def display_inventory(self, inventory):
        print("Inventory:")
        for item in inventory.items:
            print(f"\t{item}")
    
    def process_command(self):
        self.always_display()
        print("\033[31mThis is red text.\033[0m")
        print("\033[32mThis is green text.\033[0m")
        command_input = input("Enter a command: ")
        if command_input != "":
            command_name, *command_args = command_input.split()

            if command_name in globals.commands:
                globals.commands[command_name](globals.player, *command_args)
            else:
                util.clear_terminal()
                print(f"Invalid command: '{command_name}',\nTry again.")
        else:
            util.clear_terminal()
            print("Please enter a command.")

