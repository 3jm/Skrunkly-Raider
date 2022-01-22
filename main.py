import requests, os, time, ctypes, websocket, json, random, discum
from concurrent.futures import ThreadPoolExecutor
import colorama
from colorama import Fore, Style

req = requests.Session()
tokens = open('tokens.txt','r').read().splitlines()
colorama.init(autoreset=True)
with open("config.json", encoding='utf-8', errors='ignore') as f:
    configdata = json.load(f, strict=False)
config = configdata["BotConfig"]

tokens = open('tokens.txt','r').read().splitlines()
proxies = open('proxies.txt','r').read().splitlines()
proxies = [{'https':'http://'+proxy} for proxy in proxies]

class VERSION:
    __version__ = 1.0

def Setup():
    ctypes.windll.kernel32.SetConsoleTitleW(f'Skrunkly Raider v{VERSION.__version__} | By 3jm')
    os.system('cls')
    print(Fore.CYAN + '\n\n     >>' + Fore.RESET + ' Welcome to Skrunkly Raider ' + Fore.CYAN + f'v{VERSION.__version__}', Fore.RESET)
    print(Fore.CYAN + '     >>' + Fore.RESET + ' Github Link ' + Fore.CYAN +  '>>' + Fore.CYAN + f' https://github.com/3jm/Skrunkly', Fore.RESET)
    print(Fore.CYAN + '\n\n     1 >>' + Fore.RESET + ' Join (Invite Code)' + Fore.RESET)
    print(Fore.CYAN + '     2 >>'+ Fore.RESET + ' Leave (Server ID)' + Fore.RESET)
    print(Fore.CYAN + '     3 >>' + Fore.RESET + ' Spam (Channel ID) (Amount) (Message)' + Fore.RESET)
    print(Fore.CYAN + '     4 >>' + Fore.RESET + ' React (Channel ID) (Message)' + Fore.RESET)
    print(Fore.CYAN + '     5 >>' + Fore.RESET + ' Srape Proxies (HTTP)' + Fore.RESET)
    print(Fore.CYAN + '     6 >>' + Fore.RESET + ' Info' + Fore.RESET)
    print(Fore.CYAN + '     7 >>' + Fore.RESET + ' Reset Console' + Fore.RESET)

def Join(invite):
    try:
        print(f'{Fore.CYAN}     >>{Fore.RESET} Joining...{Fore.RESET}')
        inv = invite.replace('https://discord.gg/', "")
        if config["useproxy"] == True:
            for tok in tokens:
                bot = discum.Client(token = tok)
                proxy = random.choice(proxies)
                r = bot.joinGuild(inv)
        else:
            for tok in tokens:
                r = req.post(f'https://discord.com/api/v9/invites/{inv}', headers = {"Authorization": tok})
        print(f'{Fore.CYAN}     >>{Fore.RESET} All accounts have attempted to join the server.')
    except Exception as e:
        print(f"{Fore.RED}     [ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def Leave(serverid):
    try:
        print(f'{Fore.CYAN}     >>{Fore.RESET} Leaving...{Fore.RESET}')
        if config["useproxy"] == True:
            for tok in tokens:
                proxy = random.choice(proxies)
                r = req.delete(f'https://discord.com/api/v9/users/@me/guilds/{serverid}', headers = {'Authorization': tok}, proxies = proxy)
        else:
            for tok in tokens:
                r = req.delete(f'https://discord.com/api/v9/users/@me/guilds/{serverid}', headers = {'Authorization': tok})
        print(f'{Fore.CYAN}     >>{Fore.RESET} All accounts have attempted to leave the server.')
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def Spam(channel, amount, message):
    try:
        print(f'{Fore.CYAN}     >>{Fore.RESET} Spamming...{Fore.RESET}')
        if config["useproxy"] == True:
            for _ in range(int(amount)):
                for tok in tokens:
                    proxy = random.choice(proxies)
                    r = req.post(f'https://discordapp.com/api/v9/channels/{channel}/messages', headers = {'Authorization': tok}, json = {'content': message,'nonce':'','tts':False}, proxies = proxy)
        else:
            for _ in range(int(amount)):
                for tok in tokens:
                    r = req.post(f'https://discordapp.com/api/v9/channels/{channel}/messages', headers = {'Authorization': tok}, json = {'content': message,'nonce':'','tts':False})
                print(f'{Fore.CYAN}     >>{Fore.RESET} Spammed!')
    except Exception as e:
        print(f"{Fore.YELLOW}[ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
    Start()

def React():
    print(f'{Fore.RED}     [X]{Fore.RESET} Not setup yet!')
    Start()

def Info():
    print(f'\n\n     {Fore.CYAN}>> {Fore.RESET}Skrunkly was made by 3jm on github\n     {Fore.CYAN}>> {Fore.RESET}commands are seperated by {Fore.RED}SPACES{Fore.RESET}\n{Fore.YELLOW}     [!] {Fore.RESET}If you paid for this tool in {Fore.RED}ANY WAY{Fore.RESET} demand a refund.')
    Start()

def Reset():
    os.system('cls')
    Setup()
    Start()

def Scrape():
    print(f'{Fore.CYAN}     >> {Fore.RESET}Scraping Proxies...')
    try:
        r = requests.get('https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=1500')
        file = open("proxies.txt", "a+")
        file.seek(0)
        file.truncate()
        proxies = []
        for proxy in r.text.split('\n'):
            proxy = proxy.strip()
            if proxy:
                proxies.append(proxy)
        for p in proxies:
            file.write((p)+"\n")
        file.close()
        print(f"{Fore.CYAN}     >>{Fore.RESET} Finished!")
    except Exception as e:
        print(f"{Fore.RED}     [ERROR]: {Fore.RESET}{e}")
    Start()

def Start():
    command = list(input(Fore.CYAN + '\n\n     >> ' + Fore.RESET).split(' '))
    if command[0] == "1":
        invite = command[1]
        Join(invite)
    elif command[0] == "2":
        serverid = command[1]
        Leave(serverid)
    elif command[0] == "3":
        channel = command[1]
        amount = command[2]
        message = command[3]
        Spam(channel, amount, message)
    elif command[0] == "4":
        React()
    elif command[0] == "5":
        Scrape()
    elif command[0] == "6":
        Info()
    elif command[0] == "7":
        Reset()
    else:
        print(f'{Fore.RED}     [ERROR]{Fore.RESET} Invalid Command!')
        Start()

if __name__ == '__main__':
    try:
        Setup()
        Start()
    except Exception as e:
        print(f"{Fore.RED}     [ERROR]: {Fore.YELLOW}{e}"+Fore.RESET)
        Start()