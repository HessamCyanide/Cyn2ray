import requests
import yaml
import schedule
import time
import base64
import os
import re

sources = [
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/Alvin9999/PAC/master/v2ray_config.txt"
]

def fetch_configs():
    configs = []
    v2ray_protocols = ["vmess://", "vless://", "trojan://", "ss://", "socks://", "http://"]
    # فقط آمریکا، آلمان و فنلاند
    country_patterns = [
        r"\b(united ?states|usa|us|america|ashburn|dallas|los angeles|new york|chicago|washington|miami|phoenix|atlanta|seattle|boston|san jose|houston|denver|las vegas|charlotte|detroit|philadelphia|portland|minneapolis|baltimore|cleveland|pittsburgh|orlando|cincinnati|kansas city|sacramento|st louis|salt lake city|raleigh|richmond|columbus|indianapolis|austin|san francisco)\b",
        r"\b(germany|de|berlin|frankfurt|dusseldorf|munich|hamburg|stuttgart)\b",
        r"\b(finland|fi|helsinki|espoo|vantaa|tampere|oulu|turku|lahti|kuopio|jyvaskyla|pori|lappeenranta)\b",
        r"🇺🇸", r"🇩🇪", r"🇫🇮"
    ]
    country_regex = re.compile("|".join(country_patterns), re.IGNORECASE)
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                for line in response.text.splitlines():
                    line = line.strip()
                    if any(line.startswith(proto) for proto in v2ray_protocols):
                        # فقط کانفیگ‌های آمریکا، آلمان و فنلاند
                        if country_regex.search(line):
                            configs.append(line)
        except Exception as e:
            print(f"❌ خطا در دریافت از {url}: {e}")
    return configs

def update_subscription():
    configs = fetch_configs()
    if configs:
        subscription = "\n".join(configs)
        encoded = base64.b64encode(subscription.encode()).decode()
        with open("subscription.txt", "w") as f:
            f.write(encoded)
        print("✅ subscription.txt بروزرسانی شد.")
    else:
        print("⚠️ هیچ کانفیگی دریافت نشد.")

def update_yaml_permissions():
    config_path = "config.yml"
    config = {"permissions": {"read": True, "write": True}}
    with open(config_path, "w") as f:
        yaml.dump(config, f)
    print("🔧 config.yml بروزرسانی شد.")

def job():
    update_subscription()
    update_yaml_permissions()

job()  # اجرای اولیه
