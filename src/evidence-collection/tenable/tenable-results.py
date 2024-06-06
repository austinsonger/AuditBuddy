import os
import csv
from datetime import datetime
from tenable.io import TenableIO
import schedule
import time

current_year = datetime.utcnow().strftime('%Y')
current_date = datetime.utcnow().strftime('%Y-%m-%d')

CORP_TENABLE_ACCESS_KEY = os.getenv('CORP_TENABLE_ACCESS_KEY')  # 'CORP_TENABLE_ACCESS_KEY'
CORP_TENABLE_SECRET_KEY = os.getenv('CORP_TENABLE_SECRET_KEY')  # 'CORP_TENABLE_SECRET_KEY

# Directory to save CSV files
OUTPUT_DIR = "/evidence-artifacts/private-sector/{current_year}/Tenable"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Tenable.io API
tio = TenableIO(CORP_TENABLE_ACCESS_KEY, CORP_TENABLE_SECRET_KEY)

def fetch_scan_results():
    try:
        # The scans list method provides a comprehensive set of data for each scan
        scans = tio.scans.list()
        return scans
    except Exception as e:
        print(f"Failed to fetch scan results: {str(e)}")
        return []

def save_to_csv(scans):
    if not scans:
        return
    file_name = "{current_date}-tenable-scans.csv"
    file_path = os.path.join(OUTPUT_DIR, file_name)
    keys = scans[0].keys()  # Assumes all scans will have the same set of keys
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        for scan in scans:
            writer.writerow(scan)
    print(f"Scan results saved to {file_path}")

def weekly_job():
    print("Fetching Tenable scan results...")
    scans = fetch_scan_results()
    if scans:
        save_to_csv(scans)

# Schedule the job every week
schedule.every().week.do(weekly_job)

# Main loop to run the scheduled tasks
print("Scheduler started...")
try:
    while True:
        schedule.run_pending()
        time.sleep(60)  # wait one minute
except KeyboardInterrupt:
    print("Scheduler stopped manually.")
