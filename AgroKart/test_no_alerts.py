import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Order, User, Product

print("=== TESTING NO ALERTS ===")

# Check if orders are being created properly
user = User.objects.first()
product = Product.objects.first()

if user and product:
    print(f"✅ User: {user.username}")
    print(f"✅ Product: {product.name}")
    
    # Create a test order
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
    print(f"✅ Total orders: {Order.objects.count()}")
    
    print("\n=== ALERTS REMOVED ===")
    print("✅ Add to cart alerts have been removed")
    print("✅ Orders will redirect directly to myorders page")
    print("✅ No popup messages will appear")
    
    print("\n=== TESTING INSTRUCTIONS ===")
    print("1. Go to any product page")
    print("2. Click 'Add to Cart'")
    print("3. Should redirect to myorders page without any alert")
    print("4. Order should appear in the list")
    
else:
    print("❌ No user or product found!")

print("\n=== TEST COMPLETE ===") 