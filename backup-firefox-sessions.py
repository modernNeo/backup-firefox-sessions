#!/usr/bin/env python
import datetime
import json
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()
PROFILE_LOCATION = os.getenv("PROFILE_LOCATION")
BACKUP_LOCATION = os.getenv("BACKUP_LOCATION")

PROFILE_LOCATION = f"{PROFILE_LOCATION}/recovery.jsonlz4"
FORMATTED_DATE = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
SESSION_STORE_BACKUPS_IDENTIFIER = 'sessionstore-backups'
BACKUP_JSON_LOCATION = f"{BACKUP_LOCATION}/{FORMATTED_DATE}-{SESSION_STORE_BACKUPS_IDENTIFIER}.json"

backup_json_files = sorted(Path(BACKUP_LOCATION).iterdir(), key=os.path.getmtime, reverse=True)
backup_folders_to_delete = backup_json_files[10:]
for backup_folder_to_delete in backup_folders_to_delete:
    backup_folder_to_delete = "/".join(backup_folder_to_delete.parts[1:])
    os.remove(f"/{backup_folder_to_delete}")

command = f"./mozlz4-linux -x '{PROFILE_LOCATION}' > '{BACKUP_JSON_LOCATION}'"
print(command)
subprocess.getstatusoutput(command)

backup_json = json.load(open(BACKUP_JSON_LOCATION))
tab_urls = {}

def add_tab_to_dict(urls, tab_entry):
    if 'url' in tab_entry:
        url = tab_entry['url']
        hostname = urlparse(url).hostname
        if hostname not in urls:
            urls[hostname] = []
        urls[hostname].append({
            'title': tab_entry['title'] if 'title' in tab_entry else None,
            'url': url
        })

for window in backup_json['windows']:
    for tab in window['tabs']:
        for entry in tab['entries']:
            add_tab_to_dict(tab_urls, entry)
    for closedTab in window['_closedTabs']:
        for closedTabEntry in closedTab['state']['entries']:
            add_tab_to_dict(tab_urls, closedTabEntry)
with open(BACKUP_JSON_LOCATION, "w") as f:
    json.dump(tab_urls, f, indent=4)