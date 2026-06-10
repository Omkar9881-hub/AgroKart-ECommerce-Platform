#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('c:/Users/User/Desktop/AgroKart')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Product, Order
from django.contrib.auth.models import User
from django.utils import timezone

def test_auto_order_confirmation():
    """Test the automatic order confirmation functionality"""
    
    print("🧪 Testing Automatic Order Confirmation System")
    print("=" * 50)
    
    # Get or create a test user
    user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test Farm Address',
            'last_name': '9876543210'
        }
    )
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Created test user: {user.username}")
    else:
        print(f"📋 Using existing user: {user.username}")
    
    # Get a product to test with
    product = Product.objects.first()
    if not product:
        print("❌ No products found in database")
        print("💡 Please run add_products.py first to create test products")
        return
    
    print(f"📦 Testing with product: {product.name}")
    print(f"💰 Price: ₹{product.price}/kg")
    print(f"📊 Stock before order: {product.stock_quantity}")
    
    # Create a test order (simulating add_to_cart)
    quantity = 2
    total_price = product.price * quantity
    
    # Create order with automatic confirmation
    order = Order.objects.create(
        user=user,
        product_name=product.name,
        product_price=product.price,
        quantity=quantity,
        total_price=total_price,
        shipping_address=user.first_name or "Address not provided",
        phone_number=user.last_name or "Not provided",
        status='confirmed'  # Automatically confirmed
    )
    
    # Update product stock
    product.stock_quantity -= quantity
    product.save()
    
    print(f"\n✅ Order created successfully!")
    print(f"🆔 Order ID: {order.id}")
    print(f"👤 User: {order.user.username}")
    print(f"📦 Product: {order.product_name}")
    print(f"🔢 Quantity: {order.quantity}")
    print(f"💵 Total: ₹{order.total_price}")
    print(f"📍 Address: {order.shipping_address}")
    print(f"📱 Phone: {order.phone_number}")
    print(f"✅ Status: {order.status.upper()} (Automatically Confirmed)")
    print(f"📅 Created: {order.created_at}")
    
    # Test order methods
    print(f"\n🔍 Testing Order Methods:")
    print(f"   Can be edited: {order.can_be_edited()}")
    print(f"   Can be cancelled: {order.can_be_cancelled()}")
    print(f"   Time left for edit: {order.time_left_for_edit()} minutes")
    print(f"   Time left for cancel: {order.time_left_for_cancel()} hours")
    
    # Check admin panel access
    print(f"\n🔗 Admin Panel Information:")
    print(f"   Admin URL: http://127.0.0.1:8000/admin/core/order/")
    print(f"   Order will appear in admin panel with status: {order.get_status_display()}")
    print(f"   Admin can mark as shipped when ready")
    
    # Display all orders for this user
    user_orders = Order.objects.filter(user=user).order_by('-created_at')
    print(f"\n📋 All Orders for {user.username}:")
    print(f"   Total Orders: {user_orders.count()}")
    
    for i, ord in enumerate(user_orders, 1):
        print(f"   {i}. Order #{ord.id}: {ord.product_name} - {ord.status.upper()} - ₹{ord.total_price}")
    
    print(f"\n🎉 Test completed successfully!")
    print(f"💡 The order is now automatically confirmed and ready for admin processing")
    print(f"🚀 You can now test the full flow by:")
    print(f"   1. Running the Django server: python manage.py runserver")
    print(f"   2. Logging in as admin and checking the orders")
    print(f"   3. Marking orders as shipped when ready")

if __name__ == "__main__":
    test_auto_order_confirmation() 