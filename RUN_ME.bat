@echo off
title DED ERP Server
echo Starting DED ERP Server...
echo.
echo Server will start at: http://localhost:5000
echo Username: admin
echo Password: admin123
echo.
echo DO NOT CLOSE THIS WINDOW!
echo.
python -u run_server.py
pause

