# backup-firefox-sessions

A Python script to automate the process of backing up your firefox sessions locally because in their infinite wisdom, [firefox decided that such a feature is not necessary](https://support.mozilla.org/en-US/questions/1204253).

[Also had to add a custom binary cause of a wierd format that FireFox uses for compression.](https://superuser.com/a/1563665)

## Installation


obtain `PROFILE_LOCATIONS` from https://www.techrepublic.com/article/how-to-backup-firefox-to-recover-a-potentially-lost-session/

```bash
# optional env variables
PROFILE_LOCATIONS # defaults to "$HOME/.mozilla/firefox"
REPO_LOCATION # defaults to "$HOME/firefox_sessionsstore"
VIRTUAL_ENV_LOCATION # defaults to "$HOME/firefox_sessionsstore"
BACKUP_LOCATION # defaults to "$HOME/firefox_sessionsstore/archives"
VIRTUAL_ENV_NAME # defaults to firefoxSessionStoreArchiver

curl -sSL https://raw.githubusercontent.com/modernNeo/firefox_sessionstore_archiver/master/install_archiver.sh | bash
```