#!/bin/bash
cd "$(dirname "$0")"
echo "Starting Backtest Bench setup..."
echo
if command -v python3 >/dev/null 2>&1; then
  python3 get_data.py
else
  echo "Python is not installed on this Mac."
  echo
  echo "1. Go to https://www.python.org/downloads/ and click the yellow Download button."
  echo "2. Open the downloaded file and follow the installer."
  echo "3. When it finishes, double-click start-mac.command again."
fi
echo
read -p "Press Enter to close this window."
