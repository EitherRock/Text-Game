from system import util
from inventory import Inventory

class NPC:
    def __init__(self, name, description, location, health, role, attitude, status, commands=None, items=None, relationship_status=None, relationships=None, dialogue_tree=None):
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


class Enemy(NPC):
    def __init__(self, name, description, location, health, role, status, commands=None, items=None, relationships=None, dialogue_tree=None):
        super().__init__(name, description, location, health, role, status, commands, items, relationships, dialogue_tree)
        self.attitude = 'hostile'
        self.experience = 10
        self.abilities = ['attack', 'defend', 'flee']
    
    
