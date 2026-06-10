import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Order, User, Product

print("=== SIMPLE ORDER TEST ===")

# Get user and product
user = User.objects.first()
product = Product.objects.first()

print(f"User: {user.username if user else 'None'}")
print(f"Product: {product.name if product else 'None'}")

if user and product:
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
    
    # Check total orders
    total = Order.objects.count()
    print(f"Total orders: {total}")
    
    # Check user orders
    user_orders = Order.objects.filter(user=user)
    print(f"Orders for {user.username}: {user_orders.count()}")
    
    # Show recent orders
    print("\nRecent orders:")
    for o in Order.objects.all().order_by('-created_at')[:3]:
        print(f"  #{o.id}: {o.user.username} - {o.product_name} - {o.status}")
else:
    print("❌ No user or product found!")

print("=== TEST DONE ===") 