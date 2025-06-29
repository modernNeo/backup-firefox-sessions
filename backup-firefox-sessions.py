#!/usr/bin/env python
import datetime
import json
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()
BACKUP_LOCATION = os.getenv("BACKUP_LOCATION")

os.mkdir(BACKUP_LOCATION)
backup_json_files = sorted(Path(BACKUP_LOCATION).iterdir(), key=os.path.getmtime, reverse=True)
backup_json_files_to_delete = backup_json_files[300:] # aiming for at least a day's worth of backups
for backup_json_file_to_delete in backup_json_files_to_delete:
    backup_json_file_to_delete = "/".join(backup_json_file_to_delete.parts[1:])
    os.remove(f"/{backup_json_file_to_delete}")

PROFILE_COMPRESSED_JSON_LOCATION = f"{os.getenv('PROFILE_COMPRESSED_JSON_FOLDER_LOCATION')}/recovery.jsonlz4"
BACKUP_JSON_LOCATION = f"{BACKUP_LOCATION}/{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"

command = f"./mozlz4-linux -x '{PROFILE_COMPRESSED_JSON_LOCATION}' > '{BACKUP_JSON_LOCATION}'"
print(command)
subprocess.getstatusoutput(command)

backup_json = json.load(open(BACKUP_JSON_LOCATION))
tab_urls = {}

def add_tab_to_dict(tab_entry):
    if 'url' in tab_entry:
        url = tab_entry['url']
        hostname = urlparse(url).hostname
        if hostname not in tab_urls:
            tab_urls[hostname] = []
        tab_urls[hostname].append({
            'title': tab_entry['title'] if 'title' in tab_entry else None,
            'url': url
        })

for window in backup_json['windows']:
    for tab in window['tabs']:
        for entry in tab['entries']:
            add_tab_to_dict(entry)
    for closedTab in window['_closedTabs']:
        for closedTabEntry in closedTab['state']['entries']:
            add_tab_to_dict(closedTabEntry)
with open(BACKUP_JSON_LOCATION, "w") as f:
    json.dump(tab_urls, f, indent=4)