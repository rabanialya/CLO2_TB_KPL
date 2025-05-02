from enemy import Enemy
from utils import save_game
import sys
import random

def battle(player, enemy):
    print(f"Pertarungan dimulai melawan {enemy.name}!")

    while player.is_alive() and enemy.is_alive():
        print(f"\n{enemy.name} HP: {enemy.hp} | {player.name} HP: {player.hp}")
        action = input("Pilih tindakan (serang/skill/item/kabur): ").lower()

        if action == "serang":
            damage = player.attack()
            enemy.hp -= damage
            print(f"Kamu menyerang dan memberikan {damage} damage!")
            if enemy.is_alive():
                enemy_attack(player, enemy)

        elif action == "skill":
            print(f"Skill tersedia: {', '.join(player.skills)}")
            skill = input("Pilih skill: ").capitalize()

            if skill in player.skills:
                damage = player.attack() + 10
                enemy.hp -= damage
                print(f"Kamu menggunakan {skill} dan memberikan {damage} damage!")
                if enemy.is_alive():
                    enemy_attack(player, enemy)
            else:
                print("Skill tidak tersedia.")

        elif action == "item":
            player.use_item("Potion")

        elif action == "kabur":
            print("Kamu kabur dari pertarungan!")
            return False

        else:
            print("Perintah tidak dikenali. Coba lagi.")

    return player.is_alive()

def enemy_attack(player, enemy):
    damage = enemy.attack()
    player.hp -= damage
    print(f"{enemy.name} menyerang dan memberikan {damage} damage!")

def start_adventure(player):
    print(f"Selamat datang {player.name} sang {player.job}! Petualanganmu dimulai di Desa Awal.")

    while True:
        cmd = input("\n[Desa Awal] Apa yang ingin kamu lakukan? (help untuk bantuan) > ").lower()

        if cmd == "help":
            print("Perintah: ke utara, status, inventory, exit")
        elif cmd == "status":
            print(f"Nama: {player.name} | Job: {player.job} | HP: {player.hp}/{player.max_hp}")
        elif cmd == "inventory":
            print(f"Inventory: {', '.join(player.inventory)}")
        elif cmd == "ke utara":
            print("Kamu berjalan ke utara dan tiba di Hutan Gelap...")
            goblin = Enemy("Goblin")
            if battle(player, goblin):
                print("Goblin terjatuh dan menjatuhkan Potion.")
                player.inventory.append("Potion")
                save_game(player)

                mercy = input("Apakah kamu ingin membunuh Goblin atau membiarkannya hidup? (bunuh/biarkan): ").lower()
                if mercy == "bunuh":
                    print("Kamu menghabisi Goblin.")
                else:
                    print("Kamu membiarkan Goblin hidup.")

                print("Kamu melanjutkan perjalanan dan menemukan Gua Kristal.")
                quest_crystal_cave(player)
            else:
                print("Kamu kalah dalam pertarungan...")
                game_over()
            break
        elif cmd == "exit":
            print("Keluar dari game...")
            break
        else:
            print("Perintah tidak dikenali. Coba lagi.")

def quest_crystal_cave(player):
    def quest_crystal_cave(player):
        print("Di dalam gua, seorang kakek tua mendekat.")
    accept = input("Kakek: 'Tolong bantu aku dapatkan 3 bulu tikus.' Terima misi? (iya/tidak): ").lower()
    if accept == "iya":
        for i in range(1, 4):
            print(f"\n>> Tikus {i} muncul!")
            tikus = Enemy("Tikus")
            if battle(player, tikus):
                print(f"Kamu mendapatkan bulu tikus {i}.")
            else:
                print("Kamu kalah saat melawan tikus...")
                game_over()
                return

        print("Kamu kembali ke kakek dan menyerahkan bulu.")
        save_game(player)
        print("Kamu tiba di Kuil Kegelapan...")

        boss = Enemy("Boss Terakhir")
        print(f"Tiba-tiba, {boss.name} muncul dengan aura jahat!")
        print(f"Pertarungan dimulai melawan {boss.name}!")
    else:
        print("Kamu menolak membantu kakek.")
        print("Karena menolak, petualanganmu berakhir di sini. Game Over.")
        game_over()
        return  

    while boss.hp > 0 and player.hp > 0:
        print(f"\n{boss.name} HP: {boss.hp} | {player.name} HP: {player.hp}")
        action = input("Pilih tindakan (serang/skill/item/kabur): ").lower()

        if action == "serang":
            damage = player.attack()
            boss.hp -= damage
            print(f"Kamu menyerang dan memberikan {damage} damage!")
        elif action == "skill":
            if player.skills:
                print("Skill yang tersedia:", ', '.join(player.skills))
                skill_choice = input("Pilih skill: ").capitalize()
                if skill_choice in player.skills:
                    damage = random.randint(25, 40)
                    boss.hp -= damage
                    print(f"Kamu menggunakan {skill_choice} dan memberikan {damage} damage!")
                else:
                    print("Skill tidak valid.")
                    continue
            else:
                print("Kamu tidak punya skill.")
                continue
        elif action == "item":
            if player.inventory:
                player.use_item("Potion")
            else:
                print("Kamu tidak punya item!")
                continue
        elif action == "kabur":
            print("Tidak bisa kabur dari Boss!")
            continue
        else:
            print("Pilihan tidak dikenali.")
            continue

        if boss.hp > 0:
            damage = boss.attack()
            player.hp -= damage
            print(f"{boss.name} menyerang dan memberikan {damage} damage!")

    if player.is_alive():
        print(f"Selamat! Kamu mengalahkan {boss.name} dan menyelesaikan petualangan!")
        while True:
            again = input("Mau main lagi? (iya/tidak): ").lower()
            if again == "iya":
                from main import start
                start()
                break
            elif again == "tidak":
                print("Terima kasih sudah bermain!")
                exit()
            else:
                print("Pilihan tidak valid.")
    else:
        print("Kamu kalah... Game Over.")
        while True:
            again = input("Mau coba lagi? (iya/tidak): ").lower()
            if again == "iya":
                from main import start
                start()
                break
            elif again == "tidak":
                print("Terima kasih sudah bermain!")
                exit()
            else:
                print("Pilihan tidak valid.")

    while boss.hp > 0 and player.hp > 0:
        print(f"\n{boss.name} HP: {boss.hp} | {player.name} HP: {player.hp}")
        action = input("Pilih tindakan (serang/skill/item/kabur): ").lower()

        if action == "serang":
            damage = player.attack()
            boss.hp -= damage
            print(f"Kamu menyerang dan memberikan {damage} damage!")
        elif action == "skill":
            if player.skills:
                print("Skill yang tersedia:", ', '.join(player.skills))
                skill_choice = input("Pilih skill: ").capitalize()
                if skill_choice in player.skills:
                    damage = random.randint(25, 40)
                    boss.hp -= damage
                    print(f"Kamu menggunakan {skill_choice} dan memberikan {damage} damage!")
                else:
                    print("Skill tidak valid.")
                    continue
            else:
                print("Kamu tidak punya skill.")
                continue
        elif action == "item":
            if player.inventory:
                player.use_item("Potion")
            else:
                print("Kamu tidak punya item!")
                continue
        elif action == "kabur":
            print("Tidak bisa kabur dari Boss!")
            continue
        else:
            print("Pilihan tidak dikenali.")
            continue

        if boss.hp > 0:
            damage = boss.attack()
            player.hp -= damage
            print(f"{boss.name} menyerang dan memberikan {damage} damage!")

    if player.is_alive():
        print(f"Selamat! Kamu mengalahkan {boss.name} dan menyelesaikan petualangan!")
        while True:
            again = input("Mau main lagi? (iya/tidak): ").lower()
            if again == "iya":
                from main import start
                start()
                break
            elif again == "tidak":
                print("Terima kasih sudah bermain!")
                exit()
            else:
                print("Pilihan tidak valid.")
    else:
        print("Kamu kalah... Game Over.")
        while True:
            again = input("Mau coba lagi? (iya/tidak): ").lower()
            if again == "iya":
                from main import start
                start()
                break
            elif again == "tidak":
                print("Terima kasih sudah bermain!")
                exit()
            else:
                print("Pilihan tidak valid.")

def game_over():
    while True:
        choice = input("\nGAME OVER. Ingin mencoba lagi? (iya/tidak): ").lower()
        if choice == "iya":
            from main import start
            start()
            break
        elif choice == "tidak":
            print("Terima kasih sudah bermain!")
            sys.exit()
        else:
            print("Pilihan tidak dikenali. Coba lagi.")