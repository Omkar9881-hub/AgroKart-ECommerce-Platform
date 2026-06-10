#!/usr/bin/env python
"""
Script to resolve specific stock alerts for Millet (Bajra) Seeds and Fresh Fenugreek Seeds
"""
import os
import sys
import django
from datetime import datetime

# Setup Django environment
sys.path.append('c:/Users/User/Desktop/AgroKart')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import StockAlert, Product

def resolve_specific_alerts():
    """Resolve the specific stock alerts mentioned by the user"""

    print("🔍 Searching for stock alerts to resolve...")

    # Alert messages to resolve
    alerts_to_resolve = [
        "Millet (Bajra) Seeds has only 1 units remaining. Please restock soon.",
        "Fresh Fenugreek Seeds has only 2 units remaining. Please restock soon."
    ]

    resolved_count = 0

    for alert_message in alerts_to_resolve:
        try:
            # Find the alert by message
            alert = StockAlert.objects.filter(
                message=alert_message,
                is_resolved=False
            ).first()

            if alert:
                print(f"✅ Found alert: {alert_message}")
                print(f"   Product: {alert.product.name}")
                print(f"   Alert Type: {alert.get_alert_type_display()}")
                print(f"   Created: {alert.created_at}")

                # Mark as resolved
                alert.is_resolved = True
                alert.resolved_at = datetime.now()
                alert.save()

                print(f"   ✅ Marked as resolved at {alert.resolved_at}")
                resolved_count += 1
            else:
                print(f"❌ Alert not found: {alert_message}")

        except Exception as e:
            print(f"❌ Error resolving alert '{alert_message}': {str(e)}")

    print(f"\n📊 Summary: {resolved_count} out of {len(alerts_to_resolve)} alerts resolved successfully")

    # Show remaining unresolved alerts
    remaining_alerts = StockAlert.objects.filter(is_resolved=False)
    if remaining_alerts.exists():
        print(f"\n📋 Remaining unresolved alerts: {remaining_alerts.count()}")
        for alert in remaining_alerts[:5]:  # Show first 5
            print(f"   • {alert.product.name}: {alert.message}")
    else:
        print("\n🎉 All stock alerts have been resolved!")

if __name__ == "__main__":
    print("🚀 Starting stock alert resolution process...")
    resolve_specific_alerts()
    print("✅ Process completed!")
