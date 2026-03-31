# How to Start the Server After Closing

Every time you want to run the platform after closing VS Code or terminal, follow these simple steps:

## Method 1: Command Prompt (Recommended for Windows)

1. **Open Command Prompt** (not PowerShell)
   - Press `Win + R`, type `cmd`, press Enter

2. **Navigate to project folder:**
   \`\`\`cmd
   cd C:\Users\HP\Downloads\electronic-rental-platform
   \`\`\`

3. **Activate virtual environment:**
   \`\`\`cmd
   venv\Scripts\activate
   \`\`\`
   - You should see `(venv)` at the start of your command line

4. **Start the server:**
   \`\`\`cmd
   python manage.py runserver
   \`\`\`

5. **Access the platform:**
   - Open browser: `http://127.0.0.1:8000/`
   - Admin login: username `admin`, password `admin123`

## Method 2: VS Code Terminal

1. **Open VS Code**
   - File → Open Folder → Select `electronic-rental-platform`

2. **Open Terminal**
   - Press `Ctrl + ` (backtick)
   - **Important:** Switch to Command Prompt (not PowerShell)
     - Click dropdown next to `+` icon
     - Select "Command Prompt"

3. **Activate and run:**
   \`\`\`cmd
   venv\Scripts\activate
   python manage.py runserver
   \`\`\`

## Quick Start Batch File

I've created `start_server.bat` for you. Just double-click it to start the server!

## Stopping the Server

- Press `Ctrl + C` in the terminal
- Close the terminal window

## Troubleshooting

### Error: "No module named 'django'"
**Solution:** Run `pip install -r requirements.txt` first

### Error: "Port already in use"
**Solution:** 
- Stop any running Django server (Ctrl + C)
- Or use a different port: `python manage.py runserver 8001`

### Error: PowerShell script execution
**Solution:** Use Command Prompt instead of PowerShell
