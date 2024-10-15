import json
import requests
import random
import threading
import time
from colorama import Fore, Style
from discord import Client, Intents
import asyncio
from colorama import init

init(autoreset=True)
with open('sb.json', 'r') as json_file:
    config = json.load(json_file)
grupchat_id = config.get('grupchatid', "unknown")
with open('token.txt', 'r') as token_file:
    tokens = [line.strip() for line in token_file.readlines()]
with open('numesv.txt', 'r') as names_file:
    names = [line.strip() for line in names_file.readlines()]
intents = Intents.all()
client = Client(intents=intents)
async def get_user_name(token):
    headers = {
        'Authorization': token
    }
    response = requests.get('https://discord.com/api/v10/users/@me', headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data['username']
    else:
        return "unknow username"
def change_name(token, entity_id, new_name, old_name, user_name):
    url = f'https://discord.com/api/v10/channels/{entity_id}'
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    data = {
        'name': new_name
    }
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"{Fore.MAGENTA}{user_name} successfully changed group name [{old_name}] to [{new_name}]")
    elif response.status_code == 401:
        print(f"{Fore.BLACK}{user_name} failed to change group name nigga [401]")
    elif response.status_code == 403:
        print(f"{Fore.BLACK}{user_name} failed to change group name nigga [403]")
    else:
        print(f"{Fore.BLACK}{user_name} failed to change group name nigga [{response.text}]")
async def change_names_periodically(token):
    user_name = await get_user_name(token)
    while True:
        new_name = random.choice(names)
        url = f'https://discord.com/api/v10/channels/{grupchat_id}'
        headers = {
            'Authorization': token
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            old_name = response.json().get('name', 'unknow grup')
            print(f"{Fore.MAGENTA}{user_name} successfully changed group name [{old_name}] to [{new_name}]")
            change_name(token, grupchat_id, new_name, old_name, user_name)
        else:
            print(f"{Fore.BLACK}{user_name} failed to fetch the current group name [{response.status_code}]")
        time.sleep(1)
def start_threads():
    threads = []
    for token in tokens:
        thread = threading.Thread(target=lambda: asyncio.run(change_names_periodically(token)))
        threads.append(thread)
        thread.start()
    for thread in threads:
        thread.join()
if __name__ == "__main__":
    start_threads()
