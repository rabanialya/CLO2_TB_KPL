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
