import requests
import socket
import whois
import dns.resolver
import subprocess

def menu():
    print("""
==============================
       ANGEL KOROL TOOL PRO
==============================
1 - WHOIS информация
2 - DNS записи
3 - Поиск IP по домену
4 - Проверка robots.txt
5 - Ping сайта
6 - Проверка открытых портов
7 - Определение CDN
8 - Выход
==============================
""")

def pause():
    input("\nEnter для возврата...")

def whois_lookup():
    domain = input("Домен: ")
    try:
        w = whois.whois(domain)
        print("\nWHOIS:\n")
        print(w)
    except Exception as e:
        print("Ошибка WHOIS:", e)
    pause()

def dns_lookup():
    domain = input("Домен: ")
    try:
        for rtype in ["A", "MX", "NS"]:
            print(f"\n{rtype}:")
            answers = dns.resolver.resolve(domain, rtype, lifetime=5)
            for r in answers:
                print(r.to_text())
    except Exception as e:
        print("Ошибка DNS:", e)
    pause()

def ip_lookup():
    domain = input("Домен: ")
    try:
        ip = socket.gethostbyname(domain)
        print("IP:", ip)
    except Exception as e:
        print("Ошибка:", e)
    pause()

def robots_check():
    site = input("Сайт: ")
    try:
        url = f"http://{site}/robots.txt"
        r = requests.get(url, timeout=5)
        print("\nrobots.txt:\n")
        print(r.text)
    except Exception as e:
        print("Ошибка:", e)
    pause()

def ping_site():
    host = input("Сайт: ")
    try:
        result = subprocess.run(["ping", "-c", "1", host], stdout=subprocess.PIPE, text=True)
        print(result.stdout)
    except Exception as e:
        print("Ошибка ping:", e)
    pause()

def port_scan():
    host = input("Хост: ")
    ports = [21, 22, 80, 443, 8080]

    print("\nСканирование портов...\n")

    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((host, port))
            if result == 0:
                print(f"[+] Открыт порт: {port}")
            sock.close()
        except:
            pass

    pause()

def cdn_detect():
    site = input("Сайт: ")

    try:
        r = requests.get("http://" + site, timeout=5)
        headers = r.headers

        server = headers.get("Server", "").lower()
        cf = headers.get("cf-ray")
        via = headers.get("Via", "").lower()

        print("\nАнализ CDN:\n")

        if "cloudflare" in server or cf:
            print("Cloudflare CDN")
        elif "akamai" in server or "akamai" in via:
            print("Akamai CDN")
        elif "fastly" in server or "fastly" in via:
            print("Fastly CDN")
        else:
            print("CDN не найден или скрыт")

        print("\nServer:", server if server else "нет данных")

    except Exception as e:
        print("Ошибка:", e)

    pause()

while True:
    menu()
    choice = input("Выбор: ")

    if choice == "1":
        whois_lookup()
    elif choice == "2":
        dns_lookup()
    elif choice == "3":
        ip_lookup()
    elif choice == "4":
        robots_check()
    elif choice == "5":
        ping_site()
    elif choice == "6":
        port_scan()
    elif choice == "7":
        cdn_detect()
    elif choice == "8":
        print("Выход")
        break
    else:
        print("Неверный выбор")
        pause()
