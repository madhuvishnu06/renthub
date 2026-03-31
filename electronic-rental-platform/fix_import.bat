@echo off
echo Fixing import error in chat/views.py...
python fix_chat_import.py
echo.
echo Done! Now you can run: python manage.py runserver
pause
