@echo off
echo ========================================
echo نظام إدارة المخزون المتكامل
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate
echo.

REM Install requirements
echo Installing requirements...
pip install -r requirements.txt
echo.

REM Check if database exists
if not exist "erp_system.db" (
    echo Initializing database...
    flask init-db
    echo.
)

REM Start the application
echo Starting the application...
echo.
echo ========================================
echo Application is running on http://localhost:5000
echo Username: admin
echo Password: admin123
echo ========================================
echo.
python run.py

pause

