import globals
from player_class import Player
from non_playable_character import NPC, Enemy
from location import Location
from item import Item, Container
from combat import Combat
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
    globals.combat = Combat()

    # Initialize the player
    player_name = input("Enter your name: ")
    globals.player = Player(player_name, 10, 5, 0, 5)

    globals.game_display = display.Display()

    globals.all_commands = {
        "travel": command.TravelCommand('player', globals.player),
        "fight": command.FightCommand(tag='player'),
        "search": command.SearchCommand('player', globals.player),
        "log": command.LogCommand('system', globals.player),
        "info": command.InfoCommand('system', globals.player),
        "quit": command.QuitCommand('system', globals.player),
        "sleep": command.SleepCommand('player', globals.player),
        "talk": command.TalkCommand('player'),
        "take": command.TakeCommand('player'),
        "back": command.BackCommand('system'),
        "attack": command.AttackCommand(tag='player'),
        "fight": command.FightCommand(tag='fight'),
        "flee": command.FleeCommand(tag='player'),

        
        # "buy": Command.BuyCommand("Buy", "Buy an item"),
        # "sell": Command.SellCommand("Sell", "Sell an item"),
        # "level_up": Command.LevelUpCommand("Level Up", "Level up your character"),
        # "quest": Command.QuestCommand("Quest", "Start a quest"),
        # "show_inventory": Command.ShowInventoryCommand("Show Inventory", "Show player's inventory")
    }

    globals.commands = {
        "travel": command.TravelCommand('player', globals.player),
        # "fight": command.FightCommand(),
        "search": command.SearchCommand('player', globals.player),
        "log": command.LogCommand('system', globals.player),
        "info": command.InfoCommand('system', globals.player),
        "quit": command.QuitCommand('system', globals.player),
        "sleep": command.SleepCommand('player', globals.player),
    }

    globals.combat_commands = {
        "attack": command.AttackCommand(tag='player'),
        "fight": command.FightCommand(tag='fight'),
        "flee": command.FleeCommand(tag='player'),
    }

    globals.items = {
        "Stick": Item(name="Stick", description="A small stick"),
        "Stone": Item(name="Stone", description="A small stone"),
        "Coin": Item(name="Coin", description="A shiny gold coin", price=1),
        "Backpack": Container(name="Backpack", description="A small backpack", capacity=5, equipable=True),
    }
    globals.npcs = {
        "bryn": NPC(name='Bryn', description='A mystical lady', location='Town', health=10, role='Shopkeeper', attitude='friendly', status='alive', dialogue_tree=dialogue_tree, damage=5),
        "tyrone": NPC(name='Tyrone', description='A wise crow', location='Town', health=10, role='Sage', attitude='friendly', status='alive', dialogue_tree=dialogue_tree, damage=5),
        "rat": Enemy(name='Rat', description='A small rat', location='Cave', health=5, damage=3, role='Enemy', status='alive'),
        "snake": Enemy(name='Snake', description='A venomous snake', location='Forest', health=3, damage=2, role='Enemy', status='alive')
    }
    globals.locations = {
        "Cave": Location(name="Cave", description="A dark, damp cave", items=[globals.items['Stick'], globals.items['Stone'], globals.items['Coin'], globals.items['Backpack']], enemies=[], npcs=[], connected_locations=["Forest"], commands=["sleep"]),
        "Forest": Location(name="Forest", description="A dense forest", items=[], enemies=['snake', 'rat'], connected_locations=["Cave", "Town"], npcs=[], commands=[]),
        "Town": Location(name="Town", description="A bustling town", connected_locations=["Forest", "Tyrone and Bryn's Books and Things-Not a location"], npcs=[globals.npcs["bryn"], globals.npcs["tyrone"]], items=[], enemies=[], commands=[])
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
        globals.game_display.process_player_input()
    

# Start the game loop
game_loop()
