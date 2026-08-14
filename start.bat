@echo off
title RebornRec Local Server Engine
echo =======================================================
echo  Starting RebornRec Local Server Engine...
echo =======================================================
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    pause
    exit
)
echo Checking server dependencies...
pip install flask --quiet
echo Server is running! Keep this window open while playing.
echo Control panel available at: http://localhost:8080
echo =======================================================
python app.py
pause
