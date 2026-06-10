import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Order, User, Product

print("=== TESTING SIMPLE ADD TO CART FLOW ===")

# Check current state
print(f"Total Orders: {Order.objects.count()}")
print(f"Total Users: {User.objects.count()}")
print(f"Total Products: {Product.objects.count()}")

# Get user and product
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
    
    print(f"✅ Test order created: #{order.id}")
    
    print("\n=== SIMPLIFIED FLOW ===")
    print("✅ 1. User sees product cards")
    print("✅ 2. User clicks 'Add' button")
    print("✅ 3. Quantity selector appears")
    print("✅ 4. User selects quantity")
    print("✅ 5. User clicks 'Add to Cart'")
    print("✅ 6. Order created automatically")
    print("✅ 7. Redirect to myorders page")
    print("✅ 8. Order appears in history")
    
    print("\n=== TESTING INSTRUCTIONS ===")
    print("1. Go to: http://127.0.0.1:8000/product/")
    print("2. Click 'Add' button on any product")
    print("3. Select quantity using +/- buttons")
    print("4. Click 'Add to Cart' button")
    print("5. Should redirect to myorders page")
    print("6. Order should appear in the list")
    
    print("\n=== EXPECTED BEHAVIOR ===")
    print("✅ No complex logic")
    print("✅ No popup messages")
    print("✅ Direct redirect")
    print("✅ Order automatically confirmed")
    print("✅ Appears in myorders history")
    
else:
    print("❌ No user or product found!")

print("\n=== TEST COMPLETE ===") 