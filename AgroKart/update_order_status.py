import os
import django
import sys

# Setup Django environment for standalone script
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Order

def update_order_status_to_shipped(order_id):
    try:
        order = Order.objects.get(id=order_id)
        if order.status == 'shipped':
            print(f"Order #{order_id} is already marked as shipped.")
            return
        order.status = 'shipped'
        order.save()
        print(f"Order #{order_id} status updated to 'shipped'.")
        print(f"Order Details:")
        print(f"  Product Name: {order.product_name}")
        print(f"  Quantity: {order.quantity}")
        print(f"  Total Price: ₹{order.total_price}")
        print(f"  Status: {order.status}")
    except Order.DoesNotExist:
        print(f"Order with ID {order_id} does not exist.")

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python update_order_status.py <order_id>")
        sys.exit(1)
    order_id = sys.argv[1]
    if not order_id.isdigit():
        print("Order ID must be a numeric value.")
        sys.exit(1)
    update_order_status_to_shipped(int(order_id))
