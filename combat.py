import globals as globals

class Combat:
    def __init__(self, player=None, enemy=None):
        self.player = player
        self.enemy = enemy

    def start(self):
        if 'attack' not in globals.commands:
                globals.commands['attack'] = globals.all_commands['attack']
        if 'travel' in globals.commands:
            del globals.commands['travel']
        if 'search' in globals.commands:
            del globals.commands['search']
        if 'sleep' in globals.commands:
            del globals.commands['sleep']
        print("Combat started!")
        damage = 0
        # Process commands until the user enters the 'back' command
        while True:
            print(f"You fight the {self.enemy.name}...")
            globals.game_display.process_command()
            if globals.break_loop:
                break
            damage = self.player_turn(damage=damage)
            if self.check_defeat():
                globals.break_loop = True
                break
            damage = self.enemy_turn(damage=damage)
            if self.check_victory():
                globals.break_loop = True
                break
    
    def player_turn(self, damage):
        print("Player's turn.")
        if self.player.health - damage <= 0:
            print("Player is defeated.")
            globals.break_loop = True
            return
        else:
            globals.game_display.process_command()
        
            return damage, 
    
    def enemy_turn(self, damage):
        print("Enemy's turn.")
        print("Enemy attacks!")
        # self.player.health -= self.enemy.attack
        # print(f"Player health: {self.player.health}")
        damage = 1
        return damage
    
    def check_victory(self):
        if self.enemy.health <= 0:
            print("Player wins!")
            return True
        return False
    
    def check_defeat(self):
        if self.player.health <= 0:
            print("Player loses!")
            return True
        return False
    
    def end(self):
        print("Combat ended.")
    
    def __str__(self):
        return "Combat"
    
    def __repr__(self):
        return "Combat"
    
    def attack(self, damage, target):
        target.health -= damage
        return damage
    
    def flee(self):
        pass

    