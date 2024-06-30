import globals
from system import util

class Command:
    def __init__(self, name, description, tag, func):
        self.name = name
        self.description = description
        self.tag = tag
        self.func = func
        
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def execute(self, player, command_args):
        pass

    def current_command_params(self):
        return self.name

class TravelCommand(Command):
    def __init__(self, tag, player):
        super().__init__("Travel", "Travel to a different location", tag, player.travel)
    def execute(self, command_args):
        self.func(self.player, *command_args)
    
    def current_command_params(self):
        return ', '.join(globals.player.location.connected_locations)
        

class FightCommand(Command):
    def __init__(self, tag,):
        super().__init__("Fight", "Fight an enemy", tag, self.execute)
    def execute(self, player, command_args):
        player.fight(command_args)

class QuitCommand(Command):
    def __init__(self, tag, player):
        super().__init__("Quit", "Quit the game", tag, player.quit)
    def execute(self, player):
        player.quit()

class LogCommand(Command):
    def __init__(self, tag, player):
        super().__init__("Log", "Display the log of events", tag, player.log)
    def execute(self, player):
        player.log()

class SearchCommand(Command):
    def __init__(self, tag, player):
        super().__init__("Search", "Search your current location, an npc or a container", tag, player.search)
    def execute(self, player, command_args):
        player.search(command_args)

class SleepCommand(Command):
    def __init__(self, tag, player):
        super().__init__("Sleep", "Rest and recover health and stamina", tag, player.sleep)
    def execute(self, player):
        player.sleep()

class InfoCommand(Command):
    def __init__(self, tag, player):
        super().__init__("Info", "Display player and location info", tag, player.info)
    def execute(self, player, *args, **kwargs):
        self.func(player, *args, **kwargs)
    
    def current_command_params(self):
        return "player, location, npc"

class TalkCommand(Command):
    def __init__(self, tag):
        super().__init__("Talk", "Talk to an NPC", tag, self.execute)
    def execute(self, player, *args, **kwargs):
        if not args:
            util.clear_terminal()
            # Display command name and definition
            print(f"Command: {self.name}")
            print(f"Definition: {self.description}")

            # Display NPCs in the current location
            if player.location.name in globals.locations:
                location = globals.locations[player.location.name]
                npc_names = '\n\t'.join([npc.name for npc in location.npcs]) if location.npcs else None
                if npc_names:
                    print("\nNPCs in this location:")
                    print(f"\t{npc_names}")
                else:
                    print("No NPCs in this location.")
            return
        npc_name = args[0]
        if player.location.name in globals.locations:
            location = globals.locations[player.location.name]
            npc = next((npc for npc in location.npcs if npc.name == npc_name), None)
            if npc is not None:
                util.clear_terminal()
                npc.talk('start')
            else:
                util.clear_terminal()
                print(f"No NPC named {npc_name} found.")
        else:
            util.clear_terminal()
            print("No NPCs in this location.")
    
    def current_command_params(self):
        return ', '.join([str(npc) for npc in globals.player.location.npcs])

class TakeCommand(Command):
    def __init__(self, tag):
        super().__init__("Take", "Take an item", tag, self.execute)
    def execute(self, player, *args, **kwargs):
        if not args:
            util.clear_terminal()
            print("You must specify an item to take.")
            return
        
        item_name = args[0]
        player = globals.player
        valid_item = False
        for item in globals.inventory.items:
            if item_name == item.name:
                valid_item = True
                globals.inventory.take(player, item)
                util.clear_terminal()
                print(f"{item.name} added to inventory.\n")
                break

        if not valid_item:
            util.clear_terminal()
            print(f"No item named {item_name} found.\n")
            

class BackCommand(Command):
    def __init__(self, tag):
        super().__init__("Back", "Back out", tag, self.execute)
    def execute(self, player):
        player.back()

class AttackCommand(Command):
    def __init__(self, tag):
        super().__init__("Attack", "Attack an enemy or npc and deal damage.", tag, self.execute)
    def execute(self, player, *args, **kwargs):
        if not args:
            util.clear_terminal()
            # Display command name and definition
            print(f"Command: {self.name}")
            print(f"Definition: {self.description}")

            # Display enemies in the current location
            if player.location.name in globals.locations:
                location = globals.locations[player.location.name]
                enemy_names = '\n\t'.join([enemy for enemy in location.enemies]) if location.enemies else None
                if enemy_names:
                    print("\nEnemies in this location:")
                    print(f"\t{enemy_names}")
                else:
                    print("No enemies in this location.")
            
        else:
            enemy_name = args[0]
            if globals.combat is not None:
                enemy = next((enemy for enemy in globals.combat.enemies if enemy.name == enemy_name), None)
                if enemy is not None:
                    util.clear_terminal()
                    # Assuming globals.combat is the current combat instance
                    globals.combat.attack(player.damage, enemy)
                else:
                    util.clear_terminal()
                    print(f"No enemy named {enemy_name} found.")

class FleeCommand(Command):
    def __init__(self, tag):
        super().__init__("Flee", "Flee from combat", tag, self.execute)
    def execute(self, player, *args, **kwargs):
        globals.combat.flee()

class InventoryCommand(Command):
    def __init__(self, tag):
        super().__init__("Inventory", "Display player's inventory", tag, self.execute)
    def execute(self, player):
        util.clear_terminal()
        globals.player.show_inventory()

class DropCommand(Command):
    def __init__(self, tag):
        super().__init__("Drop", "Drop an item", tag, self.execute)
    def execute(self, player, *args, **kwargs):
        if not args:
            util.clear_terminal()
            print("You must specify an item to drop.")
            return
        
        item_name = args[0]
        player = globals.player
        valid_item = False
        for item in player.inventory.items:
            if item_name == item.name:
                valid_item = True
                globals.player.inventory.drop(item)
                break

        if not valid_item:
            util.clear_terminal()
            print(f"No item named {item_name} found.\n")