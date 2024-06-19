from system.logger import Logger
from system.util import clear_terminal
import globals as globals
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
        self.inventory = []
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

    def search(self, player, *args, **kwargs):
        # TODO: Implement search logic, add extra parameters if searching storage, npcs, etc.
        searchable_items = [item for item in player.location.inventory if item['searchable']]
        
        if len(searchable_items) == 0:
            clear_terminal()
            print("There are no items to search for in this location.")
            return
        
        # Use a randomizer to determine if the search is successful
        if random.random() < 0.5:  # 50% chance of success
            clear_terminal()
            print("Your search was unsuccessful.")
            return

        # Randomly pick an item from the searchable items
        item = random.choice(searchable_items)
        self.inventory.append(item)
        clear_terminal()
        print(f"You found a {item['name']}!")
        globals.log.log(f"{player.name} found a {item['name']}!")
    
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
            # Display general information
            print(f"Name: {self.name}, Health: {self.health}, Stamina: {self.stamina}")
            if self.mana:
                print(f"Mana: {self.mana}")
    def fly(self):
        print("You fly")

    def __str__(self):
        string = f"Name: {self.name}, Health: {self.health}, Stamina: {self.stamina}"
        if self.mana:
            string += f", Mana: {self.mana}"
        return f"Name: {self.name}, Health: {self.health}, Stamina: {self.stamina}, Mana: {self.mana}"
    
    
