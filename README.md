# backup-firefox-sessions

A Python script to automate the process of backing up your firefox sessions locally because in their infinite wisdom, [firefox decided that such a feature is not necessary](https://support.mozilla.org/en-US/questions/1204253).

[Also had to add a custom binary cause of a wierd format that FireFox uses for compression.](https://superuser.com/a/1563665)

## Installation

```.dotenv
PROFILE_LOCATION = "<location>"
BACKUP_LOCATION = "<local_location_anywhere_on_computer>"
```

obtain `PROFILE_LOCATION` from https://www.techrepublic.com/article/how-to-backup-firefox-to-recover-a-potentially-lost-session/

## CronTab Installation

create the file `backup_firefox.sh`
```shell
#!/bin/bash


pushd /path/to/repository/ && git pull origin master && \
 source path/to/virtual_env/bin/activate && \
  /path/to/repository/backup-firefox-sessions.py
```
[Cron String Generator](https://crontab.guru/)
```shell
*/5 * * * * /path/to/backup_firefox.sh
```