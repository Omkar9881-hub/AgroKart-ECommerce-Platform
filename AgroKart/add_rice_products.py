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

def add_rice_products():
    """Add rice products to the database"""
    
    rice_products = [
        {
            'name': 'Delhi Rice',
            'description': 'High-quality Delhi rice known for its aroma and taste.',
            'category': 'RICE',
            'category_mr': 'दिल्ली तांदूळ',
            'price': 200.00,
            'stock_quantity': 100,
            'is_active': True
        },
        {
            'name': 'Basmati Rice',
            'description': 'Premium Basmati rice with long grains and aromatic flavor.',
            'category': 'RICE',
            'category_mr': 'बासमती तांदूळ',
            'price': 300.00,
            'stock_quantity': 150,
            'is_active': True
        },
        {
            'name': 'Kolam Rice',
            'description': 'Kolam rice is known for its soft texture and is ideal for daily meals.',
            'category': 'RICE',
            'category_mr': 'कोलम तांदूळ',
            'price': 180.00,
            'stock_quantity': 120,
            'is_active': True
        },
        {
            'name': 'Indrayani Rice',
            'description': 'Indrayani rice is famous for its unique taste and aroma.',
            'category': 'RICE',
            'category_mr': 'इंद्रायणी तांदूळ',
            'price': 250.00,
            'stock_quantity': 80,
            'is_active': True
        }
    ]

    created_count = 0
    for product_data in rice_products:
        product, created = Product.objects.get_or_create(
            name=product_data['name'],
            defaults=product_data
        )
        if created:
            created_count += 1
            print(f'✓ Created: {product.name} - ₹{product.price}/kg')
        else:
            print(f'⚠ Already exists: {product.name}')

    print(f'\n🎉 Successfully added {created_count} rice products to database!')

if __name__ == "__main__":
    add_rice_products()
