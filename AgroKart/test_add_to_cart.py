import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Order, User, Product
from django.test import Client
import json

print("=== TESTING ADD TO CART FUNCTIONALITY ===")

# Check current state
print(f"Total Orders: {Order.objects.count()}")
print(f"Total Users: {User.objects.count()}")
print(f"Total Products: {Product.objects.count()}")

# Get user and product
user = User.objects.first()
product = Product.objects.first()

if not user or not product:
    print("❌ No user or product found!")
    exit()

print(f"✅ User: {user.username}")
print(f"✅ Product: {product.name} (ID: {product.id})")

# Test backend add-to-cart endpoint
client = Client()
client.force_login(user)

print(f"\n=== TESTING BACKEND ENDPOINT ===")
print(f"Testing /add-to-cart/ with product_id={product.id}, quantity=1")

response = client.post('/add-to-cart/', 
    data=json.dumps({'product_id': product.id, 'quantity': 1}),
    content_type='application/json'
)

print(f"Response status: {response.status_code}")
print(f"Response content: {response.content.decode()}")

if response.status_code == 200:
    data = json.loads(response.content)
    print(f"✅ Backend response: {data}")
    
    if data.get('success'):
        print("✅ Backend add-to-cart working!")
        
        # Check if order was created
        latest_order = Order.objects.filter(user=user).order_by('-created_at').first()
        if latest_order:
            print(f"✅ Order created: #{latest_order.id}")
            print(f"✅ Order status: {latest_order.status}")
            print(f"✅ Order product: {latest_order.product_name}")
            print(f"✅ Order quantity: {latest_order.quantity}")
            print(f"✅ Order total: ₹{latest_order.total_price}")
        else:
            print("❌ No order found in database")
    else:
        print(f"❌ Backend error: {data.get('message', 'Unknown error')}")
else:
    print(f"❌ Backend request failed: {response.status_code}")

print(f"\n=== CURRENT ORDERS ===")
orders = Order.objects.filter(user=user).order_by('-created_at')
print(f"Total orders for {user.username}: {orders.count()}")

for order in orders[:5]:  # Show last 5 orders
    print(f"  #{order.id}: {order.product_name} - {order.status} - ₹{order.total_price}")

print("\n=== TESTING INSTRUCTIONS ===")
print("1. Go to: http://127.0.0.1:8000/product/")
print("2. Open browser console (F12)")
print("3. Click 'Add' button on any product")
print("4. Select quantity using +/- buttons")
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

print("\n=== TEST COMPLETE ===") 