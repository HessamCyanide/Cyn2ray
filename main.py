import requests
import yaml
import schedule
import time
import base64
import os

sources = [
    "https://raw.githubusercontent.com/mahdibland/V2RayAggregator/master/sub/sub_merge.txt",
    "https://raw.githubusercontent.com/Alvin9999/PAC/master/v2ray_config.txt"
]

def fetch_configs():
    configs = []
    for url in sources:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                for line in response.text.splitlines():
                    if line.startswith("vmess://") or line.startswith("vless://") or line.startswith("trojan://"):
                        configs.append(line.strip())
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
