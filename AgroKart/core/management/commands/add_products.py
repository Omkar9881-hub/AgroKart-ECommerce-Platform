from django.core.management.base import BaseCommand
from core.models import Product

class Command(BaseCommand):
    help = 'Add hardcoded products to database'

    def handle(self, *args, **options):
        # Clear existing products (optional)
        Product.objects.all().delete()
        self.stdout.write(self.style.WARNING('Cleared existing products'))

        # Products data from your hardcoded HTML
        products_data = [
            {
                'name': 'Organic Rice Seeds',
                'description': 'Certified organic rice seeds for sustainable farming with natural pest resistance. 100% organic certified, water efficient variety with premium grain quality.',
                'category': 'CEREALS',
                'price': 220.00,
                'stock_quantity': 50,
                'is_active': True
            },
            {
                'name': 'Hybrid Corn Seeds',
                'description': 'Advanced hybrid corn variety with superior yield potential and drought tolerance. Drought tolerant, high yield potential with uniform maturity.',
                'category': 'CEREALS',
                'price': 230.00,
                'stock_quantity': 45,
                'is_active': True
            },
            {
                'name': 'Premium Tomato Seeds',
                'description': 'High-quality tomato seeds with excellent fruit quality and extended shelf life. Blight resistant with high sugar content and continuous harvest.',
                'category': 'VEGETABLES',
                'price': 450.00,
                'stock_quantity': 30,
                'is_active': True
            },
            {
                'name': 'Red Onion Seeds',
                'description': 'Premium red onion variety with excellent storage quality and strong flavor profile. Long storage life, rich flavor with uniform bulb size.',
                'category': 'VEGETABLES',
                'price': 380.00,
                'stock_quantity': 40,
                'is_active': True
            },
            {
                'name': 'Potato Seeds',
                'description': 'High-yielding potato variety with excellent cooking quality and disease resistance. High starch content, good cooking quality and disease resistant.',
                'category': 'VEGETABLES',
                'price': 320.00,
                'stock_quantity': 60,
                'is_active': True
            },
            {
                'name': 'Green Cabbage Seeds',
                'description': 'Organic green cabbage variety with compact heads and excellent nutritional value. Compact head formation, high vitamin C and cold tolerant.',
                'category': 'VEGETABLES',
                'price': 290.00,
                'stock_quantity': 35,
                'is_active': True
            },
            {
                'name': 'Fresh Spinach Seeds',
                'description': 'Nutrient-rich spinach variety with tender leaves and rapid growth characteristics. High iron content, fast growing with tender leaves.',
                'category': 'LEAFY GREENS',
                'price': 420.00,
                'stock_quantity': 25,
                'is_active': True
            },
            {
                'name': 'Crisp Lettuce Seeds',
                'description': 'Premium lettuce variety with crisp texture and excellent shelf life for fresh consumption. Crisp texture, long shelf life and heat tolerant.',
                'category': 'LEAFY GREENS',
                'price': 480.00,
                'stock_quantity': 20,
                'is_active': True
            },
            {
                'name': 'Fresh Cucumber Seeds',
                'description': 'Hybrid cucumber variety with excellent fruit quality and high productivity for market cultivation. High productivity, uniform fruit size and disease resistant.',
                'category': 'VEGETABLES',
                'price': 340.00,
                'stock_quantity': 55,
                'is_active': True
            },
            {
                'name': 'Fresh Carrot Seeds',
                'description': 'Organic carrot variety with sweet flavor and high beta-carotene content for healthy nutrition. High in beta-carotene, crisp texture and organic certified.',
                'category': 'ROOT VEGETABLES',
                'price': 360.00,
                'stock_quantity': 42,
                'is_active': True
            }
        ]

        # Create products
        created_count = 0
        for product_data in products_data:
            product, created = Product.objects.get_or_create(
                name=product_data['name'],
                defaults=product_data
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Created: {product.name} - ₹{product.price}/kg')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'⚠ Already exists: {product.name}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Successfully added {created_count} products to database!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'📊 Total products in database: {Product.objects.count()}')
        )