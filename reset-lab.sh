#!/bin/bash

set -e

echo "[+] Resetting lab..."

rm -f app/globomantics.db
rm -f logs/app.log

python3 scripts/seed_db.py

git checkout -- app/app.py 2>/dev/null || true

echo "[+] Lab reset complete."