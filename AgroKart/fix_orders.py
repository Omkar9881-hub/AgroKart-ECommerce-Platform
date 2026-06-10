import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Order, User, Product

print("=== FIXING ORDER SYSTEM ===")

# Check current state
print(f"Total Orders: {Order.objects.count()}")
print(f"Total Users: {User.objects.count()}")
print(f"Total Products: {Product.objects.count()}")

# Get user and product
user = User.objects.first()
product = Product.objects.first()

if not user:
    print("❌ No users found!")
    exit()

if not product:
    print("❌ No products found!")
    exit()

print(f"Using User: {user.username}")
print(f"Using Product: {product.name}")

# Create a test order
print("\nCreating test order...")
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

# Verify order
saved_order = Order.objects.get(id=order.id)
print(f"✅ Order verified: #{saved_order.id}")

# Check user orders
user_orders = Order.objects.filter(user=user)
print(f"📋 Orders for {user.username}: {user_orders.count()}")

# Show all orders
print("\nAll Orders:")
for o in Order.objects.all().order_by('-created_at'):
    print(f"  #{o.id}: {o.user.username} - {o.product_name} - {o.status} - ₹{o.total_price}")

print("\n=== FIX COMPLETE ===")
print("Now test the website:")
print("1. Go to http://127.0.0.1:8000/myorders/")
print("2. You should see the orders listed")
print("3. Check admin panel: http://127.0.0.1:8000/admin/core/order/") 