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

def add_products():
    """Add new products to the database"""
    
    # Product 1: Sunflower Seeds
    product1 = Product(
        name="Premium Sunflower Seeds",
        description="High-quality sunflower seeds with excellent oil content and disease resistance. Perfect for commercial farming with guaranteed high yield potential.",
        price=180.00,
        stock_quantity=150,
        category="OILSEEDS",
        is_active=True
    )
    
    # Product 2: Cotton Seeds
    product2 = Product(
        name="Hybrid Cotton Seeds",
        description="Advanced hybrid cotton variety with superior fiber quality and bollworm resistance. Ideal for textile industry requirements.",
        price=320.00,
        stock_quantity=80,
        category="CASH CROPS",
        is_active=True
    )
    
    try:
        # Save products to database
        product1.save()
        product2.save()
        
        print("✅ Products added successfully!")
        print(f"1. {product1.name} - ₹{product1.price}/kg")
        print(f"2. {product2.name} - ₹{product2.price}/kg")
        
    except Exception as e:
        print(f"❌ Error adding products: {e}")

if __name__ == "__main__":
    add_products()