#!/bin/python
import datetime
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROFILE_LOCATION = os.getenv("PROFILE_LOCATION")
BACKUP_LOCATION = os.getenv("BACKUP_LOCATION")
FORMATTED_DATE = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

SESSION_STORE_BACKUPS_IDENTIFIER = 'sessionstore-backups'

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

shutil.copytree(PROFILE_LOCATION, f'{BACKUP_LOCATION}/{FORMATTED_DATE}-{SESSION_STORE_BACKUPS_IDENTIFIER}')