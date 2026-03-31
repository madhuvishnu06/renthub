@echo off
echo ============================================================
echo FIXING DATABASE ISSUES - ELECTRONIC RENTAL PLATFORM
echo ============================================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Creating migrations for all apps...
python manage.py makemigrations users
python manage.py makemigrations products
python manage.py makemigrations bookings
python manage.py makemigrations payments
python manage.py makemigrations chat
python manage.py makemigrations adminpanel

echo.
echo Applying all migrations...
python manage.py migrate

echo.
echo ============================================================
echo DATABASE SETUP COMPLETE!
echo ============================================================
echo.
echo You can now run: python manage.py runserver
echo.
pause
