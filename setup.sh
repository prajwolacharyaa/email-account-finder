#!/usr/bin/env bash
set -e

echo "[+] Creating Python virtual environment..."
python3 -m venv .venv

echo "[+] Activating virtual environment..."
source .venv/bin/activate

echo "[+] Installing requirements..."
pip install -r requirements.txt

echo "[+] Setup complete."
echo "[+] Run the web app with: source .venv/bin/activate && python app.py"
echo "[+] Run the CLI with: source .venv/bin/activate && python cli.py target@example.com"
