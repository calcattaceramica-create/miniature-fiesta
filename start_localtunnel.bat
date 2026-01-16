@echo off
chcp 65001 >nul
color 0B
title LocalTunnel - dedapp

echo.
echo ═══════════════════════════════════════════════════════════════
echo                    🌍 LocalTunnel Starting...
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🔄 Connecting to LocalTunnel...
echo.

lt --port 5000 --subdomain dedapp

echo.
echo ❌ LocalTunnel stopped!
echo.
pause

