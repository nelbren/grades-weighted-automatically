@ECHO OFF
IF EXIST ".venv\Scripts\activate" (
  .venv\Scripts\activate
  IF EXIST "my_set_env.bat" (
    call my_set_env.bat
    .venv\Scripts\python.exe grades-weighted-automatically.py
  ) ELSE (
    ECHO Please make my_set_env.bat! ^( config.bat ^) 
  )
  deactivate
) ELSE (
  ECHO Please make my virtual environment! ^( install.bat ^)
)