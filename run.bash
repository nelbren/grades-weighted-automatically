#!/bin/bash
if [ ! -r venv/bin/activate ]; then
  echo "Please make my virtual environment! ( python3 -m venv venv )"
  exit 1
fi
source venv/bin/activate
if [ ! -r my_set_env.bash ]; then
  echo "Please make my_set_env.bash!"
  echo "  1) cp my_set_env.bash.example my_set_env.bash"
  echo "  2) vi my_set_env.bash"
  exit 2
fi
source my_set_env.bash
#if ! python -c "import requests" 2>/dev/null; then
#  echo "Please install the modules with: install_requirements.bash"
#  exit 3
#fi

python3 grades-weighted-automatically.py
