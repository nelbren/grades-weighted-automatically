#!/bin/bash
if [ ! -r venv/bin/activate ]; then
  echo "Please make my virtual environment! ( python3 -m venv venv )"
  exit 1
fi
source venv/bin/activate
pip install -r requirements.txt
