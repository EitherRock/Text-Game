class Shop:
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def display_items(self):
        print(f"Welcome to {self.name}!")
        print("Available items:")
        for item in self.items:
            print(f"- {item}")

    def buy_item(self, item):
        if item in self.items:
            print(f"You bought {item}!")
            self.items.remove(item)
        else:
            print(f"Sorry, {item} is not available.")

    def add_item(self, item):
        self.items.append(item)
        print(f"{item} has been added to the shop.")

# Example usage:
my_shop = Shop("My Shop", ["Sword", "Shield", "Potion"])
my_shop.display_items()
my_shop.buy_item("Sword")
my_shop.display_items()
my_shop.add_item("Bow")
my_shop.display_items()
