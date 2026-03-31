@echo off
echo ========================================
echo   Electronic Rental Platform Server
echo ========================================
echo.

cd /d "%~dp0"

if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found!
    echo Please run setup first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Django development server...
echo.
echo Access the platform at: http://127.0.0.1:8000/
echo Admin login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python manage.py runserver

pause
