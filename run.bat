@ECHO OFF
IF EXIST "venv\Scripts\activate" (
  venv\Scripts\activate
  IF EXIST "my_set_env.bat" (
    call my_set_env.bat
    REM python -c "import requests" 2>nul
    REM IF %ERRORLEVEL% == 0 (
    venv\Scripts\python.exe grades-weighted-automatically.py
    REM ) ELSE (
    REM   ECHO Please install the modules with: install_requirements.bat
    REM )
  ) ELSE (
    ECHO Please make my_set_env.bat!
    ECHO   1^) copy my_set_env.bat.example my_set_env.bat
    ECHO   2^) notepad my_set_env.bat
  )
  deactivate
) ELSE (
  ECHO Please make my virtual environment! ( python3 -m venv venv ^)
)
