# backup-firefox-sessions

A Python script to automate the process of backing up your firefox sessions locally because in their infinite wisdom, [firefox decided that such a feature is not necessary](https://support.mozilla.org/en-US/questions/1204253).

## Installation

```.dotenv
PROFILE_LOCATION = "<location>"
BACKUP_LOCATION = "<local_location_anywhere_on_computer"
```

obtain `PROFILE_LOCATION` from https://www.techrepublic.com/article/how-to-backup-firefox-to-recover-a-potentially-lost-session/

## CronTab Installation
[Cron String Generator](https://crontab.guru/)
```bash
*/5 * * * * /path/to/backup-firefox-sessions.py
```