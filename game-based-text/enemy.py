import json

with open('config.json') as f:
    config = json.load(f)

class Enemy:
    def __init__(self, name):
        self.name = name
        self.hp = config["enemies"][name]["hp"]
        self.attack_power = config["enemies"][name]["attack"]

    def attack(self):
        return self.attack_power

    def is_alive(self):
        return self.hp > 0
