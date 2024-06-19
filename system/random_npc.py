import csv
import random

# List of possible values for each attribute
names = ["NPC1", "NPC2", "NPC3"]
descriptions = ["A friendly NPC.", "A hostile NPC.", "A neutral NPC."]
locations = ["Cave", "Forest", "Castle"]
health_values = [10, 20, 30]
commands = ["talk", "attack", "give item"]
items = ["Sword", "Shield", "Potion"]
attitudes = ["Friendly", "Hostile", "Neutral"]
statuses = ["Alive", "Dead"]
relationship_statuses = ["Single", "Married", "Complicated"]
relationships = ["Friend", "Enemy", "Neutral"]
roles = ["Merchant", "Guard", "Villager"]
dialogue_trees = ["Hello!", "Go away!", "What do you want?"]

# Open the CSV file in write mode
with open('npc.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    # Write the header
    writer.writerow(["Name", "Description", "Location", "Health", "Commands", "Items", "Attitude", "Status", "Relationship Status", "Relationships", "Role", "Dialogue Tree"])
    # Write 10 random NPCs
    for _ in range(10):
        writer.writerow([
            random.choice(names),
            random.choice(descriptions),
            random.choice(locations),
            random.choice(health_values),
            random.choice(commands),
            random.choice(items),
            random.choice(attitudes),
            random.choice(statuses),
            random.choice(relationship_statuses),
            random.choice(relationships),
            random.choice(roles),
            random.choice(dialogue_trees),
        ])