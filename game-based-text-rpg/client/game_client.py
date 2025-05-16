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
