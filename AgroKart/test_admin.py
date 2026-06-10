#!/usr/bin/env python
"""
Quick script to create test orders for admin panel testing
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.append('c:/Users/User/Desktop/AgroKart')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Order, Product

def create_test_data():
    print("🚀 Creating test data for admin panel...")
    
    # Create test user if doesn't exist
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test Farm, Village, District - 123456'
        }
    )
    if created:
        test_user.set_password('testpass123')
        test_user.save()
        print(f"✅ Created test user: {test_user.username}")
    else:
        print(f"ℹ️ Test user already exists: {test_user.username}")
    
    # Create test products if don't exist
    products_data = [
        {
            'name': 'Premium Wheat Seeds',
            'description': 'High-quality wheat seeds with excellent yield potential',
            'price': 150.00,
            'stock_quantity': 100,
            'category': 'CEREALS'
        },
        {
            'name': 'Hybrid Tomato Seeds',
            'description': 'Disease-resistant hybrid tomato variety',
            'price': 250.00,
            'stock_quantity': 50,
            'category': 'VEGETABLES'
        }
    ]
    
    created_products = []
    for product_data in products_data:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        created_products.append(product)
        if created:
            print(f"✅ Created product: {product.name}")
        else:
            print(f"ℹ️ Product already exists: {product.name}")
    
    # Create test orders with different statuses
    orders_data = [
        {
            'product_name': 'Premium Wheat Seeds',
            'product_price': 150.00,
            'quantity': 2,
            'total_price': 300.00,
            'status': 'pending',
            'shipping_address': 'Test Farm Address, Village, District - 123456',
            'phone_number': '9876543210'
        },
        {
            'product_name': 'Hybrid Tomato Seeds',
            'product_price': 250.00,
            'quantity': 1,
            'total_price': 250.00,
            'status': 'confirmed',
            'shipping_address': 'Another Farm Address, Village, District - 654321',
            'phone_number': '9876543211'
        },
        {
            'product_name': 'Premium Wheat Seeds',
            'product_price': 150.00,
            'quantity': 3,
            'total_price': 450.00,
            'status': 'shipped',
            'shipping_address': 'Third Farm Address, Village, District - 111222',
            'phone_number': '9876543212'
        }
    ]
    
    for order_data in orders_data:
        order, created = Order.objects.get_or_create(
            user=test_user,
            product_name=order_data['product_name'],
            quantity=order_data['quantity'],
            defaults=order_data
        )
        if created:
            print(f"✅ Created order: #{order.id} - {order.product_name} ({order.status})")
        else:
            print(f"ℹ️ Order already exists: #{order.id}")
    
    print(f"\n🎉 Test data creation completed!")
    print(f"📊 Total Orders: {Order.objects.count()}")
    print(f"📦 Total Products: {Product.objects.count()}")
    print(f"👥 Total Users: {User.objects.count()}")
    print(f"\n🔗 Admin Panel: http://127.0.0.1:8000/admin/")
    print(f"📋 Orders List: http://127.0.0.1:8000/admin/core/order/")

if __name__ == '__main__':
    create_test_data()