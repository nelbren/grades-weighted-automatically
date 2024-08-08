#!/bin/bash
if [ ! -r venv/bin/activate ]; then
  echo "Please make my virtual environment! ( ./install.bash )"
  exit 1
fi

source venv/bin/activate

if [ ! -r my_set_env.bash ]; then
  echo "Please make my_set_env.bash! ( ./install.bash )"
  exit 2
fi

source my_set_env.bash

python3 grades-weighted-automatically.py