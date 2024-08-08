@ECHO OFF

REM https://gabimarti.medium.com/personalizando-el-int%C3%A9rprete-de-comandos-de-windows-parte-iv-8b107aedf8d3
CHCP 65001 > NUL
REM https://batcheero.blogspot.com/2007/06/how-to-enabledelayedexpansion.html
setlocal ENABLEDELAYEDEXPANSION

<NUL set /p ="Python Install...."
python3 -V 1>/nul 2>/nul
IF %ERRORLEVEL% == 0 (
    ECHO ✓
) ELSE (
    ECHO ×
    ECHO.
    ECHO Please manually install Python3
    EXIT /B 1
)

<NUL set /p ="Python Venv......."
IF EXIST "venv\Scripts\activate" (
    ECHO ✓
) ELSE (
    ECHO ☐
    ECHO.
    ECHO python3 -m venv venv
    python3 -m venv venv
    ECHO.

    <NUL set /p ="Python Venv......."
    IF EXIST "venv\Scripts\activate" (
        ECHO ✓
    ) ELSE (
        ECHO ×
        ECHO.
        ECHO Please manually make my virtual environment! ^( python3 -m venv venv ^)
        EXIT /B 2
    )
)

call venv\Scripts\activate

<NUL set /p ="Python Modules...."
venv\Scripts\pip.exe list 2>/nul | findstr requests 1>/nul
IF %ERRORLEVEL% == 0 (
    ECHO ✓
) ELSE (
    ECHO ☐
    ECHO.
    ECHO venv\Scripts\pip.exe install -r requirements.txt
    venv\Scripts\pip.exe install -r requirements.txt
    ECHO.
    
    <NUL set /p ="Python Modules...."
    venv\Scripts\pip.exe list 2>/nul | findstr requests 1>/nul
    IF !ERRORLEVEL! == 0 (
        ECHO ✓
    ) ELSE (
        ECHO ×
        ECHO.
        ECHO Please manually install the modules! ^( pip install -r requirements.txt ^)
        EXIT /B 3
    )
)

<NUL set /p ="my_set_env.bat...."
IF EXIST "my_set_env.bat" (
    ECHO ✓
) ELSE (
    ECHO ☐
    ECHO.
    ECHO copy my_set_env.bat.example my_set_env.bat
    copy my_set_env.bat.example my_set_env.bat
    ECHO.

    <NUL set /p ="my_set_env.bat...."
    IF EXIST "my_set_env.bat" (
        ECHO ✓
    ) ELSE (
        ECHO ×
        ECHO.
        ECHO Please manually copy config! ^( copy my_set_env.bat.example my_set_env.bat ^)
        EXIT /B 4
    )
)

<NUL set /p ="INSTRUCTURE_URL..."
type my_set_env.bat | findstr replace-with-your-INFRASTRUCTURE-URL_and_rename_this_file 1>/nul 2>/nul
IF %ERRORLEVEL% == 0 (
    ECHO ×
    ECHO.
    ECHO Change INSTRUCTURE_URL in my_set_env.bat!
    EXIT /B 5
) ELSE (
    ECHO ✓
)

<NUL set /p ="API_KEY..........."
type my_set_env.bat | findstr replace-with-your-KEY_API_and_rename_this_file 1>/nul 2>/nul
IF %ERRORLEVEL% == 0 (
    ECHO ×
    ECHO.
    ECHO Change APY_KEY in my_set_env.bat!
    EXIT /B 6
) ELSE (
    ECHO ✓
)