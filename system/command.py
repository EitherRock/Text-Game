class Command:
    def __init__(self, name=None, description=None, func=None):
        self.name = name
        self.description = description
        self.func = func
        

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    
    def execute(self, player, command_args):
        pass

class TravelCommand(Command):
    def __init__(self, player):
        super().__init__("Travel", "Travel to a different location", player.travel)

    def execute(self, command_args):
        self.func(self.player, *command_args)

class FightCommand(Command):
    def __init__(self):
        super().__init__("Travel", "Travel to a different location")
    def execute(self, player, command_args):
        player.fight(command_args)

class QuitCommand(Command):
    def __init__(self, player):
        super().__init__("Quit", "Quit the game", player.quit)
    def execute(self, player):
        player.quit()

class LogCommand(Command):
    def __init__(self, player):
        super().__init__("Log", "Display the log of events", player.log)
    def execute(self, player):
        player.log()

class SearchCommand(Command):
    def __init__(self, player):
        super().__init__("Search", "Search the current location", player.search)
    def execute(self, player, command_args):
        player.search(command_args)

class SleepCommand(Command):
    def __init__(self, player):
        super().__init__("Sleep", "Rest and recover health and stamina", player.sleep)
    def execute(self, player):
        player.sleep()

class InfoCommand(Command):
    def __init__(self, player):
        super().__init__("Info", "Display player and location info", player.info)
    def execute(self, player, *args, **kwargs):
        self.func(player, *args, **kwargs)

