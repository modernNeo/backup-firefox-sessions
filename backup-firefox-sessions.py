#!/usr/bin/env python
import datetime
import json
import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
PROFILE_LOCATION = os.getenv("PROFILE_LOCATION")
BACKUP_LOCATION = os.getenv("BACKUP_LOCATION")


FORMATTED_DATE = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
SESSION_STORE_BACKUPS_IDENTIFIER = 'sessionstore-backups'
BACKUP_JSON_LOCATION = f"{BACKUP_LOCATION}/{FORMATTED_DATE}-{SESSION_STORE_BACKUPS_IDENTIFIER}/backup.json"

backup_folders = sorted(Path(BACKUP_LOCATION).iterdir(), key=os.path.getmtime, reverse=True)
backup_folders = [
    backup_folder for backup_folder in backup_folders
    if SESSION_STORE_BACKUPS_IDENTIFIER in backup_folder.name
]
backup_folders_to_delete = backup_folders[10:]
for backup_folder_to_delete in backup_folders_to_delete:
    backup_folder_to_delete = "/".join(backup_folder_to_delete.parts[1:])
    backup_folder_to_delete = f"/{backup_folder_to_delete}"
    shutil.rmtree(backup_folder_to_delete)

subprocess.getstatusoutput(f"./mozlz4-linux -x {PROFILE_LOCATION}/recovery.jsonlz4 > {BACKUP_JSON_LOCATION}")

backup_json = json.load(open(BACKUP_JSON_LOCATION))
tab_urls = {}
for window in backup_json['windows']:
    for tab in window['tabs']:
        for entry in tab['entries']:
            if 'url' in entry:
                tab_urls[entry['url']] = {
                    'title': entry['title'] if 'title' in entry else None,
                    'url' : entry['url']
                }
    for closedTab in window['_closedTabs']:
        for closedTabEntry in closedTab['state']['entries']:
            if 'url' in closedTabEntry:
                tab_urls[closedTabEntry['url']] = {
                    'title': closedTabEntry['title'] if 'title' in closedTabEntry else None,
                    'url' : closedTabEntry['url']
                }
with open(BACKUP_JSON_LOCATION, "w") as f:
    json.dump(list(tab_urls.values()), f, indent=4)