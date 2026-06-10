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

def check_orders():
    """Check all orders in the database"""
    
    print("🔍 Checking All Orders in Database")
    print("=" * 50)
    
    # Check total orders
    total_orders = Order.objects.count()
    print(f"📊 Total Orders in Database: {total_orders}")
    
    if total_orders == 0:
        print("❌ No orders found in database!")
        return
    
    # Check orders by status
    print("\n📋 Orders by Status:")
    print("-" * 30)
    status_counts = {}
    for order in Order.objects.all():
        status = order.status
        if status not in status_counts:
            status_counts[status] = 0
        status_counts[status] += 1
    
    for status, count in status_counts.items():
        print(f"   {status.upper()}: {count}")
    
    # Check orders by user
    print("\n👥 Orders by User:")
    print("-" * 30)
    user_orders = {}
    for order in Order.objects.all():
        username = order.user.username
        if username not in user_orders:
            user_orders[username] = []
        user_orders[username].append(order)
    
    for username, orders in user_orders.items():
        print(f"   {username}: {len(orders)} orders")
        for order in orders[:3]:  # Show first 3 orders per user
            print(f"     - Order #{order.id}: {order.product_name} - {order.status} - ₹{order.total_price}")
        if len(orders) > 3:
            print(f"     ... and {len(orders) - 3} more orders")
    
    # Show recent orders
    print("\n🕒 Recent Orders (Last 10):")
    print("-" * 40)
    recent_orders = Order.objects.all().order_by('-created_at')[:10]
    for order in recent_orders:
        print(f"   #{order.id}: {order.user.username} - {order.product_name} - {order.status} - ₹{order.total_price} - {order.created_at.strftime('%d %b %Y, %I:%M %p')}")
    
    # Check for any issues
    print("\n🔍 Checking for Issues:")
    print("-" * 25)
    
    # Check orders without user
    orphan_orders = Order.objects.filter(user__isnull=True)
    if orphan_orders.exists():
        print(f"   ❌ Found {orphan_orders.count()} orders without user")
    else:
        print("   ✅ All orders have users")
    
    # Check orders without product name
    empty_product_orders = Order.objects.filter(product_name__isnull=True) | Order.objects.filter(product_name='')
    if empty_product_orders.exists():
        print(f"   ❌ Found {empty_product_orders.count()} orders without product name")
    else:
        print("   ✅ All orders have product names")
    
    # Check orders with zero or negative total
    invalid_total_orders = Order.objects.filter(total_price__lte=0)
    if invalid_total_orders.exists():
        print(f"   ❌ Found {invalid_total_orders.count()} orders with invalid total price")
    else:
        print("   ✅ All orders have valid total prices")
    
    print("\n✅ Order check completed!")

def test_order_creation():
    """Test creating a new order"""
    
    print("\n🧪 Testing Order Creation")
    print("=" * 30)
    
    # Get a test user
    user = User.objects.first()
    if not user:
        print("❌ No users found in database")
        return
    
    # Get a product
    product = Product.objects.first()
    if not product:
        print("❌ No products found in database")
        return
    
    print(f"👤 Test User: {user.username}")
    print(f"📦 Test Product: {product.name}")
    print(f"💰 Price: ₹{product.price}/kg")
    print(f"📊 Available Stock: {product.stock_quantity}")
    
    # Create test order
    quantity = 1
    total_price = product.price * quantity
    
    try:
        order = Order.objects.create(
            user=user,
            product_name=product.name,
            product_price=product.price,
            quantity=quantity,
            total_price=total_price,
            shipping_address=user.first_name or "Test Address",
            phone_number=user.last_name or "9876543210",
            status='confirmed'
        )
        
        print(f"✅ Test order created successfully!")
        print(f"   🆔 Order ID: {order.id}")
        print(f"   📦 Product: {order.product_name}")
        print(f"   🔢 Quantity: {order.quantity}")
        print(f"   💵 Total: ₹{order.total_price}")
        print(f"   ✅ Status: {order.status}")
        
        # Verify order was saved
        saved_order = Order.objects.get(id=order.id)
        print(f"✅ Order verified in database - ID: {saved_order.id}")
        
        # Check if order appears in user's orders
        user_orders = Order.objects.filter(user=user)
        print(f"📋 User {user.username} now has {user_orders.count()} orders")
        
    except Exception as e:
        print(f"❌ Error creating test order: {str(e)}")

if __name__ == "__main__":
    check_orders()
    test_order_creation() 