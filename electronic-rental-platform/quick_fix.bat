@echo off
echo ========================================
echo Electronic Rental Platform - Quick Fix
echo ========================================
echo.
echo This will reset your database and create all tables
echo.
pause

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Run the force migrations script
python force_migrations.py

echo.
echo ========================================
echo Database is ready!
echo ========================================
echo.
echo Now create your admin account:
python manage.py createsuperuser

echo.
echo Starting development server...
python manage.py runserver
