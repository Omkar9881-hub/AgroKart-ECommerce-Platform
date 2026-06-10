#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('c:/Users/User/Desktop/AgroKart')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Order, User, Product

print("=== TESTING ORDER CREATION ===")

# Get first user and product
user = User.objects.first()
product = Product.objects.first()

if not user or not product:
    print("❌ No user or product found!")
    exit()

print(f"User: {user.username}")
print(f"Product: {product.name}")

# Create order
order = Order.objects.create(
    user=user,
    product_name=product.name,
    product_price=product.price,
    quantity=1,
    total_price=product.price,
    shipping_address="Test Address",
    phone_number="1234567890",
    status='confirmed'
)

print(f"✅ Order created: #{order.id}")
print(f"Total orders now: {Order.objects.count()}")

# Check if order appears for user
user_orders = Order.objects.filter(user=user)
print(f"Orders for {user.username}: {user_orders.count()}")

print("=== TEST COMPLETE ===")