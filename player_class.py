from system.logger import Logger
from system.util import clear_terminal
import globals as globals
from inventory import Inventory
from item import Container
import random

class Player:
    def __init__(self, name, max_health, max_stamina, xp=0, mana=None):
        self.name = name
        self.max_health = max_health
        self.health = self.max_health
        self.max_stamina = max_stamina
        self.stamina = self.max_stamina
        self.mana = mana
        self.experience = xp
        self.location = None
        self.previous_location = None
        self.inventory = Inventory(capacity=5)
        self.equpped_items = []
        self.days = 0
        self.statuses = ["Alive", "Full Stamina", "Full Health"]
        self.quest_log = []

    def travel(self, player, *args, **kwargs):
        if len(args) == 0:
            clear_terminal()
            print("You must specify a location to travel to.")
            return
        
        fly = False
        if 'fly' in args:
            fly = True
            print("You fly")
        
        self.previous_location = self.location
        location = args[0]
        if location not in globals.locations:
            clear_terminal()
            print("The location you entered does not exist.")
            return
        
        if fly:
            self.location = globals.locations[location]
            clear_terminal()
            print(f"{self.name} flew from {self.previous_location.name} to {self.location.name}")
            globals.log.log(f"{self.name} flew from {self.previous_location.name} to {self.location.name}")

            self.location.enemy_encounter()
                
        elif location not in self.location.connected_locations:
            clear_terminal()
            print(f"You cannot travel to {location} from {self.location.name}.")
            return
        else:
            self.location = globals.locations[location]
            clear_terminal()
            print(f"{self.name} traveled from {self.previous_location.name} to {self.location.name}")
            globals.log.log(f"{self.name} traveled from {self.previous_location.name} to {self.location.name}")

        # Remove the commands of the previous location
        if self.previous_location.npcs:
            del globals.commands['talk']

        if self.previous_location is not None:
            if self.previous_location.commands:
                for command in self.previous_location.commands:
                    del globals.commands[command]
        
        # Add the commands of the new location
        if self.location.npcs:
            globals.commands['talk'] = globals.all_commands['talk']

        if self.location.commands:
            for command in self.location.commands:
                if command not in globals.commands:
                    globals.commands[command] = globals.all_commands[command]
        
    
    def buy(self, shop):
            # Check if the shop has any items in its inventory
            if len(shop.inventory) == 0:
                print("The shop is currently out of stock.")
                return

            # Display the available items in the shop
            print("Available items in the shop:")
            for item in shop.inventory:
                print(item)

            # Prompt the player to select an item to buy
            item_name = input("Enter the name of the item you want to buy: ")

            # Find the selected item in the shop's inventory
            selected_item = None
            for item in shop.inventory:
                if item.name == item_name:
                    selected_item = item
                    break

            # Check if the selected item exists in the shop's inventory
            if selected_item is None:
                print("The selected item is not available in the shop.")
                return

            # Check if the player has enough gold to buy the item
            if self.gold < selected_item.price:
                print("You don't have enough gold to buy this item.")
                return

            # Deduct the item price from the player's gold
            self.gold -= selected_item.price

            # Add the item to the player's inventory
            self.inventory.append(selected_item)

            print(f"You bought {selected_item.name}.")

    def sell(self, item):
        # Code for selling an item
        pass

    def level_up(self):
        # Increase player's level
        self.level += 1

        # Increase player's health, stamina, and mana
        self.health += 10
        self.stamina += 5
        if self.mana:
            self.mana += 5

        # Print level up message
        print(f"{self.name} leveled up! New level: {self.level}")

    def quest(self, quest_name):
        # Code for starting a quest
        pass

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def remove_from_inventory(self, item):
        self.inventory.remove(item)

    def show_inventory(self):
        print(f"{self.name}'s Inventory:")
        for item in self.inventory:
            print(item)
    
    def quit(self, player):
        clear_terminal()
        print(f"Goodbye, {self.name}!")
        exit()
    
    def log(self, player):
        globals.log.display()

    def location_info(self, player):
        clear_terminal()
        globals.game_display.display_location_info()

    def search(self, player, target=None):
        def perform_search(target):
            globals.inventory = target.inventory
            if 'take' not in globals.commands:
                globals.commands['take'] = globals.all_commands['take']
            if 'back' not in globals.commands:
                globals.commands['back'] = globals.all_commands['back']
            if 'travel' in globals.commands:
                del globals.commands['travel']

            # Process commands until the user enters the 'back' command
            while True:
                print(f"You search the {target.name}...")
                globals.game_display.display_inventory(target.inventory)
                globals.game_display.process_command()
                if globals.break_loop:
                    break

            # Remove the 'take' and 'back' commands after the loop breaks
            if 'take' in globals.commands:
                del globals.commands['take']
            if 'back' in globals.commands:
                del globals.commands['back']
            if 'travel' not in globals.commands:
                globals.commands['travel'] = globals.all_commands['travel']

            # Reset the break_loop flag
            globals.break_loop = False

        if target is None:
            command = globals.commands.get('search')
            if command:
                clear_terminal()
                print(f"Command: {command.name}")
                print(f"Definition: {command.description}")

                # Create variables for NPCs, items, and locations
                npc_names = '\n\t'.join([npc.name for npc in self.location.npcs]) if self.location.npcs else None
                container_items = '\n\t'.join([item.name for item in self.location.inventory.items if isinstance(item, Container)]) if self.location.inventory.items else None
                location_name = self.location.name if self.location.name else None

                # Build a string to display
                search_options = "\nSearch Options:"
                if location_name:
                    search_options += f"\n\t{location_name}"
                if npc_names:
                    search_options += f"\n\t{npc_names}"
                if container_items:
                    search_options += f"\n\t{container_items}"

                print(f'{search_options}\n')
                
        elif target == self.location.name:
            clear_terminal()
            perform_search(self.location)
        elif target in [npc.name for npc in self.location.npcs]:
            # Search the NPC
            clear_terminal()
            npc = next(npc for npc in self.location.npcs if npc.name == target)
            perform_search(npc)
        elif target in [item.name for item in self.location.inventory.items if isinstance(item, Container)]:
            # Search the container
            clear_terminal()
            container = next(item for item in self.location.inventory.items if item.name == target)
            perform_search(container)
        else:
            clear_terminal()
            print(f"No location, NPC, or container named '{target}' found at this location.")
    
    def sleep(self, player):
        # Rest and recover health and stamina
        clear_terminal()
        player.health = player.max_health
        player.stamina = player.max_stamina
        player.days += 1
        print(f"{player.name} rested and recovered health and stamina.")
        globals.log.log(f"{player.name} rested and recovered health and stamina.")
    
    def info(self, player, *args, **kwargs):
        clear_terminal()
        if args:
            if args[0] == "player":
                globals.game_display.display_player_info()
            elif args[0] == "location":
                globals.game_display.display_location_info()
            elif args[0] == "npc":
                if len(args) < 2:
                    clear_terminal()
                    print("You must specify an NPC to display information.")
                    return
                npc_name = args[1].lower()
                npc = globals.npcs[npc_name]
                location = globals.locations[player.location.name]
                npc = next((npc for npc in location.npcs if npc.name.lower() == npc_name), None)
                if npc is not None:
                    globals.game_display.display_npc_info(npc)
                else:
                    print(f"No NPC named {npc_name} found at this location.")
            else:
                print(f"Invalid argument: {args[0]}")
        else:
            # Display info command, it's description, and possible arguments
            print("Command: Info")
            print("Definition: Display player and location info")
            
    def fly(self):
        print("You fly")
    
    def back(self):
        clear_terminal()
        globals.break_loop = True
 
    def __str__(self):
        string = f"Name: {self.name}, Health: {self.health}, Stamina: {self.stamina}"
        if self.mana:
            string += f", Mana: {self.mana}"
        return f"Name: {self.name}, Health: {self.health}, Stamina: {self.stamina}, Mana: {self.mana}"
    
    
