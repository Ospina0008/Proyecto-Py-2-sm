@echo off
title Minecraft Tournament Launcher
cd /d "%~dp0"
"C:\Users\junos\AppData\Local\Python\pythoncore-3.14-64\python.exe" main.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Ocurrio un error al ejecutar la aplicacion.
    pause
)
