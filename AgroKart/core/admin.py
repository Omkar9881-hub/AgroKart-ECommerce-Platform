from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Product, Order

# Register your models here.

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['name', 'description', 'category']
    list_editable = ['price', 'stock_quantity', 'is_active']
    fields = ['name', 'description', 'category', 'price', 'stock_quantity', 'image', 'is_active']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['order_id', 'customer_name', 'product_ordered', 'quantity_ordered', 'total_amount', 'order_date', 'order_status', 'action_buttons']
    list_filter = ['status', 'created_at', 'user__username']
    search_fields = ['user__username', 'user__first_name', 'user__email', 'product_name']
    readonly_fields = ['order_id', 'customer_name', 'product_ordered', 'quantity_ordered', 'total_amount', 'order_date', 'user', 'product_name', 'product_price', 'quantity', 'total_price', 'shipping_address', 'phone_number', 'created_at', 'updated_at']
    fields = ['order_id', 'customer_name', 'product_ordered', 'quantity_ordered', 'total_amount', 'order_date', 'status', 'shipping_address', 'phone_number']
    list_per_page = 25
    ordering = ['-created_at']
    
    def get_urls(self):
        """Add custom URLs for order actions"""
        urls = super().get_urls()
        custom_urls = [
            path('confirm-order/<int:order_id>/', self.admin_site.admin_view(self.confirm_order_view), name='core_order_confirm'),
            path('ship-order/<int:order_id>/', self.admin_site.admin_view(self.ship_order_view), name='core_order_ship'),
            path('deliver-order/<int:order_id>/', self.admin_site.admin_view(self.deliver_order_view), name='core_order_deliver'),
        ]
        return custom_urls + urls
    
    def confirm_order_view(self, request, order_id):
        """Confirm order view"""
        try:
            order = Order.objects.get(id=order_id)
            if order.status == 'pending':
                order.status = 'confirmed'
                order.save()
                messages.success(request, f'Order #{order.id} confirmed successfully!')
            else:
                messages.warning(request, f'Order #{order.id} cannot be confirmed (current status: {order.get_status_display()})')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found!')
        
        return HttpResponseRedirect(reverse('admin:core_order_changelist'))
    
    def ship_order_view(self, request, order_id):
        """Ship order view (Done)"""
        try:
            order = Order.objects.get(id=order_id)
            if order.status == 'confirmed':
                order.status = 'shipped'
                order.save()
                messages.success(request, f'Order #{order.id} marked as shipped (Done)!')
            else:
                messages.warning(request, f'Order #{order.id} cannot be shipped (current status: {order.get_status_display()})')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found!')
        
        return HttpResponseRedirect(reverse('admin:core_order_changelist'))
    
    def deliver_order_view(self, request, order_id):
        """Deliver order view"""
        try:
            order = Order.objects.get(id=order_id)
            if order.status == 'shipped':
                order.status = 'delivered'
                order.save()
                messages.success(request, f'Order #{order.id} delivered successfully!')
            else:
                messages.warning(request, f'Order #{order.id} cannot be delivered (current status: {order.get_status_display()})')
        except Order.DoesNotExist:
            messages.error(request, 'Order not found!')
        
        return HttpResponseRedirect(reverse('admin:core_order_changelist'))
    
    def order_id(self, obj):
        return f"#{obj.id}"
    order_id.short_description = "Order ID"
    
    def customer_name(self, obj):
        return obj.user.username
    customer_name.short_description = "Customer Name"
    
    def customer_email(self, obj):
        return obj.user.email or "Not provided"
    customer_email.short_description = "Customer Email"
    
    def product_ordered(self, obj):
        return obj.product_name
    product_ordered.short_description = "Product"
    
    def quantity_ordered(self, obj):
        return f"{obj.quantity} units"
    quantity_ordered.short_description = "Quantity"
    
    def total_amount(self, obj):
        return f"₹{obj.total_price}"
    total_amount.short_description = "Total Amount"
    
    def order_date(self, obj):
        return obj.created_at.strftime("%d %b %Y, %I:%M %p")
    order_date.short_description = "Order Date"
    
    def order_status(self, obj):
        status_colors = {
            'pending': '🟡',
            'confirmed': '🟢', 
            'shipped': '🚚',
            'delivered': '✅',
            'cancelled': '❌'
        }
        return f"{status_colors.get(obj.status, '⚪')} {obj.get_status_display()}"
    order_status.short_description = "Status"
    
    def action_buttons(self, obj):
        """Display action buttons based on order status"""
        buttons = []
        
        if obj.status == 'pending':
            # Confirm Order button
            confirm_url = reverse('admin:core_order_confirm', args=[obj.pk])
            buttons.append(
                f'<a href="{confirm_url}" class="button" style="background-color: #28a745; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold;">✅ Confirm</a>'
            )
            
        elif obj.status == 'confirmed':
            # Mark as Shipped (Done) button
            ship_url = reverse('admin:core_order_ship', args=[obj.pk])
            buttons.append(
                f'<a href="{ship_url}" class="button" style="background-color: #007bff; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold;">🚚 Done</a>'
            )
            
        elif obj.status == 'shipped':
            # Mark as Delivered button
            deliver_url = reverse('admin:core_order_deliver', args=[obj.pk])
            buttons.append(
                f'<a href="{deliver_url}" class="button" style="background-color: #17a2b8; color: white; padding: 8px 15px; text-decoration: none; border-radius: 5px; font-weight: bold;">📦 Deliver</a>'
            )
        else:
            # For delivered or cancelled orders - no action needed
            buttons.append(
                f'<span style="color: #6c757d; font-style: italic;">No action required</span>'
            )
        
        return format_html(''.join(buttons))
    
    action_buttons.short_description = "Actions"
    action_buttons.allow_tags = True
    
    def has_add_permission(self, request):
        # Admin cannot create orders manually
        return False
    
    def has_delete_permission(self, request, obj=None):
        # Admin cannot delete orders
        return False
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing existing order
            return self.readonly_fields
        return []
    
    # Custom admin actions
    actions = ['mark_as_confirmed', 'mark_as_shipped', 'mark_as_delivered']
    
    def mark_as_confirmed(self, request, queryset):
        """Mark selected orders as confirmed"""
        updated = queryset.filter(status='pending').update(status='confirmed')
        self.message_user(request, f'{updated} orders marked as confirmed.')
    mark_as_confirmed.short_description = "Mark selected orders as Confirmed"
    
    def mark_as_shipped(self, request, queryset):
        """Mark selected orders as shipped (Done)"""
        updated = queryset.filter(status='confirmed').update(status='shipped')
        self.message_user(request, f'{updated} orders marked as shipped.')
    mark_as_shipped.short_description = "Mark selected orders as Shipped (Done)"
    
    def mark_as_delivered(self, request, queryset):
        """Mark selected orders as delivered"""
        updated = queryset.filter(status='shipped').update(status='delivered')
        self.message_user(request, f'{updated} orders marked as delivered.')
    mark_as_delivered.short_description = "Mark selected orders as Delivered"
