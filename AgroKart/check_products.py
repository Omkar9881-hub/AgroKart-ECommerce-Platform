#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('c:/Users/User/Desktop/AgroKart')

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Agrokart.settings')
django.setup()

from core.models import Product

def check_products():
    """Check all products in database"""
    products = Product.objects.all()
    
    print(f"📦 Total products in database: {products.count()}")
    print("\n🌾 All Products:")
    print("-" * 50)
    
    for i, product in enumerate(products, 1):
        print(f"{i}. {product.name}")
        print(f"   Category: {product.category}")
        print(f"   Price: ₹{product.price}/kg")
        print(f"   Stock: {product.stock_quantity} units")
        print(f"   Active: {'✅' if product.is_active else '❌'}")
        print(f"   Created: {product.created_at.strftime('%Y-%m-%d %H:%M')}")
        print()

if __name__ == "__main__":
    check_products()