from system import util
from inventory import Inventory
from combat import Combat
import globals as globals

class NPC:
    def __init__(self, name, description, location, health, role, attitude, damage, status, commands=None, items=None, relationship_status=None, relationships=None, dialogue_tree=None):
        self.name = name
        self.description = description
        self.location = location
        self.health = health
        self.commands = commands
        self.inventory = Inventory(items=items)
        self.attitude = attitude
        self.status = status
        self.relationship_status = relationship_status
        self.relationships = relationships
        self.role = role
        self.dialogue_tree = dialogue_tree
        self.damage = damage
    
    def __str__(self):
        return self.name
    
    def __repr__(self):
        return self.name
    
    def talk(self, dialogue_key):
        if dialogue_key == 'check_reputation':
            if self.attitude == 'good':
                next_dialogue = 'elder'
            elif self.attitude == 'bad':
                next_dialogue = 'no_audience'
            else:
                next_dialogue = 'neutral_reception'
            self.talk(next_dialogue)
            return

        current_dialogue = self.dialogue_tree[dialogue_key]
        util.clear_terminal()
        print(current_dialogue['text'])

        if current_dialogue['responses']:
            for key, (response_text, next_node) in current_dialogue['responses'].items():
                print(f"{key}. {response_text}")
            
            choice = input("Choose an option: ")
            
            while choice not in current_dialogue['responses']:
                print("Invalid choice. Please try again.")
                choice = input("Choose an option: ")

            next_node = current_dialogue['responses'][choice][1]
            self.talk(next_node)
        else:
            print("End of conversation.")

    def fight(self):
        globals.combat = Combat(globals.player, self)
        globals.combat.start()


        # Remove the 'take' and 'back' commands after the loop breaks
        # if 'attack' in globals.commands:
        #     del globals.commands['attack']
        # if 'travel' not in globals.commands:
        #     globals.commands['travel'] = globals.all_commands['travel']
        # if 'search' not in globals.commands:
        #     globals.commands['search'] = globals.all_commands['search']
        # if 'sleep' not in globals.commands: 
        #     globals.commands['sleep'] = globals.all_commands['sleep']

        # Reset the break_loop flag
        globals.break_loop = False
        




class Enemy(NPC):
    def __init__(self, name, description, location, health, role, status, damage, commands=None, items=None, relationships=None, dialogue_tree=None):
        super().__init__(name, description, location, health, role, status, damage, commands, items, relationships, dialogue_tree)
        self.attitude = 'hostile'
        self.experience = 10
        self.combat_commands = ['attack',] #'defend', 'flee']
    
    
