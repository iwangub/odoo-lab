#!/usr/bin/env bash
set -euo pipefail

COMPOSE_FILE="/opt/odoo/docker-compose.yml"
BACKUP_DIR="/opt/odoo/backup/tmp"

SRC_DB_SERVICE="db"
SRC_FILESTORE_VOLUME="odoo_data"

DST_ODOO_SERVICE="odoo_staging"
DST_DB_SERVICE="db_staging"
DST_FILESTORE_VOLUME="odoo_data_staging"

DB_NAME="odoo"
DB_USER="odoo"

DB_ARCHIVE="prod.sql.gz"
FILESTORE_ARCHIVE="prod_filestore.tar.gz"

mkdir -p "${BACKUP_DIR}"

# Backup src DB
docker compose -f "${COMPOSE_FILE}" exec -T "${SRC_DB_SERVICE}" \
  pg_dump -U "${DB_USER}" "${DB_NAME}" | gzip > "${BACKUP_DIR}/${DB_ARCHIVE}"

# Backup src filestore
docker run --rm \
  -v "${SRC_FILESTORE_VOLUME}:/source:ro" \
  -v "${BACKUP_DIR}:/backup" \
  alpine tar czf "/backup/${FILESTORE_ARCHIVE}" -C /source .

docker compose -f "${COMPOSE_FILE}" stop "${DST_ODOO_SERVICE}"

# Close dst DB connections
docker compose -f "${COMPOSE_FILE}" exec -T "${DST_DB_SERVICE}" \
  psql -U "${DB_USER}" postgres -c "
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = '${DB_NAME}'
      AND pid <> pg_backend_pid();
  "

docker compose -f "${COMPOSE_FILE}" exec -T "${DST_DB_SERVICE}" \
  psql -U "${DB_USER}" postgres -c "DROP DATABASE IF EXISTS ${DB_NAME};"

docker compose -f "${COMPOSE_FILE}" exec -T "${DST_DB_SERVICE}" \
  psql -U "${DB_USER}" postgres -c "CREATE DATABASE ${DB_NAME};"

# Restore dst DB
gunzip -c "${BACKUP_DIR}/${DB_ARCHIVE}" | \
  docker compose -f "${COMPOSE_FILE}" exec -T "${DST_DB_SERVICE}" \
  psql -U "${DB_USER}" "${DB_NAME}"

# Restore dst filestore
docker run --rm \
  -v "${DST_FILESTORE_VOLUME}:/target" \
  -v "${BACKUP_DIR}:/backup" \
  alpine sh -c '
    set -eu
    rm -rf /target/*
    tar xzf /backup/'"${FILESTORE_ARCHIVE}"' -C /target
  '

docker compose -f "${COMPOSE_FILE}" start "${DST_ODOO_SERVICE}"

rm -f "${BACKUP_DIR}/${DB_ARCHIVE}" "${BACKUP_DIR}/${FILESTORE_ARCHIVE}"

echo "Done."
