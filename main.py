import requests
import time
import random
from termcolor import colored

def load_accounts(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file if line.strip()]

def tap_coin(init_data, uid, shake_num, user_agent, proxies=None):
    url = "https://b.bittime.com/exchange-web-gateway/tg-mini-app/shake"
    payload = {
        "initData": init_data,
        "uid": uid,
        "shakeNum": shake_num,
        "coin": shake_num
    }
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": user_agent
    }
    response = requests.post(url, json=payload, headers=headers, proxies=proxies)
    return response.json()

def cooldown_timer(cooldown_seconds):
    while cooldown_seconds > 0:
        mins, secs = divmod(cooldown_seconds, 60)
        print(f"\rCooldown: {int(mins)} menit {int(secs):02d} detik", end="")        
        time.sleep(1)
        cooldown_seconds -= 1
    print("\nCooldown selesai.")

def get_random_user_agent():
    with open("useragent.txt", "r") as file:
        user_agents = [line.strip() for line in file if line.strip()]
    return random.choice(user_agents)

def get_random_shake_num():
    return random.randint(1, 40)

def random_cooldown():
    return random.randint(600, 1800)

def main():
    accounts = load_accounts("data.txt")
    total_accounts = len(accounts)
    print(colored(f"Total akun yang akan diproses: {total_accounts}", "blue"))

    while True:
        all_accounts_processed = True
        cooldown_seconds = 0

        for i, account_data in enumerate(accounts, start=1):
            print(colored(f"\nMemproses akun {i} dari {total_accounts}...", "yellow"))
            
            uid = account_data.split('%22id%22%3A')[1].split('%')[0]
            username = account_data.split('%22username%22%3A%22')[1].split('%')[0]
            
            print(colored(f"Memproses Akun: {username} (ID: {uid})", "green"))

            while True:
                shake_num = get_random_shake_num()
                user_agent = get_random_user_agent()
                
                response = tap_coin(account_data, uid, shake_num, user_agent)
                data = response.get("data", {})
                
                if "coin" in data:
                    print(f"Coin: {data['coin']}, Energy: {data['energy']}")

                energy = data.get("energy", 0)
                if energy <= 0:
                    cooldown_seconds = random.randint(3000, 3600)
                    all_accounts_processed = False
                    print(colored("Energi habis, memulai hitung mundur cooldown...", "red"))
                    break
                else:
                    time.sleep(random.randint(3, 7))

            print(colored("Menunggu 5-10 detik sebelum memproses akun berikutnya...\n", "yellow"))
            time.sleep(random.uniform(5, 10))

        if not all_accounts_processed:
            cooldown_timer(cooldown_seconds)

        if all_accounts_processed:
            break

    print(colored("Semua akun telah diproses.", "blue"))

if __name__ == "__main__":
    main()
