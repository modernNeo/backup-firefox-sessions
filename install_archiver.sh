#!/bin/bash -x
set -e

FIREFOX_SESSIONSTORE_FOLDER="firefox_sessionsstore"
REPO_NAME="firefox_sessionstore_archiver"
TEMP_CRON="cron_backup"

if [ -z $PROFILE_LOCATIONS ]; then
    PROFILE_LOCATIONS="$HOME/.mozilla/firefox"
fi

[[ ! -d "${PROFILE_LOCATIONS}" ]] && echo "PROFILE_LOCATIONS of ${PROFILE_LOCATIONS} is not a directory...exiting script" && exit 1

PROFILE_LOCATIONS=$(realpath "$PROFILE_LOCATIONS")

if [ -z $BACKUP_LOCATION ]; then
    BACKUP_LOCATION="$HOME/${FIREFOX_SESSIONSTORE_FOLDER}/archives"
    mkdir -p "${BACKUP_LOCATION}"
fi

[[ ! -d $BACKUP_LOCATION ]] && echo "BACKUP_LOCATION of ${BACKUP_LOCATION} is not a directory...exiting script" && exit 1

BACKUP_LOCATION=$(realpath "$BACKUP_LOCATION")


if [ -z $REPO_LOCATION ]; then
    REPO_LOCATION="$HOME/${FIREFOX_SESSIONSTORE_FOLDER}"
    mkdir -p "${REPO_LOCATION}"
fi

[[ ! -d $REPO_LOCATION ]] && echo "REPO_LOCATION of ${REPO_LOCATION} is not a directory...exiting script" && exit 1

REPO_LOCATION=$(realpath "$REPO_LOCATION")


if [ -z $VIRTUAL_ENV_LOCATION ]; then
    VIRTUAL_ENV_LOCATION="$HOME/${FIREFOX_SESSIONSTORE_FOLDER}"
    mkdir -p "${VIRTUAL_ENV_LOCATION}"
fi

[[ ! -d $VIRTUAL_ENV_LOCATION ]] && echo "VIRTUAL_ENV_LOCATION of ${VIRTUAL_ENV_LOCATION} is not a directory...exiting script" && exit 1

VIRTUAL_ENV_LOCATION=$(realpath "$VIRTUAL_ENV_LOCATION")


if [ -z $VIRTUAL_ENV_NAME ]; then
    VIRTUAL_ENV_NAME="firefoxSessionStoreArchiver"
fi

VIRTUAL_ENV="${VIRTUAL_ENV_LOCATION}/${VIRTUAL_ENV_NAME}"

rm -fr  "${REPO_LOCATION}" || true
rm -r  "${VIRTUAL_ENV}" || true

mkdir -p "${VIRTUAL_ENV_LOCATION}"
mkdir -p "${BACKUP_LOCATION}"

JOB="*/5 * * * * ${REPO_LOCATION}/${REPO_NAME}/backup_firefox.sh"


cd $VIRTUAL_ENV_LOCATION

python3 -m venv ${VIRTUAL_ENV_NAME}

source ${VIRTUAL_ENV}/bin/activate



cd $REPO_LOCATION

git clone https://github.com/modernNeo/${REPO_NAME}.git

cd "${REPO_NAME}"

python3 -m pip install -r requirements.txt

echo "#!/bin/bash


pushd "${REPO_LOCATION}/${REPO_NAME}" && git pull origin master && \
 source ${VIRTUAL_ENV}/bin/activate && \
  ${REPO_LOCATION}/${REPO_NAME}/sessionstore_archiver.py" > "${REPO_LOCATION}/${REPO_NAME}/backup_firefox.sh"


chmod +x "${REPO_LOCATION}/${REPO_NAME}/backup_firefox.sh"

echo "BACKUP_LOCATION=${BACKUP_LOCATION}
PROFILE_LOCATIONS=${PROFILE_LOCATIONS}
" >  "${REPO_LOCATION}/${REPO_NAME}/.env"

. "${REPO_LOCATION}/${REPO_NAME}/backup_firefox.sh"

echo "$JOB" >> "$TEMP_CRON"
crontab "$TEMP_CRON"
rm "$TEMP_CRON"