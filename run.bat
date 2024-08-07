@ECHO OFF
IF EXIST "venv\Scripts\activate" (
  venv\Scripts\activate
  IF EXIST "my_set_env.bat" (
    call my_set_env.bat
    venv\Scripts\python.exe grades-weighted-automatically.py
  ) ELSE (
    ECHO Please make my_set_env.bat!
    ECHO   1^) copy my_set_env.bat.example my_set_env.bat
    ECHO   2^) notepad my_set_env.bat
  )
  deactivate
) ELSE (
  ECHO Please make my virtual environment! ( python3 -m venv venv ^)
)

