import globals as globals
from system.util import clear_terminal

class Combat:
    def __init__(self, player=None, enemies=None):
        self.player = player
        self.enemies = enemies
        self.current_turn = None
        self.round = 0
        self.previous_commands = {}
        self.combat_commands = {}
        self.message = ""

    def combat_setup(self):
        self.previous_commands = globals.commands
        if self.combat_commands is not None:
            # collect players combat commands to be used in combat
            for command in self.player.combat_commands:
                if command in globals.all_commands:
                    self.combat_commands[command] = globals.all_commands[command]
                    # temporarily add combat commands to globals.commands
                    globals.commands = self.combat_commands
        return
        
    def start(self):
        self.combat_setup()
        globals.log.print_and_log("Combat started.")
        
        while True:
            self.round += 1
            globals.log.print_and_log(f"Round {self.round}")
            self.current_turn = self.player
            self.player_turn()
            if globals.break_loop:
                break
            if self.check_victory():
                break
            
            for enemy in self.enemies:
                self.current_turn = enemy
                self.enemy_turn(enemy)
                if globals.break_loop:
                    break
                if self.check_defeat():
                    self.set_defeat()
                    break
                globals.game_display.display_combat_info(self.player, self.enemies, self.current_turn, self.round, last_atk_info=self.message)
                globals.game_display.process_player_input(continue_text=True)
            if globals.break_loop:
                break
                
        
        self.end()
            
        
    
    def player_turn(self):
        clear_terminal()
        globals.game_display.display_combat_info(self.player, self.enemies, self.current_turn, self.round)
        globals.game_display.process_player_input()
        return 
    
    def enemy_turn(self, enemy):
        self.attack(enemy.damage, self.player)
        return 
    
    def check_victory(self):
        if self.enemies:
            for enemy in self.enemies:
                if enemy.health <= 0:
                    self.message = f"{enemy.name} defeated!"
                    self.enemies.remove(enemy)
                    globals.game_display.display_combat_info(self.player, self.enemies, self.current_turn, self.round, last_atk_info=self.message)
                    globals.game_display.process_player_input(continue_text=True)
                    clear_terminal()
                    self.check_victory()
        else:
            print("All enemies defeated.")
            globals.break_loop = True
            return True
        

    
    def check_defeat(self):
        if self.player.health <= 0:
            self.message = f"{self.player.name} defeated!"
            # globals.game_display.process_player_input(continue_text=True)
            globals.break_loop = True
            return True
        return False
    
    def set_defeat(self):
        self.player.health = 1
        self.player.location = globals.locations['Cave']
        print(f'{self.player.name} wakes up in a cave with 1 health.')
        return
    
    def combat_cleanup(self):
        # remove combat commands from globals.commands
        if globals.break_loop:
            globals.break_loop = False
        globals.commands = self.previous_commands
        self.previous_commands = {}

        return

    def end(self):
        self.combat_cleanup()
    
    def __str__(self):
        return "Combat"
    
    def __repr__(self):
        return "Combat"
    
    def attack(self, damage, target):
        target.health -= damage
        # add damage modifier based on player/enemy stats and weapons

        message = f"{self.current_turn.name} attacks {target.name} for {damage} damage."
        self.message = message
        return
    
    def flee(self):
        print(f"{self.current_turn.name} flees combat.")
        globals.break_loop = True
        return
    

    