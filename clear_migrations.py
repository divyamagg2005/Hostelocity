#!/usr/bin/env python
"""Clear Django migration history from database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hostel_management.settings')
django.setup()

from django.db import connection

with connection.cursor() as cursor:
    # Delete all migration records
    cursor.execute("DELETE FROM django_migrations WHERE app IN ('students', 'rooms', 'payments', 'complaints');")
    print("✅ Cleared migration history for students, rooms, payments, complaints")
    
    # Show remaining migrations
    cursor.execute("SELECT app, name FROM django_migrations ORDER BY app, name;")
    rows = cursor.fetchall()
    print(f"\n📋 Remaining migrations in database:")
    for row in rows:
        print(f"  - {row[0]}.{row[1]}")

print("\n✅ Done! You can now run: python manage.py makemigrations")
