@ECHO OFF
IF EXIST "venv\Scripts\activate" (
  venv\Scripts\activate
  pip install -r requirements.txt
  deactivate
) ELSE (
  ECHO Please make my virtual environment! ( python3 -m venv venv ^)
)
