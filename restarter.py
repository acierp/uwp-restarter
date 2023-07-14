import webbrowser           
import requests
import json
import psutil
import time 

with open('config.json','r+', encoding='utf-8') as f:
    config = json.load(f)

def roblox_open():
    return "Windows10Universal.exe" in (p.name() for p in psutil.process_iter())

def kill_roblox():
    for proc in psutil.process_iter():
        if proc.name() == "Windows10Universal.exe":
            proc.kill()

def ps_data(server_url):
    get_launcher_data = requests.get(server_url, cookies={".ROBLOSECURITY": config['vip_server']['cookie']})
    if get_launcher_data.status_code == 200:
        for line in get_launcher_data.text.splitlines():
            if "GameLauncher" in line: return line
    else:
        return ps_data(server_url)
    
    
def join():
    if config['vip_server']['enabled'] == True:
        game_data = ps_data(config['vip_server']['url'])
        access_code = game_data.split("'")[1].strip()
        webbrowser.open(f'roblox://placeID={config["game_id"]}&accessCode={access_code}&linkCode={config["vip_server"]["url"].split("privateServerLinkCode=")[1]}')
    else:
        webbrowser.open(f'roblox://placeID={config["game_id"]}')

last_closed = time.time()
while True:
    if not roblox_open():
        kill_roblox()
        time.sleep(config['restart_delay_seconds'])
        join()
    if config['restart_on_interval']:
        if time.time() - last_closed >= config['restart_on_interval']['interval_seconds']:
            last_closed = time.time()
            kill_roblox()
            time.sleep(config['restart_delay_seconds'])
    time.sleep(1)
