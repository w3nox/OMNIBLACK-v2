import os
import sys
import json
import time
import requests
import re
import socket
import phonenumbers
from phonenumbers import carrier, geocoder, timezone
import dns.resolver
import subprocess
import threading
from colorama import init, Fore, Style
import random
from fake_useragent import UserAgent
import warnings
warnings.filterwarnings("ignore")

init(autoreset=True)

class ProbivSoft:
    def __init__(self):
        self.ua = UserAgent()
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': self.ua.random})
        self.results = {}
        
    def print_banner(self):
        print(Fore.CYAN + r"""
 ______     __    __     __   __     __     ______     __         ______     ______     __  __       
/\  __ \   /\ "-./  \   /\ "-.\ \   /\ \   /\  == \   /\ \       /\  __ \   /\  ___\   /\ \/ /       
\ \ \/\ \  \ \ \-./\ \  \ \ \-.  \  \ \ \  \ \  __<   \ \ \____  \ \  __ \  \ \ \____  \ \  _"-.     
 \ \_____\  \ \_\ \ \_\  \ \_\\"\_\  \ \_\  \ \_____\  \ \_____\  \ \_\ \_\  \ \_____\  \ \_\ \_\    
  \/_____/   \/_/  \/_/   \/_/ \/_/   \/_/   \/_____/   \/_____/   \/_/\/_/   \/_____/   \/_/\/_/  v2.0
                                    made by w3nox
    """ + Style.RESET_ALL)
    
    def print_menu(self):
        print(Fore.CYAN + """
╔════════════════════════════════╗
║ 1. Пробив по IP                ║
║ 2. Пробив по телефону          ║
║ 3. Пробив по email             ║
║ 4. Пробив по username          ║ 
║ 5. Выход                       ║
╚════════════════════════════════╝
        """ + Style.RESET_ALL)

    # ========== IP ПРОБИВ (12 САЙТОВ) ==========
    def ip_lookup(self, ip):
        print(Fore.CYAN + f"\n{'='*60}")
        print(f"[*] ПРОБИВ IP: {ip}")
        print(f"{'='*60}" + Style.RESET_ALL)
        
        results = []
        
        #  ip-api.com
        try:
            resp = self.session.get(f"http://ip-api.com/json/{ip}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('status') == 'success':
                    print(Fore.GREEN + "\n[1] ip-api.com:" + Style.RESET_ALL)
                    print(f"    Страна: {data.get('country')}")
                    print(f"    Регион: {data.get('regionName')}")
                    print(f"    Город: {data.get('city')}")
                    print(f"    Провайдер: {data.get('isp')}")
                    print(f"    Координаты: {data.get('lat')}, {data.get('lon')}")
                    results.append(data)
        except: pass
        
        #  ipinfo.io
        try:
            resp = self.session.get(f"https://ipinfo.io/{ip}/json", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                print(Fore.GREEN + "\n[2] ipinfo.io:" + Style.RESET_ALL)
                print(f"    Хост: {data.get('hostname', 'Нет')}")
                print(f"    Организация: {data.get('org', 'Нет')}")
                print(f"    Локация: {data.get('loc', 'Нет')}")
                results.append(data)
        except: pass
        
        #  ip2location
        try:
            resp = self.session.get(f"https://api.ip2location.com/v2/?ip={ip}&key=demo", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                print(Fore.GREEN + "\n[3] ip2location:" + Style.RESET_ALL)
                print(f"    Страна: {data.get('country_name', 'Нет')}")
                print(f"    Регион: {data.get('region_name', 'Нет')}")
                print(f"    Город: {data.get('city_name', 'Нет')}")
                results.append(data)
        except: pass
        
        #  geoplugin
        try:
            resp = self.session.get(f"http://www.geoplugin.net/json.gp?ip={ip}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                print(Fore.GREEN + "\n[4] geoplugin:" + Style.RESET_ALL)
                print(f"    Страна: {data.get('geoplugin_countryName', 'Нет')}")
                print(f"    Валюта: {data.get('geoplugin_currencyCode', 'Нет')}")
                results.append(data)
        except: pass
        
        #  abstractapi
        try:
            resp = self.session.get(f"https://ipgeolocation.abstractapi.com/v1/?api_key=ea77232d0a5c40f4b3b6ebc75e87d5c9&ip_address={ip}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                print(Fore.GREEN + "\n[5] abstractapi:" + Style.RESET_ALL)
                print(f"    Континент: {data.get('continent', 'Нет')}")
                print(f"    Часовой пояс: {data.get('timezone', {}).get('name', 'Нет')}")
                results.append(data)
        except: pass
        
        #  ipwhois
        try:
            resp = self.session.get(f"http://ipwho.is/{ip}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('success'):
                    print(Fore.GREEN + "\n[6] ipwhois.io:" + Style.RESET_ALL)
                    print(f"    Страна: {data.get('country')}")
                    print(f"    Регион: {data.get('region')}")
                    print(f"    Провайдер: {data.get('connection', {}).get('isp', 'Нет')}")
                    results.append(data)
        except: pass
        
        #  ipqualityscore (репутация)
        try:
            print(Fore.GREEN + "\n[7] ipqualityscore.com:" + Style.RESET_ALL)
            print(f"    Проверка репутации: https://www.ipqualityscore.com/free-ip-lookup-proxy-vpn-test/lookup/{ip}")
        except: pass
        
        #  abuseipdb (жалобы)
        try:
            print(Fore.GREEN + "\n[8] abuseipdb.com:" + Style.RESET_ALL)
            print(f"    Жалобы на IP: https://www.abuseipdb.com/check/{ip}")
        except: pass
        
        #  shodan (порты и сервисы)
        try:
            print(Fore.GREEN + "\n[9] shodan.io:" + Style.RESET_ALL)
            print(f"    Открытые порты: https://www.shodan.io/host/{ip}")
        except: pass
        
        #  virustotal (репутация)
        try:
            print(Fore.GREEN + "\n[10] virustotal.com:" + Style.RESET_ALL)
            print(f"    Проверка на вредонос: https://www.virustotal.com/gui/ip-address/{ip}")
        except: pass
        
        #  criminalip.io
        try:
            print(Fore.GREEN + "\n[11] criminalip.io:" + Style.RESET_ALL)
            print(f"    Сканирование: https://www.criminalip.io/asset/ip/{ip}")
        except: pass

    # ========== ТЕЛЕФОН ПРОБИВ (12+ ИСТОЧНИКОВ) ==========
    def phone_lookup(self, phone):
        print(Fore.CYAN + f"\n{'='*60}")
        print(f"[*] ПРОБИВ ТЕЛЕФОНА: {phone}")
        print(f"{'='*60}" + Style.RESET_ALL)
        
        phone_clean = re.sub(r'[^0-9+]', '', phone)
        if not phone_clean.startswith('+'):
            phone_clean = '+7' + phone_clean[-10:] if len(phone_clean) >= 10 else '+' + phone_clean
        
        #  Phonenumbers lib
        try:
            parsed = phonenumbers.parse(phone_clean, None)
            print(Fore.GREEN + "\n[1] Phonenumbers lib:" + Style.RESET_ALL)
            print(f"    Международный: {phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL)}")
            print(f"    Страна: {geocoder.description_for_number(parsed, 'ru')}")
            print(f"    Оператор: {carrier.name_for_number(parsed, 'ru')}")
            print(f"    Валидный: {phonenumbers.is_valid_number(parsed)}")
        except: pass
        
        # numverify
        try:
            resp = self.session.get(f"http://apilayer.net/api/validate?access_key=16a7956d8f8f9b4ef04b109b01b9bc08&number={phone_clean}&country_code=RU&format=1", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                if data.get('valid'):
                    print(Fore.GREEN + "\n[2] numverify:" + Style.RESET_ALL)
                    print(f"    Страна: {data.get('country_name')}")
                    print(f"    Оператор: {data.get('carrier')}")
                    print(f"    Тип: {data.get('line_type')}")
        except: pass
        
        #  Telegram
        try:
            print(Fore.GREEN + "\n[3] Telegram:" + Style.RESET_ALL)
            print(f"    Ссылка: https://t.me/{phone_clean}")
            print(f"    Проверка: @getchatlistbot - в каких группах")
        except: pass
        
        #  GetContact
        try:
            print(Fore.GREEN + "\n[6] GetContact:" + Style.RESET_ALL)
            print(f"    Искать в приложении")
        except: pass
        
        #  СБП перевод
        try:
            print(Fore.GREEN + "\n[7] СБП:" + Style.RESET_ALL)
            print(f"    Попробуй перевести 1 рубль через Сбер/Тинькофф - увидишь имя")
        except: pass
        
        #  sync.me
        try:
            print(Fore.GREEN + "\n[10] sync.me:" + Style.RESET_ALL)
            print(f"    Поиск по базе: https://sync.me/search/?number={phone_clean}")
        except: pass
        
        #  Telegram боты
        try:
            print(Fore.GREEN + "\n[11] Telegram боты:" + Style.RESET_ALL)
            print(f"    @Vbib_bot - Facebook аккаунт")
            print(f"    @TrueCaller1Bot - имя владельца")
            print(f"    @LeakCheck1_bot - утечки")
            print(f"    @x8152384_bot - соцсети")
        except: pass
        
        print(Fore.CYAN + f"\n{'='*60}" + Style.RESET_ALL)

    # ========== EMAIL ПРОБИВ (12 ИСТОЧНИКОВ) ==========
    def email_lookup(self, email):
        print(Fore.CYAN + f"\n{'='*60}")
        print(f"[*] ПРОБИВ EMAIL: {email}")
        print(f"{'='*60}" + Style.RESET_ALL)
        
        domain = email.split('@')[1]
        
        #  Формат
        print(Fore.GREEN + "\n[1] Формат:" + Style.RESET_ALL)
        if re.match(r"[^@]+@[^@]+\.[^@]+", email):
            print(f"    ✓ Корректный email")
            print(f"    Домен: {domain}")
        
        #  MX записи
        try:
            mx_records = dns.resolver.resolve(domain, 'MX')
            print(Fore.GREEN + "\n[2] MX записи:" + Style.RESET_ALL)
            for mx in mx_records[:3]:
                print(f"    {str(mx.exchange).rstrip('.')}")
        except: pass
        
        #  emailrep.io
        try:
            resp = self.session.get(f"https://emailrep.io/{email}", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                print(Fore.GREEN + "\n[3] emailrep.io:" + Style.RESET_ALL)
                print(f"    Репутация: {data.get('reputation', 'Нет')}")
                print(f"    Спам: {data.get('details', {}).get('spam', 'Нет')}")
                print(f"    Утечки: {data.get('details', {}).get('credentials_leaked', 'Нет')}")
        except: pass
        
        #  haveibeenpwned
        try:
            print(Fore.GREEN + "\n[4] HaveIBeenPwned:" + Style.RESET_ALL)
            print(f"    https://haveibeenpwned.com/account/{email}")
        except: pass
        
        #  hunter.io
        try:
            print(Fore.GREEN + "\n[6] hunter.io:" + Style.RESET_ALL)
            print(f"    https://hunter.io/email-verifier/{email}")
        except: pass

        #  Holehe
        try:
            print(Fore.GREEN + "\n[9] Holehe:" + Style.RESET_ALL)
            print(f"    Запусти: holehe {email}")
        except: pass

        print(Fore.CYAN + f"\n{'='*60}" + Style.RESET_ALL)

    # ========== USERNAME ПРОБИВ (12+ ИСТОЧНИКОВ) ==========
    def username_lookup(self, username):
        print(Fore.CYAN + f"\n{'='*60}")
        print(f"[*] ПОИСК USERNAME: {username}")
        print(f"{'='*60}" + Style.RESET_ALL)
        
        sites = [
            ('VK', f'https://vk.com/{username}'),
            ('Telegram', f'https://t.me/{username}'),
            ('Instagram', f'https://instagram.com/{username}'),
            ('TikTok', f'https://tiktok.com/@{username}'),
            ('YouTube', f'https://youtube.com/@{username}'),
            ('GitHub', f'https://github.com/{username}'),
            ('Twitter', f'https://twitter.com/{username}'),
            ('Twitch', f'https://twitch.tv/{username}'),
            ('Pinterest', f'https://pinterest.com/{username}'),
            ('Steam', f'https://steamcommunity.com/id/{username}'),
            ('Reddit', f'https://reddit.com/user/{username}'),
            ('Facebook', f'https://facebook.com/{username}'),
            ('Discord', f'https://discord.com/users/{username}'),
            ('Tumblr', f'https://{username}.tumblr.com'),
            ('SoundCloud', f'https://soundcloud.com/{username}'),
            ('Spotify', f'https://open.spotify.com/user/{username}'),
        ]
        
        found = 0
        for i, (name, url) in enumerate(sites, 1):
            try:
                resp = self.session.get(url, timeout=5, allow_redirects=True)
                if resp.status_code == 200 and len(resp.text) > 500:
                    print(Fore.GREEN + f"\n[{i}] {name}: НАЙДЕН" + Style.RESET_ALL)
                    print(f"    {url}")
                    found += 1
                else:
                    print(Fore.YELLOW + f"\n[{i}] {name}: НЕ НАЙДЕН" + Style.RESET_ALL)
            except:
                print(Fore.RED + f"\n[{i}] {name}: ОШИБКА" + Style.RESET_ALL)
        
        # Maigret
        try:
            print(Fore.GREEN + f"\n[+] Maigret (3000+ сайтов):" + Style.RESET_ALL)
            print(f"    Запусти: maigret {username} --html")
        except: pass
        
        # Telegram боты для username
        try:
            print(Fore.GREEN + f"\n[+] Telegram боты:" + Style.RESET_ALL)
            print(f"    @usinfobot - инфо по ID")
            print(f"    @SangMata_beta_bot - история смены")
            print(f"    @creationdatebot - дата создания")
        except: pass
        
        print(Fore.CYAN + f"\n{'='*60}")
        print(f"НАЙДЕНО НА {found} САЙТАХ")
        print(f"{'='*60}" + Style.RESET_ALL)

    def run(self):
        self.print_banner()
        while True:
            self.print_menu()
            choice = input("Выбери действие (1-5): ").strip()
            
            if choice == '1':
                ip = input("Введи IP адрес: ").strip()
                self.ip_lookup(ip)
                
            elif choice == '2':
                phone = input("Введи номер телефона (+7XXXXXXXXXX): ").strip()
                self.phone_lookup(phone)
                
            elif choice == '3':
                email = input("Введи email: ").strip()
                self.email_lookup(email)
                
            elif choice == '4':
                username = input("Введи username: ").strip()
                self.username_lookup(username)
                
            elif choice == '5':
                print(Fore.YELLOW + "\nВыход..." + Style.RESET_ALL)
                break
                
            else:
                print(Fore.RED + "Неверный выбор, долбоеб!" + Style.RESET_ALL)
            
            input("\nНажми Enter для продолжения...")

if __name__ == "__main__":
    tool = ProbivSoft()
    try:
        tool.run()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nПОКА, ДОЛБОЕБ!" + Style.RESET_ALL)
    except Exception as e:
        print(Fore.RED + f"\nОшибка: {e}" + Style.RESET_ALL)