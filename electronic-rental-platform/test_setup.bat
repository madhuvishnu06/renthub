@echo off
echo ====================================
echo Electronic Rental Platform Test Setup
echo ====================================
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Creating test data...
python create_test_data.py

echo.
echo Starting development server...
echo.
echo The server will start at: http://127.0.0.1:8000/
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
