import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Order, User, Product

print("=== TESTING ADD TO CART BUTTON ===")

# Check current state
print(f"Total Orders: {Order.objects.count()}")
print(f"Total Users: {User.objects.count()}")
print(f"Total Products: {Product.objects.count()}")

# Get user and product
user = User.objects.first()
product = Product.objects.first()

if user and product:
    print(f"✅ User: {user.username}")
    print(f"✅ Product: {product.name} (ID: {product.id})")
    
    print("\n=== TESTING INSTRUCTIONS ===")
    print("1. Go to: http://127.0.0.1:8000/product/")
    print("2. Open browser console (F12)")
    print("3. Click 'Add' button on any product")
    print("4. You should see quantity selector appear")
    print("5. Click 'Add to Cart' button")
    print("6. Check console for debug messages")
    print("7. Should redirect to myorders page")
    
    print("\n=== EXPECTED CONSOLE OUTPUT ===")
    print("Add to cart clicked for product: [product_id]")
    print("addToCartById called with productId: [product_id]")
    print("Found card: [HTML element]")
    print("Quantity: [number]")
    print("Sending request to /add-to-cart/")
    print("Response received: [Response object]")
    print("Data received: [JSON data]")
    print("Success! Redirecting to myorders")
    
    print("\n=== TROUBLESHOOTING ===")
    print("If button doesn't work:")
    print("1. Check if 'Add to Cart' button appears after clicking 'Add'")
    print("2. Check browser console for JavaScript errors")
    print("3. Check if CSRF token is present")
    print("4. Check if user is logged in")
    
    print("\n=== CURRENT ORDERS ===")
    orders = Order.objects.filter(user=user).order_by('-created_at')[:5]
    print(f"Recent orders for {user.username}: {orders.count()}")
    
    for order in orders:
        print(f"  #{order.id}: {order.product_name} - {order.status} - ₹{order.total_price}")
    
else:
    print("❌ No user or product found!")

print("\n=== TEST COMPLETE ===") 