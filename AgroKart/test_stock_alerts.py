#!/usr/bin/env python
"""
Test script for Stock Alert System
This script tests the backend stock alert functionality
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Product, StockAlert

def test_stock_alert_system():
    """Test the stock alert system"""
    print("🧪 Testing Stock Alert System")
    print("=" * 50)
    
    # Get all products
    products = Product.objects.all()
    print(f"📦 Found {products.count()} products in database")
    
    # Check for low stock products
    low_stock_products = [p for p in products if p.stock_quantity <= 5 and p.stock_quantity > 0]
    out_of_stock_products = [p for p in products if p.stock_quantity == 0]
    
    print(f"⚠️  Products with low stock (≤5): {len(low_stock_products)}")
    print(f"🚫 Products out of stock: {len(out_of_stock_products)}")
    
    # Create alerts for low stock products
    print("\n🔔 Creating stock alerts...")
    new_alerts = []
    
    for product in low_stock_products:
        alert = StockAlert.create_low_stock_alert(product)
        if alert:
            new_alerts.append(alert)
            print(f"  ✅ Created low stock alert for: {product.name} ({product.stock_quantity} units)")
    
    for product in out_of_stock_products:
        alert = StockAlert.create_out_of_stock_alert(product)
        if alert:
            new_alerts.append(alert)
            print(f"  ✅ Created out of stock alert for: {product.name}")
    
    # Get all active alerts
    active_alerts = StockAlert.objects.filter(is_resolved=False)
    print(f"\n📊 Total active alerts: {active_alerts.count()}")
    
    if active_alerts.exists():
        print("\n📋 Active Alerts:")
        for alert in active_alerts[:5]:  # Show first 5 alerts
            print(f"  • {alert.product.name}: {alert.message}")
            print(f"    Created: {alert.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"    Status: {'Read' if alert.is_read else 'Unread'}")
            print()
    
    # Test API endpoints (simulate)
    print("🌐 API Endpoints Available:")
    print("  • GET /api/stock-alerts/ - Get all alerts")
    print("  • GET /api/stock-alerts/count/ - Get alert count")
    print("  • POST /api/stock-alerts/check/ - Check for new alerts")
    print("  • POST /api/stock-alerts/clear-all/ - Mark all as read")
    print("  • POST /api/stock-alerts/mark-read/ - Mark specific alert as read")
    print("  • POST /api/stock-alerts/mark-resolved/ - Mark specific alert as resolved")
    
    print("\n✅ Stock Alert System Test Complete!")
    print(f"📈 Created {len(new_alerts)} new alerts")
    
    return len(new_alerts)

if __name__ == "__main__":
    try:
        test_stock_alert_system()
    except Exception as e:
        print(f"❌ Error testing stock alert system: {e}")
        sys.exit(1) 