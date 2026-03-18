#!/bin/bash
set -euo pipefail

DOCKER_SERVICE="db"
DOCKER_VOLUME="odoo_data"

if [[ ${1:-} == "staging" ]]; then
  DOCKER_SERVICE="db_staging"
  DOCKER_VOLUME="odoo_data_staging"
fi

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/opt/odoo/backups"
RETENTION_DAYS=7

mkdir -p "${BACKUP_DIR}"

echo "[$(date)] Backup DB..."
docker compose -f /opt/odoo/docker-compose.yml exec -T ${DOCKER_SERVICE} \
    pg_dump -U "${POSTGRES_USER:-odoo}" odoo \
    | gzip > "${BACKUP_DIR}/db_${TIMESTAMP}.sql.gz"

echo "[$(date)] Backup Filestore..."
docker run --rm \
    -v ${DOCKER_VOLUME}:/source:ro \
    -v "${BACKUP_DIR}":/backup \
    alpine tar czf "/backup/filestore_${TIMESTAMP}.tar.gz" -C /source .

echo "[$(date)] Backup done: db_${TIMESTAMP}.sql.gz + filestore_${TIMESTAMP}.tar.gz"

# remove old backups
find "${BACKUP_DIR}" -name "db_*.sql.gz" -mtime +$RETENTION_DAYS -delete
find "${BACKUP_DIR}" -name "filestore_*.tar.gz" -mtime +$RETENTION_DAYS -delete
echo "[$(date)] Cleanup: remove backups older then $RETENTION_DAYS days"
