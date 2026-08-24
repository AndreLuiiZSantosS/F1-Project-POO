@echo off
set "ROOT=%~dp0"
set "NODE=%ProgramFiles%\nodejs\node.exe"
start "F1 Results API" /min /d "%ROOT%" "%NODE%" api\src\server.js
start "F1 Results Frontend" /min /d "%ROOT%" "%NODE%" frontend\server.js
start "" http://127.0.0.1:5173
