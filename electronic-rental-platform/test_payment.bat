@echo off
echo Testing Payment System...
echo.

call venv\Scripts\activate.bat
python check_payment_system.py

echo.
pause
