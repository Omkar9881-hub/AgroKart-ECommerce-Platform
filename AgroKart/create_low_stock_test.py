#!/usr/bin/env python
"""
Create Low Stock Test - Manually set products to low stock for testing
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Product, StockAlert

def create_low_stock_test():
    """Create low stock scenarios for testing"""
    print("🧪 Creating Low Stock Test Scenarios")
    print("=" * 50)
    
    # Get some products and set them to low stock
    products = Product.objects.all()[:5]  # Get first 5 products
    
    for i, product in enumerate(products):
        if i == 0:
            # Set first product to very low stock (1 unit)
            product.stock_quantity = 1
            print(f"📉 Set {product.name} stock to 1 unit")
        elif i == 1:
            # Set second product to low stock (3 units)
            product.stock_quantity = 3
            print(f"📉 Set {product.name} stock to 3 units")
        elif i == 2:
            # Set third product to out of stock (0 units)
            product.stock_quantity = 0
            print(f"📉 Set {product.name} stock to 0 units (out of stock)")
        elif i == 3:
            # Set fourth product to critical stock (2 units)
            product.stock_quantity = 2
            print(f"📉 Set {product.name} stock to 2 units")
        else:
            # Set fifth product to normal stock (10 units)
            product.stock_quantity = 10
            print(f"📉 Set {product.name} stock to 10 units (normal)")
        
        product.save()
    
    # Create alerts for low stock products
    print("\n🔔 Creating stock alerts...")
    new_alerts = []
    
    for product in products:
        if product.stock_quantity <= 5 and product.stock_quantity > 0:
            alert = StockAlert.create_low_stock_alert(product)
            if alert:
                new_alerts.append(alert)
                print(f"  ✅ Created low stock alert for: {product.name} ({product.stock_quantity} units)")
        
        if product.stock_quantity == 0:
            alert = StockAlert.create_out_of_stock_alert(product)
            if alert:
                new_alerts.append(alert)
                print(f"  ✅ Created out of stock alert for: {product.name}")
    
    # Get all active alerts
    active_alerts = StockAlert.objects.filter(is_resolved=False)
    print(f"\n📊 Total active alerts: {active_alerts.count()}")
    
    if active_alerts.exists():
        print("\n📋 Active Alerts:")
        for alert in active_alerts:
            print(f"  • {alert.product.name}: {alert.message}")
            print(f"    Stock: {alert.stock_quantity} units")
            print(f"    Type: {alert.alert_type}")
            print(f"    Status: {'Read' if alert.is_read else 'Unread'}")
            print()
    
    print("✅ Low Stock Test Scenarios Created!")
    print(f"📈 Created {len(new_alerts)} new alerts")
    print("\n🌐 Now check the owner dashboard at: http://localhost:8000/owner/")
    print("🔔 You should see notification badge on the bell icon!")
    
    return len(new_alerts)

if __name__ == "__main__":
    try:
        create_low_stock_test()
    except Exception as e:
        print(f"❌ Error creating low stock test: {e}")
        sys.exit(1) 