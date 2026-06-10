import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Order, User, Product

print("=== QUICK ORDER CHECK ===")
print(f"Total Orders: {Order.objects.count()}")
print(f"Total Users: {User.objects.count()}")
print(f"Total Products: {Product.objects.count()}")

if Order.objects.count() > 0:
    print("\nRecent Orders:")
    for order in Order.objects.all().order_by('-created_at')[:5]:
        print(f"Order #{order.id}: {order.user.username} - {order.product_name} - {order.status}")
else:
    print("No orders found!")

print("=== CHECK COMPLETE ===")  