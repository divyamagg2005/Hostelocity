"""
Script to initialize the Hostel Management System project
Run this after installing requirements
"""
import os
import sys

def create_directories():
    """Create necessary directories"""
    directories = [
        'media',
        'media/student_photos',
        'staticfiles',
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✓ Created directory: {directory}")

def check_env_file():
    """Check if .env file exists"""
    if not os.path.exists('.env'):
        print("\n⚠ WARNING: .env file not found!")
        print("Please create a .env file with your Supabase credentials.")
        print("You can copy .env.example and fill in your values.\n")
        return False
    print("✓ .env file found")
    return True

def main():
    print("=" * 50)
    print("Hostel Management System - Project Initialization")
    print("=" * 50)
    
    # Create directories
    print("\n1. Creating necessary directories...")
    create_directories()
    
    # Check .env file
    print("\n2. Checking environment configuration...")
    env_exists = check_env_file()
    
    # Instructions
    print("\n" + "=" * 50)
    print("NEXT STEPS:")
    print("=" * 50)
    
    if not env_exists:
        print("1. Create .env file from .env.example")
        print("2. Add your Supabase database credentials")
        print("3. Run: python manage.py makemigrations")
    else:
        print("1. Run: python manage.py makemigrations")
    
    print("2. Run: python manage.py migrate")
    print("3. Run: python manage.py createsuperuser")
    print("4. Run: python manage.py collectstatic")
    print("5. Run: python manage.py runserver")
    print("\n" + "=" * 50)
    print("For detailed instructions, see SETUP_GUIDE.md")
    print("=" * 50)

if __name__ == "__main__":
    main()
