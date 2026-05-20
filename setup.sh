#!/bin/bash

set -e

echo "[+] Updating package index..."
sudo apt update -y

echo "[+] Installing required packages..."
sudo apt install -y python3 python3-pip python3-venv sqlite3

echo "[+] Creating Python virtual environment..."
python3 -m venv .venv

echo "[+] Installing Python dependencies..."
. .venv/bin/activate
pip install --upgrade pip
pip install -r app/requirements.txt

echo "[+] Creating logs directory..."
mkdir -p logs

echo "[+] Seeding database..."
python3 scripts/seed_db.py

echo "[+] Lab setup complete."
echo ""
echo "To start the app, run:"
echo "source .venv/bin/activate"
echo "cd app"
echo "python3 app.py"