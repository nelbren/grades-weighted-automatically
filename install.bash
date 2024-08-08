#!/bin/bash

echo_ok() {
  echo "✓"
}

echo_fail() {
  echo "×"
}

echo_work() {
  echo "☐"
}

echo -n "Python Install...."
if ! python3 -V > /dev/null; then
  echo_fail
  echo -e "\nPlease manually install Python3"
  exit 1
else
  echo_ok
fi

echo -n "Python Venv......."
if [ ! -r venv/bin/activate ]; then
  echo_work
  echo -e "\npython3 -m venv venv"
  python3 -m venv venv
  
  echo -n "Python Venv......."
  if [ ! -r venv/bin/activate ]; then
    echo_fail
    echo -e "\nPlease manually make my virtual environment! ( python3 -m venv venv )"
    exit 2
  else
    echo_ok
  fi
else
  echo_ok
fi

source venv/bin/activate

echo -n "Python Modules...."
if ! python3 -c "import requests" 2>/dev/null; then
  echo_work
  echo -e "\npip install -r requirements.txt"
  pip install -r requirements.txt
  if ! python3 -c "import requests" 2>/dev/null; then
    echo_fail
    echo -e "\nPlease manually install the modules! ( pip install -r requirements.txt )"
    exit 3
  fi
else
  echo_ok
fi

echo -n "my_set_env.bash..."
if [ ! -r my_set_env.bash ]; then
  echo_work
  echo -e "\ncp my_set_env.bash.example my_set_env.bash"
  cp my_set_env.bash.example my_set_env.bash
  if [ ! -r my_set_env.bash ]; then
    echo_fail
    echo -e "\nPlease manually copy config! ( cp my_set_env.bash.example my_set_env.bash )"
    exit 4
  fi 
else
  echo_ok
  echo -n "INSTRUCTURE_URL..."
  if grep -q replace-with-your-INFRASTRUCTURE-URL_and_rename_this_file my_set_env.bash; then
    echo_fail
    echo -e "\nChange INSTRUCTURE_URL in my_set_env.bash!"
    exit 5
  else
    echo_ok
  fi
  echo -n "API_KEY..........."
  if grep -q replace-with-your-KEY_API_and_rename_this_file my_set_env.bash; then
    echo_fail
    echo -e "\nChange API_KEY in my_set_env.bash!"
    exit 6
  else
    echo_ok
  fi
fi
