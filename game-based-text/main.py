from player import Player
import game
import json

def start():
    print("🔮 Selamat datang di Petualangan Fantasy Land!🔮")
    
    name = input("Masukkan nama karaktermu: ")
    
    with open('config.json') as f:
        config = json.load(f)

    while True:
        print("Pilih job: Warrior🪖, Mage🧙‍♂️, Thief🥷")
        job = input("> ").capitalize()

        if job in config["jobs"]:
            break
        else:
            print("Job tidak valid, coba lagi.")

    player = Player(name, job)
    
    print(f"Skill {job}:")
    for skill in player.skills:
        print(f"- {skill}")

    print(f"⚔️ Petualangan dimulai ⚔️, {player.name}!")
    game.start_adventure(player)

if __name__ == "__main__":
    start()