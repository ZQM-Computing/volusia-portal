#!/bin/bash
# Project Volusia — Database Backup
# Runs daily via crontab

cd "$(dirname "$0")/.." || exit 1

BACKUP_DIR="data/backups"
mkdir -p "$BACKUP_DIR"

DATE=$(date +%Y%m%d_%H%M%S)
cp data/volusia.db "$BACKUP_DIR/volusia.db.$DATE"

# Keep only last 7 days of backups
find "$BACKUP_DIR" -name "volusia.db.*" -mtime +7 -delete 2>/dev/null

echo "Backup created: $BACKUP_DIR/volusia.db.$DATE"
ls -lh "$BACKUP_DIR/volusia.db.$DATE" 2>/dev/null
