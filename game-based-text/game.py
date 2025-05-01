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
            # Tidak ada serangan musuh saat pakai item

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
