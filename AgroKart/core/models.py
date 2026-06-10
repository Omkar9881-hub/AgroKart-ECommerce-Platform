from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
class Product(models.Model):
    name = models.CharField(max_length=200)
    name_mr = models.CharField(max_length=200, blank=True, null=True, verbose_name="Name in Marathi")
    description = models.TextField()
    description_mr = models.TextField(blank=True, null=True, verbose_name="Description in Marathi")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    category = models.CharField(max_length=100, blank=True)
    category_mr = models.CharField(max_length=100, blank=True, null=True, verbose_name="Category in Marathi")
    is_active = models.BooleanField(default=True)
    is_low_stock = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_at']
    
    def get_stock_status(self):
        """Get stock status description"""
        if self.stock_quantity == 0:
            return "Out of Stock"
        elif self.stock_quantity <= 5:
            return "Low Stock"
        elif self.stock_quantity <= 10:
            return "Limited Stock"
        else:
            return "In Stock"

class ProductFeedback(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_feedbacks')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=5)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for {self.product.name} by {self.user.username}"
    
    class Meta:
        ordering = ['-created_at']

class StockAlert(models.Model):
    ALERT_TYPES = [
        ('low_stock', 'Low Stock'),
        ('out_of_stock', 'Out of Stock'),
        ('critical_stock', 'Critical Stock'),
    ]
    
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_alerts')
    alert_type = models.CharField(max_length=20, choices=ALERT_TYPES, default='low_stock')
    message = models.TextField()
    stock_quantity = models.IntegerField()
    is_read = models.BooleanField(default=False)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"Stock Alert: {self.product.name} - {self.get_alert_type_display()}"
    
    class Meta:
        ordering = ['-created_at']
    
    def mark_as_read(self):
        """Mark alert as read"""
        self.is_read = True
        self.save()
    
    def mark_as_resolved(self):
        """Mark alert as resolved"""
        self.is_resolved = True
        self.resolved_at = timezone.now()
        self.save()
    
    @classmethod
    def create_low_stock_alert(cls, product):
        """Create a low stock alert for a product"""
        if product.stock_quantity <= 5 and product.stock_quantity > 0:
            # Check if alert already exists and is not resolved
            existing_alert = cls.objects.filter(
                product=product,
                alert_type='low_stock',
                is_resolved=False
            ).first()
            
            if not existing_alert:
                message = f"{product.name} has only {product.stock_quantity} units remaining. Please restock soon."
                return cls.objects.create(
                    product=product,
                    alert_type='low_stock',
                    message=message,
                    stock_quantity=product.stock_quantity
                )
        return None
    
    @classmethod
    def create_out_of_stock_alert(cls, product):
        """Create an out of stock alert for a product"""
        if product.stock_quantity == 0:
            # Check if alert already exists and is not resolved
            existing_alert = cls.objects.filter(
                product=product,
                alert_type='out_of_stock',
                is_resolved=False
            ).first()
            
            if not existing_alert:
                message = f"{product.name} is out of stock. Please restock immediately."
                return cls.objects.create(
                    product=product,
                    alert_type='out_of_stock',
                    message=message,
                    stock_quantity=0
                )
        return None

class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)  # Store product name directly
    product_price = models.DecimalField(max_digits=10, decimal_places=2)  # Store price at time of order
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default='pending')
    shipping_address = models.TextField()
    phone_number = models.CharField(max_length=15)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.user.username} - {self.product_name}"
    
    def can_be_edited(self):
        """Check if order can be edited (within 30 minutes of creation)"""
        time_limit = timedelta(minutes=30)
        return (timezone.now() - self.created_at) < time_limit and self.status == 'pending'
    
    def can_be_cancelled(self):
        """Check if order can be cancelled (confirmed orders can be cancelled, shipped orders cannot)"""
        # Allow cancellation for pending and confirmed orders only
        # Once shipped, order cannot be cancelled
        return self.status in ['pending', 'confirmed']
    
    def time_left_for_edit(self):
        """Get remaining time for editing in minutes"""
        time_limit = timedelta(minutes=30)
        elapsed = timezone.now() - self.created_at
        remaining = time_limit - elapsed
        if remaining.total_seconds() > 0:
            return int(remaining.total_seconds() / 60)
        return 0
    
    def time_left_for_cancel(self):
        """Get remaining time for cancellation in hours"""
        time_limit = timedelta(hours=2)
        elapsed = timezone.now() - self.created_at
        remaining = time_limit - elapsed
        if remaining.total_seconds() > 0:
            return round(remaining.total_seconds() / 3600, 1)
        return 0

class Feedback(models.Model):
    RATING_CHOICES = [
        (1, '1 Star'),
        (2, '2 Stars'),
        (3, '3 Stars'),
        (4, '4 Stars'),
        (5, '5 Stars'),
    ]
    
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='feedback')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback for Order #{self.order.id} - {self.rating} stars"
    
    class Meta:
        ordering = ['-created_at']

class ContactMessage(models.Model):
    username = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.email})"

class CustomerInquiry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    username = models.CharField(max_length=150)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.username} ({self.email})"
