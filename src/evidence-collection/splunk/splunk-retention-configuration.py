import requests
import json
import os
from datetime import datetime
import schedule
import time

# Splunk API configuration
CORP_SPLUNK_BASE_URL = os.getenv('CORP_SPLUNK_BASE_URL')  # 'CORP_SPLUNK_BASE_URL'
CORP_SPLUNK_USERNAME = os.getenv('CORP_SPLUNK_USERNAME')  # 'CORP_SPLUNK_USERNAME'
CORP_SPLUNK_PASSWORD = os.getenv('CORP_SPLUNK_PASSWORD')  # 'CORP_SPLUNK_PASSWORD'

# Directory to save JSON files
OUTPUT_DIR = "splunk_retention_configs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def fetch_retention_configs():
    # Endpoint to fetch index settings (including retention policies)
    url = f"{CORP_SPLUNK_BASE_URL}/services/data/indexes"
    headers = {
        "Authorization": f"Basic {CORP_SPLUNK_USERNAME}:{CORP_SPLUNK_PASSWORD}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers, verify=False)  # Set verify=True in production environments
    if response.status_code == 200:
        index_settings = response.json().get('entry', [])
        retention_configs = [
            {
                'title': entry['name'],
                'frozenTimePeriodInSecs': entry['content']['frozenTimePeriodInSecs'],
                'maxTotalDataSizeMB': entry['content']['maxTotalDataSizeMB'],
                'homePath': entry['content']['homePath'],
                'coldPath': entry['content']['coldPath'],
                'thawedPath': entry['content']['thawedPath']
            }
            for entry in index_settings
        ]
        return retention_configs
    else:
        print("Failed to fetch retention configurations, Status Code:", response.status_code)
        return []

def save_to_json(configs):
    file_name = datetime.now().strftime('%Y-%m-%d') + "-splunk-retention-configs.json"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    with open(file_path, 'w') as file:
        json.dump(configs, file, indent=4)
    print(f"Retention configurations saved to {file_path}")

def monthly_job():
    print("Fetching Splunk retention configurations...")
    configs = fetch_retention_configs()
    if configs:
        save_to_json(configs)

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
