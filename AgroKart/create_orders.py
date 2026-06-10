import os
import django
import sys

# Setup Django
sys.path.append('c:/Users/User/Desktop/AgroKart')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import Order, Product

# Get first user (admin)
user = User.objects.first()
print(f"Creating orders for user: {user.username}")

# Create sample orders
orders_data = [
    {
        'user': user,
        'product_name': 'Premium Wheat Seeds',
        'product_price': 150.00,
        'quantity': 2,
        'total_price': 300.00,
        'status': 'pending',
        'shipping_address': 'Farm Address, Village, District - 123456',
        'phone_number': '9876543210'
    },
    {
        'user': user,
        'product_name': 'Hybrid Tomato Seeds',
        'product_price': 250.00,
        'quantity': 1,
        'total_price': 250.00,
        'status': 'confirmed',
        'shipping_address': 'Another Farm, Village, District - 654321',
        'phone_number': '9876543211'
    },
    {
        'user': user,
        'product_name': 'Cotton Seeds Premium',
        'product_price': 320.00,
        'quantity': 1,
        'total_price': 320.00,
        'status': 'shipped',
        'shipping_address': 'Third Farm, Village, District - 111222',
        'phone_number': '9876543212'
    }
]

for order_data in orders_data:
    order = Order.objects.create(**order_data)
    print(f"✅ Created Order #{order.id}: {order.product_name} - {order.status}")

print(f"\n🎉 Created {len(orders_data)} test orders!")
print(f"📊 Total Orders: {Order.objects.count()}")
print(f"🔗 Admin Panel: http://127.0.0.1:8000/admin/core/order/")