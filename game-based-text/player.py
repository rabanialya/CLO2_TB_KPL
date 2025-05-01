import random
import json

class Player:
    def __init__(self, name, job):
        self.name = name
        self.job = job
        self.hp = 100
        self.max_hp = 100
        self.inventory = ["Potion"]

        # Load skill dari config
        with open('config.json') as f:
            config = json.load(f)
        self.skills = [skill.capitalize() for skill in config["jobs"].get(job, [])]

    def attack(self):
        return random.randint(15, 30)

    def use_item(self, item_name):
        item_name = item_name.capitalize()
        if item_name in self.inventory:
            if item_name == "Potion":
                heal_amount = 30
                self.hp = min(self.hp + heal_amount, self.max_hp)
                self.inventory.remove(item_name)
                print(f"{self.name} menggunakan {item_name} dan memulihkan {heal_amount} HP!")
            else:
                print("Item tidak dikenali.")
        else:
            print(f"{item_name} tidak ada di inventory.")

    def is_alive(self):
        return self.hp > 0
