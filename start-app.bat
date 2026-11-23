@echo off
set "ROOT=%~dp0"
set "NODE=%ProgramFiles%\nodejs\node.exe"
if not defined ADMIN_EMAIL (
    echo Configure ADMIN_EMAIL and ADMIN_PASSWORD before starting the application.
    exit /b 1
)
if not defined ADMIN_PASSWORD (
    echo Configure ADMIN_EMAIL and ADMIN_PASSWORD before starting the application.
    exit /b 1
)
start "F1 Results API" /min /d "%ROOT%" "%NODE%" api\src\server.js
start "F1 Results Frontend" /min /d "%ROOT%" "%NODE%" frontend\server.js
start "" http://127.0.0.1:5173
