import requests
import json
import os
from datetime import datetime
import schedule
import time

current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

# Cloudflare API configuration
CORP_CLOUDFLARE_EMAIL = os.getenv('CORP_CLOUDFLARE_EMAIL')
CORP_CLOUDFLARE_API_KEY = os.getenv('CORP_CLOUDFLARE_API_KEY')
CORP_CLOUDFLARE_ZONE_ID = os.getenv('CORP_CLOUDFLARE_ZONE_ID')
CORP_CLOUDFLARE_URL = f"https://api.cloudflare.com/client/v4/zones/{CLOUDFLARE_ZONE_ID}/firewall/rules"

# Directory to save JSON files
OUTPUT_DIR = "/evidence-artifacts/private-sector/{current_year}/cloudflare"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_firewall_rules():
    headers = {
        "X-Auth-Email": CLOUDFLARE_EMAIL,
        "X-Auth-Key": CLOUDFLARE_API_KEY,
        "Content-Type": "application/json"
    }
    
    response = requests.get(CLOUDFLARE_URL, headers=headers)
    if response.status_code == 200:
        rules = response.json().get('result', [])
        return rules
    else:
        print("Failed to fetch firewall rules, Status Code:", response.status_code)
        return []

def save_to_json(rules):
    file_name = "{current_date}-cloudflare-firewall-rules.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(rules, file, indent=4)
    print(f"Firewall rules saved to {file_path}")

def monthly_job():
    print("Fetching Cloudflare firewall rules...")
    rules = fetch_firewall_rules()
    if rules:
        save_to_json(rules)

# Schedule the job every month
schedule.every().month.do(monthly_job)

# Main loop to run the scheduled tasks
print("Scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
except KeyboardInterrupt:
    print("Scheduler stopped manually.")
