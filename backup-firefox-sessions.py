#!/usr/bin/env python
import datetime
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from dotenv import load_dotenv

load_dotenv()
BACKUP_LOCATION = os.getenv("BACKUP_LOCATION")

PROFILE_LOCATIONS = os.getenv('PROFILE_LOCATIONS')
if not os.path.isdir(BACKUP_LOCATION):
    raise Exception(f"'{BACKUP_LOCATION}' is not a valid directory")
if not os.path.isdir(PROFILE_LOCATIONS):
    raise Exception(f"there are no firefox profiles located under '{PROFILE_LOCATIONS}'")
for profile in os.listdir(PROFILE_LOCATIONS):
    if re.match(r"\w{8}.\d+.", profile):
        PROFILE_BACKUP_LOCATION = os.path.join(BACKUP_LOCATION, profile)
        Path(PROFILE_BACKUP_LOCATION).mkdir(parents=True, exist_ok=True)
        backup_json_files = sorted(Path(PROFILE_BACKUP_LOCATION).iterdir(), key=os.path.getmtime, reverse=True)
        backup_json_files_to_delete = backup_json_files[300:]  # aiming for at least a day's worth of backups
        for backup_json_file_to_delete in backup_json_files_to_delete:
            backup_json_file_to_delete = "/".join(backup_json_file_to_delete.parts[1:])
            os.remove(f"/{backup_json_file_to_delete}")
        BACKUP_JSON_LOCATION = os.path.join(PROFILE_BACKUP_LOCATION, f"{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json")


        profile_path = os.path.join(PROFILE_LOCATIONS, profile, "sessionstore-backups", "recovery.jsonlz4")
        if not os.path.exists(profile_path):
            profile_path = os.path.join(PROFILE_LOCATIONS, profile, "sessionstore-backups", "previous.jsonlz4")
        if not os.path.exists(profile_path):
            continue
        command = f"./mozlz4-linux -x '{profile_path}' > '{BACKUP_JSON_LOCATION}'"
        print(command)
        output = subprocess.getstatusoutput(command)

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