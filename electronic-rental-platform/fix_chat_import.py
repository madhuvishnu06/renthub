import os
import re

# Path to the chat views file
chat_views_path = 'chat/views.py'

# Read the file
with open(chat_views_path, 'r') as f:
    content = f.read()

# Replace CustomUser with User
content = content.replace('from users.models import CustomUser', 'from users.models import User')
content = content.replace('CustomUser', 'User')

# Write back to file
with open(chat_views_path, 'w') as f:
    f.write(content)

print("✓ Fixed chat/views.py import error")
print("Now run: python manage.py runserver")
