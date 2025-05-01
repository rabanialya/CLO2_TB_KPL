import json

def save_game(player):
    data = {
        "name": player.name,
        "job": player.job,
        "hp": player.hp,
        "inventory": player.inventory
    }
    with open('savegame.json', 'w') as f:
        json.dump(data, f)
    print("Game disimpan!")

def load_game():
    try:
        with open('savegame.json', 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return None

