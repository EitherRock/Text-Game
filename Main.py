import globals
from player_class import Player
from non_playable_character import NPC
from system import command, util, logger, display

dialogue_tree = {
    'start': {
        'text': "Welcome, traveler! What brings you to our village?",
        'responses': {
            # '1': ("I'm here to seek an audience with the elder.", 'check_reputation'),
            '1': ("Just passing through. Anything interesting happening around here?", 'passing'),
            '2': ("None of your business.", 'rude')
        }
    },
    'check_reputation': {
        'text': "",
        'responses': {}
    },
    'elder': {
        'text': "The elder is in the great hall. You may find him there.",
        'responses': {
            '1': ("Thank you.", 'end'),
            '2': ("Can you tell me more about the elder?", 'more_elder')
        }
    },
    'passing': {
        'text': "Well, we've had some trouble with bandits lately. It's been tough.",
        'responses': {
            '1': ("Bandits? Tell me more.", 'bandits'),
            '2': ("I can help with that.", 'help')
        }
    },
    'rude': {
        'text': "Alright, no need to be rude. Safe travels.",
        'responses': {}
    },
    'more_elder': {
        'text': "The elder is wise and has led our village for decades.",
        'responses': {
            '1': ("Thank you for the information.", 'end')
        }
    },
    'bandits': {
        'text': "The bandits have been attacking travelers on the main road.",
        'responses': {
            '1': ("I'll see what I can do.", 'end')
        }
    },
    'help': {
        'text': "We would be grateful for your assistance!",
        'responses': {
            '1': ("I'll take care of it.", 'end')
        }
    },
    'end': {
        'text': "Safe travels, adventurer.",
        'responses': {}
    }
}

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
        "sleep": command.SleepCommand(globals.player),
        "talk": command.TalkCommand(),

        
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
    globals.npcs = {
        "bryn": NPC(name='Bryn', description='A mystical lady', location='Town', health=10, role='Shopkeeper', attitude='friendly', status='alive', dialogue_tree=dialogue_tree), 
    }
    globals.locations = {
        "Cave": {
            "name": "Cave",
            "description": "A dark, damp cave",
            "items": [{'name': "Stick", 'searchable': True}, {'name':"Stone",'searchable': True}, {'name':"Stone",'searchable': True}, {'name':"Gold Coin",'searchable': True}],
            "enemies": ["Rat", "Bat"],
            "npcs": [],
            "connected_locations": ["Forest"],
            "commands": ["sleep"]
        },
        "Forest": {
            "name": "Forest",
            "description": "A dense forest",
            "items": [{'name': "Bow", 'searchable': True}],
            "enemies": ["Wolf", "Bear"],
            "connected_locations": ["Cave", "Town"],
            "npcs": [], 
            "commands": []

        },
        "Town": {
            "name": "Town",
            "description": "A bustling town",
            # "connected_locations": [{'name': "Tyrone and Bryn's Books and Things", "items": ["Book", "Potion"], "npcs": ["Tyrone", "Bryn"], "commands":[]}, {'name': "General Store", "items": ["Sword", "Shield"], "npcs": ["Shopkeeper"]}],
            "connected_locations": ["Forest", "General Store", "Tyrone and Bryn's Books and Things"],
            "npcs": [globals.npcs["bryn"]],
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
        print(command_input)
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
    

# Start the game loop
game_loop()
