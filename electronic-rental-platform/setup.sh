#!/bin/bash

echo "============================================"
echo "Electronic Rental Platform - Setup Script"
echo "============================================"
echo ""

# Check Python version
echo "Checking Python installation..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo ""
echo "Step 1: Creating virtual environment..."
python3 -m venv venv

echo ""
echo "Step 2: Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Step 3: Upgrading pip..."
pip install --upgrade pip

echo ""
echo "Step 4: Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Step 5: Creating media directories..."
mkdir -p media/products
mkdir -p media/payments
mkdir -p media/qrcodes

echo ""
echo "Step 6: Running database migrations..."
python manage.py makemigrations
python manage.py migrate

echo ""
echo "Step 7: Creating superuser..."
echo "Please enter admin credentials:"
python manage.py createsuperuser

echo ""
echo "============================================"
echo "Setup Complete!"
echo "============================================"
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then open your browser to:"
echo "  Main Site: http://127.0.0.1:8000/"
echo "  Admin Panel: http://127.0.0.1:8000/admin/"
echo "  Screenshots: http://127.0.0.1:8000/screenshots/"
echo ""
echo "============================================"
