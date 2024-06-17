import globals
from player_class import Player
from system import command, util, logger, display




def game_setup():
    global player, commands, log, locations, game_display
    
    # Initialize the logger
    globals.log = logger.Logger()
    globals.log.log("Game started")

    # Initialize the player
    player_name = input("Enter your name: ")
    globals.player = Player(player_name, 10, 5, 0, 5)

    globals.game_display = display.Display()

    globals.all_commands = {
        "travel": command.TravelCommand(globals.player),
        "fight": command.FightCommand(),
        "search": command.SearchCommand(globals.player),
        "log": command.LogCommand(globals.player),
        "info": command.InfoCommand(globals.player),
        "quit": command.QuitCommand(globals.player),
        "sleep": command.SleepCommand(globals.player)

        
        # "buy": Command.BuyCommand("Buy", "Buy an item"),
        # "sell": Command.SellCommand("Sell", "Sell an item"),
        # "level_up": Command.LevelUpCommand("Level Up", "Level up your character"),
        # "quest": Command.QuestCommand("Quest", "Start a quest"),
        # "show_inventory": Command.ShowInventoryCommand("Show Inventory", "Show player's inventory")
    }

    globals.commands = {
        "travel": command.TravelCommand(globals.player),
        "fight": command.FightCommand(),
        "search": command.SearchCommand(globals.player),
        "log": command.LogCommand(globals.player),
        "info": command.InfoCommand(globals.player),
        "quit": command.QuitCommand(globals.player),
        "sleep": command.SleepCommand(globals.player)
    }

    globals.locations = {
        "Cave": {
            "name": "Cave",
            "description": "A dark, damp cave",
            "items": [{'name': "Stick", 'searchable': True}, {'name':"Stone",'searchable': True}, {'name':"Stone",'searchable': True}, {'name':"Gold Coin",'searchable': True}],
            "enemies": ["Rat", "Bat"],
            "commands": ["sleep"]
        },
        "Forest": {
            "name": "Forest",
            "description": "A dense forest",
            "items": [{'name': "Bow", 'searchable': True}],
            "enemies": ["Wolf", "Bear"],
            "commands": []
        },
        "Town": {
            "name": "Town",
            "description": "A bustling town",
            "locations": [{'name': "Tyrone and Bryn's Books and Things", "items": ["Book", "Potion"], "npcs": ["Tyrone", "Bryn"]}, {'name': "General Store", "items": ["Sword", "Shield"], "npcs": ["Shopkeeper"]}],
            "items": [],
            "enemies": [],
            "commands": []
        }
    }

    # Set the player's starting location 
    # TODO: set from csv or some kind of save file
    globals.player.location = globals.locations["Cave"]
    globals.player.previous_location = globals.locations["Cave"]

    # Print welcome message
    util.clear_terminal()
    print(f"Welcome, {globals.player.name}!")
    globals.log.log(f"{globals.player.name} Created")


def game_loop():
    util.clear_terminal()
    # Start the game setup
    game_setup()
    while True:
        globals.game_display.always_display()
        print("\033[31mThis is red text.\033[0m")
        print("\033[32mThis is green text.\033[0m")
        # Get user input
        command_input = input("Enter a command: ")
        command_name, *command_args = command_input.split()

        if command_name in globals.commands:
            globals.commands[command_name](globals.player, *command_args)
        else:
            print(f"Invalid command: {command_input} Try again.")

# Start the game loop
game_loop()
