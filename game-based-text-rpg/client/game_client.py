import requests

BASE_URL = "http://127.0.0.1:8000"

class Player:
    def __init__(self, name, job, hp, attack):
        self.name = name
        self.job = job
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.items = []
        self.location = "Village"
        self.completed_side_quests = set()

    def attack_enemy(self, enemy):
        print(f"\n{self.name} menyerang {enemy.name}! ⚔️")
        enemy.hp -= self.attack
        if enemy.hp < 0:
            enemy.hp = 0
        print(f"{enemy.name} HP tersisa: {enemy.hp}")

    def use_item(self):
        if not self.items:
            print("Kamu tidak punya item untuk digunakan. 🥴")
            return
        print("\nItem yang tersedia:")
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item['name']} (+{item['heal']} HP)")
        choice = input("Pilih nomor item untuk dipakai (atau tekan Enter batal): ")
        if not choice.isdigit():
            print("Batal menggunakan item.")
            return
        choice = int(choice)
        if 1 <= choice <= len(self.items):
            item = self.items.pop(choice - 1)
            self.hp += item["heal"]
            if self.hp > self.max_hp:
                self.hp = self.max_hp
            print(f"Kamu menggunakan {item['name']} dan HP-mu menjadi {self.hp}.")
        else:
            print("Pilihan item tidak valid.")

def fetch_data(endpoint):
    try:
        response = requests.get(f"{BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching {endpoint} from API: {e}")
        exit(1)

def choose_job(jobs_data):
    print("\nPilih job karakter:")
    for i, (job, stats) in enumerate(jobs_data.items(), start=1):
        print(f"{i}. {job} (HP: {stats['hp']}, Attack: {stats['attack']})")
    while True:
        choice = input("Masukkan nomor pilihan job: ")
        if choice.isdigit() and 1 <= int(choice) <= len(jobs_data):
            job_name = list(jobs_data.keys())[int(choice) - 1]
            return job_name, jobs_data[job_name]
        print("Pilihan tidak valid, coba lagi.")

def print_location_info(location, locations):
    print("\n" + "═" * 40)  
    print(f"=== {location.name} === 🌍")
    print(location.description)
    if location.side_quest:
        print(f"Quest sampingan tersedia: {location.side_quest['description']} 🌟")
    print("Arah yang bisa ditempuh:")
    for direction, neighbor_key in location.neighbors.items():
        neighbor = locations[neighbor_key]
        print(f" - {direction.capitalize()} ke {neighbor.name}: {neighbor.description}")

def print_battle_result(player, enemy):
    print("\n" + "═" * 40)  
    print(f"Pertarungan dimulai antara {player.name} dan {enemy.name}! 🎮")
    print("═" * 40)

def battle(player, enemy, current_location):
    print(f"\nKamu bertemu dengan {enemy.name}! ⚔️")  
    print_battle_result(player, enemy)
    while player.hp > 0 and enemy.hp > 0:
        print(f"\n{player.name} HP: {player.hp} / {player.max_hp} | {enemy.name} HP: {enemy.hp}")
        print("1. Serang ⚔️")
        print("2. Gunakan item 🧪")
        choice = input("Pilih tindakan: ")
        if choice == "1":
            player.attack_enemy(enemy)
        elif choice == "2":
            player.use_item()
        else:
            print("Pilihan tidak valid, giliran musuh.")
        
        if enemy.hp > 0:
            enemy.attack_player(player)

    if player.hp > 0:
        print(f"\n🎉 Kamu menang melawan {enemy.name}! 🎉")
        current_location.is_cleared = True  
        return True
    else:
        print(f"\n😢 {player.name} kalah melawan {enemy.name} ... Game over.")
        return False

def handle_side_quest(player, location):
    if location.name != "Forest" or (location.side_quest and location.side_quest["name"] in player.completed_side_quests):
        return
    print("\n" + "═" * 40)  
    print(f"Quest sampingan ditemukan: {location.side_quest['description']} 🌟")
    choice = input("Apakah kamu ingin menyelesaikan quest ini? (ya/tidak): ").strip().lower()
    if choice == "ya":
        print("Quest sampingan dimulai... 🚀")
        print("Kamu harus mencari herb langka di hutan.")
        
        enemies_data = fetch_data("enemies")  
        fairy_stats = enemies_data.get("Fairy")  
        
        if fairy_stats:
            for i in range(3):  
                fairy = Enemy("Fairy", fairy_stats["hp"], fairy_stats["attack"])  
                print(f"\nPertarungan {i + 1} dimulai melawan Fairy!")
                won = battle(player, fairy, location)  
                
                if not won:  
                    print("Kamu kalah dalam pertarungan. Quest gagal.")
                    return  
            
            print("Kamu berhasil menemukan herb langka! 🌿")
            print("Kamu berhasil menyelesaikan quest dan mendapat hadiah HP +20! 🎁")
            player.max_hp += 20
            player.hp += 20
            if player.hp > player.max_hp:
                player.hp = player.max_hp
            print(f"HP maksimalmu sekarang {player.max_hp} dan HP saat ini {player.hp}")
            player.completed_side_quests.add(location.side_quest["name"])
            
            location.is_cleared = True  
            location.enemies = []  
        else:
            print("Data musuh tidak ditemukan.")
    else:
        print("Kamu melewatkan quest sampingan ini.")

def main():
    print("\n=== Selamat datang di Game Petualangan Text ===")
    name = input("Masukkan nama pemain: ")
    jobs_data = fetch_data("jobs")
    job_name, job_stats = choose_job(jobs_data)
    player = Player(name, job_name, job_stats["hp"], job_stats["attack"])
    items_data = fetch_data("items")
    for item_name, item_stats in items_data.items():
        player.items.append({"name": item_name, **item_stats})
    enemies_data = fetch_data("enemies")


visited = set()
    print(f"\nHalo, {player.name} si {player.job}! Petualangan dimulai dari Desa.")
    # Automata
    state = "exploring"
    while True:
        current_location = locations[player.location]
        if state == "exploring":
            print_location_info(current_location, locations)
            handle_side_quest(player, current_location)
            if player.location not in visited and current_location.enemies:
                state = "battling"
            else:
                print("\nArah mana yang ingin kamu tuju?")
                for direction, neighbor_key in current_location.neighbors.items():
                    neighbor = locations[neighbor_key]
                    print(f" - {direction.capitalize()} ke {neighbor.name}")
                direction = input("Masukkan arah (atau ketik 'exit' untuk keluar): ").strip().lower()
                if direction == "exit":
                    print("Terima kasih sudah bermain! 👋")
                    break
                if direction in current_location.neighbors:
                    player.location = current_location.neighbors[direction]
                else:
                    print("Arah tidak valid. Silakan pilih lagi.")
        elif state == "battling":
            for enemy_name in current_location.enemies:
                enemy_stats = enemies_data.get(enemy_name)
                if not enemy_stats:
                    print(f"Musuh {enemy_name} tidak ditemukan di data API.")
                    continue
                enemy = Enemy(enemy_name, enemy_stats["hp"], enemy_stats["attack"])
                won = battle(player, enemy, current_location)
                if not won:
                    while True:
                        choice = input("\nKamu kalah. Ingin coba lagi dari awal atau keluar? (ulang/keluar): ").strip().lower()
                        if choice == "ulang":
                            main()  
                            return
                        elif choice == "keluar":
                            print("Game selesai. Terima kasih sudah bermain! 👋")
                            exit()
                        else:
                            print("Pilihan tidak valid. Ketik 'ulang' atau 'keluar'.")
            visited.add(player.location)  
            state = "exploring"  
            if current_location.is_cleared:
                print("Disini musuh sudah dikalahkan. ✅")

if __name__ == "__main__":
    main()
