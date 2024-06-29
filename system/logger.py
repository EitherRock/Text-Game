from datetime import datetime
from system.util import clear_terminal

class Logger:
    def __init__(self):
        self.events = []

    def log(self, event):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.events.append(f"{timestamp}: {event}")

    def display(self):
        clear_terminal()
        for event in self.events:
            print(event)
    
    def print_and_log(self, text):
        print(text)
        self.log(text)