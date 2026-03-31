@echo off
echo ============================================
echo Electronic Rental Platform - Setup Script
echo ============================================
echo.

REM Check Python version
echo Checking Python installation...
python --version

if %errorlevel% neq 0 (
    echo Error: Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

echo.
echo Step 1: Creating virtual environment...
python -m venv venv

echo.
echo Step 2: Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Step 3: Upgrading pip...
python -m pip install --upgrade pip

echo.
echo Step 4: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 5: Creating media directories...
if not exist "media\products" mkdir media\products
if not exist "media\payments" mkdir media\payments
if not exist "media\qrcodes" mkdir media\qrcodes

echo.
echo Step 6: Running database migrations...
python manage.py makemigrations
python manage.py migrate

echo.
echo Step 7: Creating superuser...
echo Please enter admin credentials:
python manage.py createsuperuser

echo.
echo ============================================
echo Setup Complete!
echo ============================================
echo.
echo To start the development server, run:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Then open your browser to:
echo   Main Site: http://127.0.0.1:8000/
echo   Admin Panel: http://127.0.0.1:8000/admin/
echo   Screenshots: http://127.0.0.1:8000/screenshots/
echo.
echo ============================================
pause
