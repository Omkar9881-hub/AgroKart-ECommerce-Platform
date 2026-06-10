#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('c:/Users/User/Desktop/AgroKart')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from django.contrib.auth.models import User

def create_admin():
    """Create admin user"""
    
    # Check if admin already exists
    if User.objects.filter(username='admin').exists():
        print("⚠️ Admin user already exists!")
        admin = User.objects.get(username='admin')
        print(f"👤 Username: {admin.username}")
        print(f"📧 Email: {admin.email}")
        print(f"🔑 Is Superuser: {admin.is_superuser}")
        return
    
    # Create admin user
    admin = User.objects.create_superuser(
        username='admin',
        email='admin@agrokart.com',
        password='admin123',
        first_name='Admin',
        last_name='AgroKart'
    )
    
    print("✅ Admin user created successfully!")
    print(f"👤 Username: {admin.username}")
    print(f"📧 Email: {admin.email}")
    print(f"🔑 Password: admin123")
    print(f"🌐 Admin Panel: http://127.0.0.1:8000/admin/")
    print("\n🎯 Admin can now:")
    print("- View all customer orders")
    print("- See customer names, products, quantities, amounts")
    print("- View order dates and times")
    print("- Only view order history (no edit/delete permissions)")

if __name__ == "__main__":
    create_admin()