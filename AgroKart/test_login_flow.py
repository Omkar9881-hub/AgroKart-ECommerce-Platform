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
from django.test import Client
from django.urls import reverse

def test_login_flow():
    """Test the complete login/signup flow"""
    
    print("🧪 Testing Login/Signup Flow")
    print("=" * 40)
    
    # Create test client
    client = Client()
    
    # 1. Test Signup
    print("\n📝 Testing Signup...")
    signup_data = {
        'username': 'testuser2',
        'phone': '9876543210',
        'email': 'test2@example.com',
        'location': 'Test City',
        'password': 'testpass123',
        'confirm_password': 'testpass123'
    }
    
    response = client.post(reverse('signup'), signup_data)
    print(f"Signup Response Status: {response.status_code}")
    
    if response.status_code == 302:  # Redirect after successful signup
        print("✅ Signup successful - redirected to login")
    else:
        print("❌ Signup failed")
    
    # 2. Test Login
    print("\n🔐 Testing Login...")
    login_data = {
        'username': 'testuser2',
        'password': 'testpass123'
    }
    
    response = client.post(reverse('login'), login_data)
    print(f"Login Response Status: {response.status_code}")
    
    if response.status_code == 302:  # Redirect after successful login
        print("✅ Login successful - redirected to home")
        
        # Check if user is authenticated
        user = User.objects.get(username='testuser2')
        print(f"👤 User created: {user.username}")
        print(f"📧 Email: {user.email}")
        print(f"📍 Location: {user.first_name}")
        
    else:
        print("❌ Login failed")
    
    # 3. Test existing user count
    total_users = User.objects.filter(is_superuser=False).count()
    print(f"\n👥 Total customers in database: {total_users}")
    
    print("\n✅ Login/Signup Flow Test Complete!")
    print("🌐 Test URLs:")
    print("- Signup: http://127.0.0.1:8000/signup/")
    print("- Login: http://127.0.0.1:8000/login/")
    print("- Home: http://127.0.0.1:8000/")

if __name__ == "__main__":
    test_login_flow()