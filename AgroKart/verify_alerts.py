#!/usr/bin/env python
"""
Script to verify that stock alerts have been resolved
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('c:/Users/User/Desktop/AgroKart')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import StockAlert

def verify_alerts():
    """Verify the status of stock alerts"""

    print("🔍 Checking stock alert status...")

    # Check all alerts
    all_alerts = StockAlert.objects.all().order_by('-created_at')

    if not all_alerts.exists():
        print("📭 No stock alerts found in the database")
        return

    resolved_count = 0
    unresolved_count = 0

    print(f"\n📊 Total alerts found: {all_alerts.count()}")
    print("\n" + "="*80)

    for alert in all_alerts:
        status = "✅ RESOLVED" if alert.is_resolved else "❌ UNRESOLVED"
        print(f"{status} | {alert.product.name}")
        print(f"         Message: {alert.message}")
        print(f"         Type: {alert.get_alert_type_display()}")
        print(f"         Created: {alert.created_at}")
        if alert.is_resolved:
            print(f"         Resolved: {alert.resolved_at}")
            resolved_count += 1
        else:
            unresolved_count += 1
        print("-" * 80)

    print("\n📈 Summary:")
    print(f"   ✅ Resolved alerts: {resolved_count}")
    print(f"   ❌ Unresolved alerts: {unresolved_count}")

    if unresolved_count == 0:
        print("\n🎉 All stock alerts have been successfully resolved!")
    else:
        print(f"\n⚠️  {unresolved_count} alerts still need attention")

if __name__ == "__main__":
    print("🚀 Starting alert verification...")
    verify_alerts()
    print("✅ Verification completed!")
