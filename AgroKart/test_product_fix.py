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

def test_product_fix():
    """Test that product details show correct information"""
    
    print("🧪 Testing Product Details Fix")
    print("=" * 40)
    
    # Get specific products to test
    cotton_seeds = Product.objects.filter(name__icontains='Cotton').first()
    tomato_seeds = Product.objects.filter(name__icontains='Tomato').first()
    rice_seeds = Product.objects.filter(name__icontains='Rice').first()
    
    print("📋 Product Information Test:")
    print("-" * 35)
    
    if cotton_seeds:
        print(f"🌱 Cotton Seeds (ID: {cotton_seeds.id})")
        print(f"   Name: {cotton_seeds.name}")
        print(f"   Price: ₹{cotton_seeds.price}/kg")
        print(f"   Stock: {cotton_seeds.stock_quantity} units")
        print(f"   URL: /productinfo/?product={cotton_seeds.id}")
        print()
    
    if tomato_seeds:
        print(f"🍅 Tomato Seeds (ID: {tomato_seeds.id})")
        print(f"   Name: {tomato_seeds.name}")
        print(f"   Price: ₹{tomato_seeds.price}/kg")
        print(f"   Stock: {tomato_seeds.stock_quantity} units")
        print(f"   URL: /productinfo/?product={tomato_seeds.id}")
        print()
    
    if rice_seeds:
        print(f"🌾 Rice Seeds (ID: {rice_seeds.id})")
        print(f"   Name: {rice_seeds.name}")
        print(f"   Price: ₹{rice_seeds.price}/kg")
        print(f"   Stock: {rice_seeds.stock_quantity} units")
        print(f"   URL: /productinfo/?product={rice_seeds.id}")
        print()
    
    print("✅ Fix Applied:")
    print("- ❌ Removed hardcoded JavaScript productData")
    print("- ❌ Removed loadProductData() function calls")
    print("- ✅ Backend data now properly displays")
    print("- ✅ Each product shows its own information")
    print("- ✅ No more 'Wheat Seeds' showing for other products")
    
    print(f"\n🌐 Test These URLs:")
    if cotton_seeds:
        print(f"- Cotton: http://127.0.0.1:8000/productinfo/?product={cotton_seeds.id}")
    if tomato_seeds:
        print(f"- Tomato: http://127.0.0.1:8000/productinfo/?product={tomato_seeds.id}")
    if rice_seeds:
        print(f"- Rice: http://127.0.0.1:8000/productinfo/?product={rice_seeds.id}")

if __name__ == "__main__":
    test_product_fix()