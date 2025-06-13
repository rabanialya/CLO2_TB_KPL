import cProfile
from memory_profiler import profile

import time
import os
import requests

from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = os.getenv("BASE_URL")

# === OBSERVER PATTERN === #
class Observer:
    def update(self, event_type, data):
        pass

class Subject:
    def _init_(self):
        self._observers = []

    def add_observer(self, observer: Observer):
        self._observers.append(observer)

    def notify(self, event_type, data=None):
        for observer in self._observers:
            observer.update(event_type, data)

class UIObserver(Observer):
    def update(self, event_type, data):
        if event_type == "hp_changed":
            delay_print(f"⚠  HP {data['player']} sekarang {data['hp']}/{data['max_hp']}")
        elif event_type == "item_used":
            delay_print(f"🧪 {data['player']} menggunakan {data['item']}, HP menjadi {data['hp']}")
        elif event_type == "enemy_defeated":
            delay_print(f"🎯 Musuh {data['enemy']} telah dikalahkan!")

# === GAME CORE === #
class Player(Subject):
    def _init_(self, name, job, hp, attack):
        super()._init_()
        self.name = name
        self.job = job
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.items = []
        self.location = "Village"
        self.completed_side_quests = set()

    @profile
    def attack_enemy(self, enemy):
        delay_print(f"\n{self.name} menyerang {enemy.name}! ⚔")
        enemy.hp -= self.attack
        enemy.hp = max(0, enemy.hp)
        delay_print(f"{enemy.name} HP tersisa: {enemy.hp}")

    def use_item(self):
        if not self.items:
            delay_print("Kamu tidak punya item untuk digunakan. 🥴")
            return
        delay_print("\nItem yang tersedia:")
        for i, item in enumerate(self.items, start=1):
            delay_print(f"{i}. {item['name']} (+{item['heal']} HP)")
        choice = input("Pilih nomor item untuk dipakai (atau tekan Enter batal): ")
        if not choice.isdigit():
            delay_print("Batal menggunakan item.")
            return
        index = int(choice)
        if 1 <= index <= len(self.items):
            item = self.items.pop(index - 1)
            self.hp = min(self.max_hp, self.hp + item['heal'])
            self.notify("item_used", {"player": self.name, "item": item['name'], "hp": self.hp})
            delay_print(f"Kamu menggunakan {item['name']}, HP sekarang: {self.hp}")
        else:
            delay_print("Pilihan item tidak valid.")

class Enemy:
    def _init_(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    @profile
    def attack_player(self, player):
        delay_print(f"\n{self.name} menyerang {player.name}! ⚔")
        player.hp -= self.attack
        player.hp = max(0, player.hp)
        player.notify("hp_changed", {"player": player.name, "hp": player.hp, "max_hp": player.max_hp})
        delay_print(f"{player.name} HP tersisa: {player.hp}")

class Location:
    def _init_(self, name, description, enemies=None, neighbors=None, is_final=False, side_quest=None):
        self.name = name
        self.description = description
        self.enemies = enemies if enemies else []
        self.neighbors = neighbors if neighbors else {}
        self.is_final = is_final
        self.side_quest = side_quest
        self.is_cleared = False

def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        delay_print(f"Gagal mengambil data dari API: {e}")
        exit(1)

def choose_job(jobs_data):
    delay_print("\nPilih job karakter:")
    for i, (job, stats) in enumerate(jobs_data.items(), start=1):
        delay_print(f"{i}. {job} (HP: {stats['hp']}, Attack: {stats['attack']})")
    while True:
        choice = input("Masukkan nomor pilihan job: ")
        if choice.isdigit() and 1 <= int(choice) <= len(jobs_data):
            job_name = list(jobs_data.keys())[int(choice) - 1]
            return job_name, jobs_data[job_name]
        delay_print("Pilihan tidak valid, coba lagi.")

def print_location_info(current_location, locations):
    delay_print("\n" + "═" * 40)
    delay_print(f"==== {current_location.name} ==== ")
    delay_print(current_location.description)
    if current_location.side_quest:
        delay_print(f"Quest sampingan: {current_location.side_quest['description']} 🌟")
    delay_print("Arah yang bisa ditempuh:")
    for direction, neighbor_key in current_location.neighbors.items():
        neighbor = locations[neighbor_key]
        delay_print(f" - {direction.capitalize()} ke {neighbor.name}: {neighbor.description}")

@profile
def battle(player, enemy, location):
    delay_print(f"\nKamu bertemu {enemy.name}! ⚔")
    while player.hp > 0 and enemy.hp > 0:
        delay_print(f"\n{player.name} HP: {player.hp} / {player.max_hp} | {enemy.name} HP: {enemy.hp}")
        print("1. Serang ⚔\n2. Gunakan item 🧪")
        action = input("Pilih tindakan: ")
        if action == "1":
            player.attack_enemy(enemy)
        elif action == "2":
            player.use_item()
        else:
            print("Pilihan tidak valid.")

        if enemy.hp > 0:
            enemy.attack_player(player)

    if player.hp > 0:
        delay_print(f"\n🎉 Kamu menang melawan {enemy.name}!")
        player.notify("enemy_defeated", {"enemy": enemy.name})
        location.is_cleared = True
        return True
    else:
        delay_print(f"\n😢 {player.name} kalah melawan {enemy.name} ...")
        return False

@profile
def handle_side_quest(player, current_location, locations, enemies_data):
    if current_location.side_quest is None or current_location.name != "Forest" or current_location.side_quest['name'] in player.completed_side_quests:
        return
    delay_print(f"\nQuest sampingan ditemukan: {current_location.side_quest['description']} 🌟")
    choice = input("Ingin selesaikan quest ini? (ya/tidak): ").strip().lower()
    if choice != "ya":
        delay_print("Quest dilewati.")
        return
    delay_print("Quest dimulai... Cari herb langka.")
    fairy_stats = enemies_data.get("Fairy")
    if not fairy_stats:
        delay_print("Data musuh Fairy tidak tersedia.")
        return
    for i in range(3):
        fairy = Enemy("Fairy", fairy_stats["hp"], fairy_stats["attack"])
        delay_print(f"\nPertarungan {i+1} melawan Fairy!")
        if not battle(player, fairy, current_location):
            delay_print("Kamu kalah, quest gagal.")
            return
    delay_print("🎉 Kamu menang melawan Fairy!")
    delay_print("Kamu menemukan herb langka dan mendapat HP +20!")
    player.max_hp += 20
    player.hp = min(player.max_hp, player.hp + 20)
    player.completed_side_quests.add(current_location.side_quest['name'])
    current_location.is_cleared = True
    current_location.enemies = []
    print_location_info(current_location, locations)

def delay_print(message, delay=0.001):
    """Menampilkan pesan dengan delay."""
    for char in message:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()  # Untuk newline setelah pesan

@profile
def main():
    delay_print("\n=== Selamat datang di Game Petualangan Text ===")
    name = input("Masukkan nama pemain: ")
    jobs_data = fetch_data("jobs")
    job_name, job_stats = choose_job(jobs_data)

    player = Player(name, job_name, job_stats["hp"], job_stats["attack"])
    player.add_observer(UIObserver())

    for item_name, item_stats in fetch_data("items").items():
        player.items.append({"name": item_name, **item_stats})

    enemies_data = fetch_data("enemies")
    locations_json = fetch_data("locations")

    locations = {}
    for key, value in locations_json.items():
        locations[key] = Location(
            key,
            value["description"],
            value.get("enemies", []),
            value.get("neighbors", {}),
            value.get("is_final", False),
            value.get("side_quest")
        )

    visited = set()
    delay_print(f"\nHalo, {player.name} si {player.job}! Petualangan dimulai dari Desa.")

    state = "exploring"
    while True:
        current_location = locations[player.location]
        if state == "exploring":
            print_location_info(current_location, locations)
            handle_side_quest(player, current_location, locations, enemies_data)  # Panggil fungsi quest di sini
            if player.location not in visited and current_location.enemies:
                state = "battling"
            else:
                direction = input("Pilih arah untuk bergerak (atau 'exit' untuk keluar): ").strip().lower()
                if direction == "exit":
                    delay_print("Terima kasih sudah bermain! 👋")
                    break
                if direction in current_location.neighbors:
                    player.location = current_location.neighbors[direction]
                else:
                    delay_print("Arah tidak valid. Pilih arah yang tersedia.")

        elif state == "battling":
            for enemy_name in current_location.enemies:
                enemy_stats = enemies_data.get(enemy_name)
                if enemy_stats is None:
                    delay_print(f"Data untuk musuh {enemy_name} tidak ditemukan.")
                    continue
                enemy = Enemy(enemy_name, enemy_stats["hp"], enemy_stats["attack"])
                if not battle(player, enemy, current_location):
                    while True:
                        retry = input("\nKamu kalah. Ulang dari awal atau keluar? (ulang/keluar): ").strip().lower()
                        if retry == "ulang":
                            main()
                            return
                        elif retry == "keluar":
                            delay_print("Game selesai. Sampai jumpa!")
                            exit()
                        else:
                            delay_print("Pilihan tidak valid.")
            visited.add(player.location)
            state = "exploring"
            if current_location.is_cleared:
                delay_print("Musuh di lokasi ini telah dikalahkan. ✅")

if __name__ == "__main__":
    import sys

    if "--profile" in sys.argv:
        import cProfile
        cProfile.run('main()', 'profile_result.prof')
    else:
        main()