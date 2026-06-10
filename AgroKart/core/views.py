from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from .models import Order, Product, StockAlert, Feedback, ProductFeedback, ContactMessage, CustomerInquiry
import json
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from django.utils import timezone
from django.views.decorators.http import require_GET
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.db.models import Sum

# Other views...

@login_required
def generate_bill(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    user = request.user
    
    # Get user details with better fallback handling
    phone = user.last_name or ''
    address = user.first_name or ''
    
    # If user details are missing from the user model, try to get from order
    if not phone and order.phone_number and order.phone_number != "Not provided":
        phone = order.phone_number
    
    if not address and order.shipping_address and order.shipping_address != "Address not provided":
        address = order.shipping_address
    
    context = {
        'order': order,
        'user': user,
        'customer': {
            'username': user.username,
            'email': user.email,
            'phone': phone,
            'address': address,
        },
        'order_details': {
            'order_name': order.product_name,
            'order_id': order.id,
            'quantity': order.quantity,
            'rate': order.product_price,
            'total': order.total_price,
            'date': order.created_at,
        }
    }
    return render(request, 'core/order_receipt.html', context)

# Other views...
# ============================
# Signup View
# ============================
def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        location = request.POST.get('location')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Basic validation
        if not all([username, phone, email, location, password, confirm_password]):
            messages.error(request, "All fields are required!")
            return render(request, 'core/Signup.html')
        
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'core/Signup.html')
        
        if len(password) < 6 or not any(char.isalpha() for char in password):
            messages.error(request, "Password must be at least 6 characters and contain at least one letter!")
            return render(request, 'core/Signup.html')
        
        # Check if username or email already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return render(request, 'core/Signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'core/Signup.html')
        
        try:
            # Create new user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password
            )
            # Store phone in last_name and location in first_name
            user.first_name = location
            user.last_name = phone
            user.save()
            
            messages.success(request, "Account created successfully! Please login.")
            return redirect('login')
            
        except Exception as e:
            messages.error(request, f"Error creating account: {str(e)}")
            return render(request, 'core/Signup.html')
    
    return render(request, 'core/Signup.html')

# ============================
# Login View (Corrected)
# ============================
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Special case for Owner
        if username == 'Owner' and password == 'Owner@123':
            request.session['is_owner'] = True
            return redirect('owner')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}! Login successful.")
            return redirect('home')  # Successful login → Home
        else:
            messages.error(request, "Incorrect username or password!")
            return render(request, 'core/login.html')
    return render(request, 'core/login.html')


# ============================
# Home View
# ============================
def home_view(request):
    # Get featured products for home page
    products = Product.objects.filter(is_active=True).order_by('-created_at')[:6]  # Show 6 featured products
    categories = [
        'Cash Crops',
        'Oilseeds', 
        'Root Vegetables',
        'Vegetables',
        'Leafy Greens',
        'Cereals'
    ]
    return render(request, 'core/home.html', {'products': products, 'categories': categories})


# ============================
# forget password view
# ============================
def forgetpassword_view(request):
    return render(request, 'core/forgetpassword.html')


# ============================
# Aboutus view
# ============================
def aboutus_view(request):
    return render(request, 'core/AboutUs.html')


# ============================
# About view
# ============================
def about_view(request):
    return render(request, 'core/About.html')

# ============================
# product view
# ============================
def product_view(request):
    from django.core.paginator import Paginator
    from django.db.models import Q
    
    # Get search query and category filter from request
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    
    # Start with all active products
    products = Product.objects.filter(is_active=True)
    
    # Apply search filter if provided - search across ALL products
    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(category__icontains=search_query) |
            Q(name_mr__icontains=search_query) |
            Q(description_mr__icontains=search_query)
        )
    
    # Apply category filter if provided
    if category_filter:
        products = products.filter(category__iexact=category_filter)
    
    # Order by creation date
    products = products.order_by('-created_at')
    
    # Pagination - show 9 products per page
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Use the 6 specific categories you want to show
    categories = [
        'Cash Crops',
        'Oilseeds', 
        'Root Vegetables',
        'Vegetables',
        'Leafy Greens',
        'Cereals'
    ]
    
    return render(request, 'core/Product.html', {
        'products': page_obj,
        'categories': categories,
        'page_obj': page_obj,
        'search_query': search_query,
        'category_filter': category_filter
    })


# ============================
# productinfo view
# ============================
def productinfo_view(request, product_id=None):
    product = None
    
    if product_id:
        try:
            # Get product by ID from database
            product = Product.objects.get(id=product_id, is_active=True)
            print(f"DEBUG: Found product - ID: {product.id}, Name: {product.name}")
        except Product.DoesNotExist:
            print(f"DEBUG: Product with ID {product_id} not found")
            # Product not found, redirect to products page
            messages.error(request, "Product not found!")
            return redirect('product')
        except ValueError:
            print(f"DEBUG: Invalid product ID: {product_id}")
            # Invalid product ID format
            messages.error(request, "Invalid product ID!")
            return redirect('product')
    else:
        # For backward compatibility, check GET parameter
        product_id = request.GET.get('product')
        if product_id:
            try:
                product = Product.objects.get(id=product_id, is_active=True)
            except Product.DoesNotExist:
                messages.error(request, "Product not found!")
                return redirect('product')
            except ValueError:
                messages.error(request, "Invalid product ID!")
                return redirect('product')
        else:
            print("DEBUG: No product ID provided")
            # No product ID provided
            messages.error(request, "No product specified!")
            return redirect('product')
    
    return render(request, 'core/ProductInfo.html', {'product': product})



# ============================
# My Orders View
# ============================
@login_required
def myorders_view(request):
    print(f"DEBUG: myorders_view called for user: {request.user.username}")
    
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    print(f"DEBUG: Found {orders.count()} orders for user {request.user.username}")
    
    # Add additional context for each order
    for order in orders:
        print(f"DEBUG: Order #{order.id}: {order.product_name} - {order.status} - ₹{order.total_price}")
        
        # Add time-based information
        order.can_be_edited = order.can_be_edited()
        order.can_be_cancelled = order.can_be_cancelled()
        order.time_left_for_edit = order.time_left_for_edit()
        order.time_left_for_cancel = order.time_left_for_cancel()
        
        # Add expected delivery date for all orders (7 days from creation)
        order.expected_delivery_date = order.created_at + timedelta(days=7)
        
        # Add status-specific information
        if order.status == 'confirmed':
            order.status_message = 'Order confirmed and ready for processing'
            order.next_step = 'Admin will process and ship your order'
        elif order.status == 'shipped':
            order.status_message = 'Order has been shipped'
            order.next_step = 'Your order is on its way to you'
        elif order.status == 'delivered':
            order.status_message = 'Order has been delivered'
            order.next_step = 'Thank you for your purchase!'
        elif order.status == 'pending':
            order.status_message = 'Order is pending confirmation'
            order.next_step = 'Please wait for confirmation'
        elif order.status == 'cancelled':
            order.status_message = 'Order has been cancelled'
            order.next_step = 'Order was cancelled'
    
    print(f"DEBUG: Returning {orders.count()} orders to template")
    return render(request, 'core/myorders.html', {'orders': orders, 'csrf_token': request.META.get('CSRF_COOKIE', '')})

@login_required
def edit_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if not order.can_be_edited():
        return JsonResponse({
            'success': False, 
            'message': 'Order cannot be edited. Time limit exceeded or order status changed.'
        })
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            new_quantity = int(data.get('quantity', order.quantity))
            new_address = data.get('address', order.shipping_address)
            new_phone = data.get('phone', order.phone_number)
            
            if new_quantity > 0:
                order.quantity = new_quantity
                order.total_price = order.product_price * new_quantity
                order.shipping_address = new_address
                order.phone_number = new_phone
                order.save()
                
                return JsonResponse({
                    'success': True,
                    'message': 'Order updated successfully!',
                    'new_total': float(order.total_price)
                })
            else:
                return JsonResponse({'success': False, 'message': 'Quantity must be greater than 0'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def cancel_order(request, order_id):
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id, user=request.user)
    
        if not order.can_be_cancelled():
            return JsonResponse({
                'success': False, 
                'message': 'Order cannot be cancelled. Order has already been shipped or delivered.'
            })
    
        # Restore product stock when order is cancelled
        try:
            product = Product.objects.get(name=order.product_name, is_active=True)
            product.stock_quantity += order.quantity
            product.save()
            print(f"DEBUG: Restored {order.quantity} units to {product.name}. New stock: {product.stock_quantity}")
        except Product.DoesNotExist:
            print(f"DEBUG: Product {order.product_name} not found for stock restoration")
        
        order.status = 'cancelled'
        order.save()
        return JsonResponse({
            'success': True,
            'message': 'Order cancelled successfully!'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Sample function to create test orders (for demonstration)
@login_required
def create_sample_order(request):
    if request.method == 'POST':
        # Create a sample order for testing
        order = Order.objects.create(
            user=request.user,
            product_name="Premium Wheat Seeds",
            product_price=150.00,
            quantity=2,
            total_price=300.00,
            shipping_address="123 Farm Road, Village, District, State - 123456",
            phone_number="9876543210"
        )
        messages.success(request, f'Sample order #{order.id} created successfully!')
        return redirect('myorders')
    
    return render(request, 'core/create_sample_order.html')


# ============================
# Add to Cart View
# ============================
@login_required
@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            quantity = int(data.get('quantity', 1))
            
            print(f"DEBUG: User {request.user.username} adding product {product_id}, quantity {quantity}")
            
            # Get product
            try:
                product = Product.objects.get(id=product_id, is_active=True)
                print(f"DEBUG: Found product {product.name}")
            except Product.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'message': 'Product not found or not available'
                })
            
            # Check stock
            if product.stock_quantity < quantity:
                return JsonResponse({
                    'success': False,
                    'message': f'Only {product.stock_quantity} units available'
                })
            
            # Calculate total price
            total_price = product.price * quantity
            
            # Create new order
            print(f"DEBUG: Creating order for {request.user.username}")
            
            order = Order.objects.create(
                user=request.user,
                product_name=product.name,
                product_price=product.price,
                quantity=quantity,
                total_price=total_price,
                shipping_address=request.user.first_name or "Address not provided",
                phone_number=request.user.last_name or "Not provided",
                status='confirmed'
            )
            
            print(f"DEBUG: Order created with ID: {order.id}")
            
            # Update product stock
            product.stock_quantity -= quantity
            product.save()
            
            # Verify order was saved
            saved_order = Order.objects.get(id=order.id)
            print(f"DEBUG: Order verified - ID: {saved_order.id}, Status: {saved_order.status}")
            
            return JsonResponse({
                'success': True,
                'message': 'Order placed successfully and confirmed!',
                'order_id': order.id,
                'redirect_url': '/myorders/'
            })
            
        except Exception as e:
            print(f"DEBUG: Error: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': f'Error: {str(e)}'
            })
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


# ============================
# Logout View
# ============================
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully!")
    return redirect('home')

# ============================
# Temporary function to add products
# ============================
def add_sample_products(request):
    """Temporary view to add sample products to database"""
    try:
        # Product 1: Sunflower Seeds
        product1, created1 = Product.objects.get_or_create(
            name="Premium Sunflower Seeds",
            defaults={
                'description': "High-quality sunflower seeds with excellent oil content and disease resistance. Perfect for commercial farming with guaranteed high yield potential.",
                'price': 180.00,
                'stock_quantity': 150,
                'category': "OILSEEDS",
                'is_active': True
            }
        )
        
        # Product 2: Cotton Seeds
        product2, created2 = Product.objects.get_or_create(
            name="Hybrid Cotton Seeds",
            defaults={
                'description': "Advanced hybrid cotton variety with superior fiber quality and bollworm resistance. Ideal for textile industry requirements.",
                'price': 320.00,
                'stock_quantity': 80,
                'category': "CASH CROPS",
                'is_active': True
            }
        )
        
        result_msg = []
        if created1:
            result_msg.append(f"✅ Added: {product1.name} - ₹{product1.price}/kg")
        else:
            result_msg.append(f"⚠️ Already exists: {product1.name}")
            
        if created2:
            result_msg.append(f"✅ Added: {product2.name} - ₹{product2.price}/kg")
        else:
            result_msg.append(f"⚠️ Already exists: {product2.name}")
        
        # Get all products count
        total_products = Product.objects.count()
        result_msg.append(f"📦 Total products in database: {total_products}")
        
        return JsonResponse({
            'success': True,
            'message': '<br>'.join(result_msg)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f"❌ Error adding products: {str(e)}"
        })

# ============================
# Admin Order Management Views
# ============================

@staff_member_required
def admin_confirm_order(request, order_id):
    """Admin function to confirm pending orders"""
    order = get_object_or_404(Order, id=order_id)
    
    if order.status == 'pending':
        order.status = 'confirmed'
        order.save()
        messages.success(request, f'Order #{order.id} has been confirmed successfully!')
    else:
        messages.warning(request, f'Order #{order.id} cannot be confirmed. Current status: {order.get_status_display()}')
    
    return HttpResponseRedirect(reverse('admin:core_order_changelist'))

@staff_member_required
def admin_ship_order(request, order_id):
    """Admin function to mark confirmed orders as shipped (Done)"""
    order = get_object_or_404(Order, id=order_id)
    
    if order.status == 'confirmed':
        order.status = 'shipped'
        order.save()
        messages.success(request, f'Order #{order.id} has been marked as shipped (Done)!')
    else:
        messages.warning(request, f'Order #{order.id} cannot be shipped. Current status: {order.get_status_display()}')
    
    return HttpResponseRedirect(reverse('admin:core_order_changelist'))

@staff_member_required
def admin_deliver_order(request, order_id):
    """Admin function to mark shipped orders as delivered"""
    order = get_object_or_404(Order, id=order_id)
    
    if order.status == 'shipped':
        order.status = 'delivered'
        order.save()
        messages.success(request, f'Order #{order.id} has been marked as delivered!')
    else:
        messages.warning(request, f'Order #{order.id} cannot be delivered. Current status: {order.get_status_display()}')
    
    return HttpResponseRedirect(reverse('admin:core_order_changelist'))

# ============================
# Get User Details API
# ============================
@login_required
@require_GET
def get_user_details(request):
    user = request.user
    return JsonResponse({
        'success': True,
        'user': {
            'username': user.username,
            'email': user.email,
            'phone': user.last_name or '',  # Phone stored in last_name field
            'address': user.first_name or '',  # Address stored in first_name field
        }
    })

@login_required
def update_user_details(request):
    if request.method == 'POST':
        user = request.user
        data = json.loads(request.body)
        user.first_name = data.get('address', user.first_name)
        user.last_name = data.get('phone', user.last_name)
        user.save()
        return JsonResponse({'success': True, 'message': 'User details updated successfully!'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


@login_required
@require_GET
def check_order_status_updates(request):
    """API endpoint to check for order status updates"""
    try:
        # Check if this is an AJAX request
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        
        if not is_ajax:
            return JsonResponse({
                'success': False,
                'error': 'This endpoint is for AJAX requests only'
            }, status=400)
        
        # Get all orders for the current user
        orders = Order.objects.filter(user=request.user).order_by('-created_at')
        
        # Prepare order data for response
        orders_data = []
        for order in orders:
            orders_data.append({
                'id': order.id,
                'status': order.status,
                'product_name': order.product_name,
                'quantity': order.quantity,
                'total_price': float(order.total_price),
                'created_at': order.created_at.isoformat(),
                'can_be_edited': order.can_be_edited(),
                'can_be_cancelled': order.can_be_cancelled(),
                'time_left_for_edit': order.time_left_for_edit(),
                'time_left_for_cancel': order.time_left_for_cancel()
            })
        
        return JsonResponse({
            'success': True,
            'orders': orders_data,
            'timestamp': timezone.now().isoformat()
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)

def owner_dashboard(request):
    if not request.session.get('is_owner'):
        return redirect('home')
    # Remove flag after access for security
    request.session['is_owner'] = False
    return render(request, 'core/owner.html')

@login_required
@csrf_exempt
def submit_feedback(request):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    order_id = data.get('order_id')
    rating = data.get('rating')
    comment = data.get('comment', '').strip()

    if not order_id or not rating:
        return JsonResponse({'success': False, 'message': 'Missing order_id or rating'}, status=400)

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Rating must be 1-5'}, status=400)

    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.status != 'delivered':
        return JsonResponse({'success': False, 'message': 'Feedback allowed only after delivery'}, status=403)

    # Prevent duplicate feedback
    if hasattr(order, 'feedback'):
        fb = order.feedback
        fb.rating = rating
        fb.comment = comment
        fb.save()
        return JsonResponse({'success': True, 'updated': True})

    Feedback.objects.create(order=order, user=request.user, rating=rating, comment=comment)
    return JsonResponse({'success': True})

@login_required
@csrf_exempt
def submit_product_feedback(request):
    """Submit feedback for a specific product"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Invalid method'}, status=405)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except Exception:
        return JsonResponse({'success': False, 'message': 'Invalid JSON'}, status=400)

    product_id = data.get('product_id')
    rating = data.get('rating')
    comment = data.get('comment', '').strip()

    if not product_id or not rating:
        return JsonResponse({'success': False, 'message': 'Missing product_id or rating'}, status=400)

    try:
        rating = int(rating)
        if rating < 1 or rating > 5:
            raise ValueError
    except ValueError:
        return JsonResponse({'success': False, 'message': 'Rating must be 1-5'}, status=400)

    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    # Create or update product feedback
    feedback, created = ProductFeedback.objects.get_or_create(
        product=product,
        user=request.user,
        defaults={'rating': rating, 'comment': comment}
    )
    
    if not created:
        feedback.rating = rating
        feedback.comment = comment
        feedback.save()
    
    return JsonResponse({
        'success': True,
        'created': created,
        'message': 'Product feedback submitted successfully!'
    })

@csrf_exempt
def api_products(request):
    if request.method == 'POST':
        # Handle product creation
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock_quantity = request.POST.get('stock_quantity')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        if not (name and description and price and stock_quantity and category):
            return JsonResponse({'success': False, 'error': 'Missing required fields.'}, status=400)
        try:
            product = Product.objects.create(
                name=name,
                description=description,
                price=price,
                stock_quantity=stock_quantity,
                category=category,
                image=image,
                is_low_stock=(int(stock_quantity) <= 5 and int(stock_quantity) > 0)
            )
            return JsonResponse({'success': True, 'id': product.id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    # GET: list products
    products = Product.objects.all()
    products_data = []
    for product in products:
        products_data.append({
            'id': product.id,
            'name': product.name,
            'category': product.category,
            'price': float(product.price),
            'stock_quantity': product.stock_quantity,
            'is_active': product.is_active,
            'created_at': product.created_at.strftime('%Y-%m-%d %H:%M') if product.created_at else None
        })
    return JsonResponse(products_data, safe=False)

def api_products_count(request):
    """Return total count of products"""
    count = Product.objects.count()
    return JsonResponse({'count': count})

def api_orders_count(request):
    """Return total count of orders"""
    count = Order.objects.count()
    return JsonResponse({'count': count})

@csrf_exempt
def toggle_product_active(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        make_active = request.POST.get('make_active') == 'true'
        try:
            product = Product.objects.get(id=product_id)
            product.is_active = make_active
            product.save()
            return JsonResponse({'success': True, 'is_active': product.is_active})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

def api_orders(request):
    page = int(request.GET.get('page', 1))
    page_size = int(request.GET.get('page_size', 29))
    orders = Order.objects.select_related('user').all().order_by('-created_at')
    paginator = Paginator(orders, page_size)
    page_obj = paginator.get_page(page)
    data = []
    for order in page_obj.object_list:
        data.append({
            'id': order.id,
            'customer_name': order.user.username,
            'product': order.product_name,
            'quantity': order.quantity,
            'total_amount': float(order.total_price),
            'order_date': order.created_at.strftime('%Y-%m-%d %H:%M'),
            'status': order.status,
        })
    return JsonResponse({
        'results': data,
        'page': page_obj.number,
        'num_pages': paginator.num_pages,
        'has_next': page_obj.has_next(),
        'has_prev': page_obj.has_previous(),
    })

@csrf_exempt
def update_product_stock(request, product_id=None):
    """Update a product's stock quantity and/or price.

    Supports:
    - PATCH /api/products/<id>/ with JSON body {"stock_quantity": N, "price": P}
    - POST  /api/products/update_stock/ with form data (product_id, stock_quantity, price)
    """
    try:
        pid = None
        new_stock = None
        new_price = None

        if request.method in ['PATCH', 'PUT']:
            # JSON body
            try:
                data = json.loads(request.body or '{}')
            except Exception:
                data = {}
            pid = product_id or data.get('id') or data.get('product_id')
            new_stock = data.get('stock_quantity')
            new_price = data.get('price')
        elif request.method == 'POST':
            pid = request.POST.get('product_id')
            new_stock = request.POST.get('stock_quantity')
            new_price = request.POST.get('price')
        else:
            return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

        if pid in [None, '']:
            return JsonResponse({'success': False, 'error': 'Missing product_id.'}, status=400)

        # At least one of stock_quantity or price must be provided
        if new_stock in [None, ''] and new_price in [None, '']:
            return JsonResponse({'success': False, 'error': 'Missing stock_quantity or price.'}, status=400)

        product = Product.objects.get(id=int(pid))

        # Update stock if provided
        if new_stock not in [None, '']:
            product.stock_quantity = int(new_stock)
            # Maintain low stock flag if used elsewhere
            try:
                product.is_low_stock = (product.stock_quantity <= 5 and product.stock_quantity > 0)
            except Exception:
                pass

        # Update price if provided
        if new_price not in [None, '']:
            product.price = float(new_price)

        product.save()

        # Generate stock alerts if needed
        try:
            StockAlert.create_low_stock_alert(product)
            StockAlert.create_out_of_stock_alert(product)
        except Exception:
            pass

        return JsonResponse({
            'success': True,
            'id': product.id,
            'stock_quantity': product.stock_quantity,
            'price': float(product.price)
        })
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def delete_product(request):
    """Delete a product by id using POST form-data: product_id"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)
    try:
        product_id = request.POST.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'Missing product_id.'}, status=400)
        product = Product.objects.get(id=int(product_id))
        product.delete()
        return JsonResponse({'success': True})
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Product not found.'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def mark_order_completed(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'completed'
            order.save()
            return JsonResponse({'success': True, 'status': order.status})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def cancel_order_api(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            order.status = 'cancelled'
            order.save()
            return JsonResponse({'success': True, 'status': order.status})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def mark_order_shipped(request, order_id):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            order = Order.objects.get(id=order_id)
            if order.status == "confirmed":
                order.status = "shipped"
                order.save()
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "message": "Order not in confirmed state."})
        except Order.DoesNotExist:
            return JsonResponse({"success": False, "message": "Order not found."})
    return JsonResponse({"success": False, "message": "Invalid request."})

@csrf_exempt
def mark_order_out_for_delivery(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            if order.status == 'shipped':
                order.status = 'out_for_delivery'
                order.save()
                return JsonResponse({'success': True, 'status': order.status})
            else:
                return JsonResponse({'success': False, 'error': 'Order not in shipped state.'}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@csrf_exempt
def mark_order_delivered(request):
    if request.method == 'POST':
        order_id = request.POST.get('order_id')
        try:
            order = Order.objects.get(id=order_id)
            if order.status in ['shipped', 'out_for_delivery']:
                order.status = 'delivered'
                order.save()
                return JsonResponse({'success': True, 'status': order.status})
            else:
                return JsonResponse({'success': False, 'error': f'Order not in a deliverable state. Current status: {order.status}'}, status=400)
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Order not found.'}, status=404)
    return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=400)

@login_required
@csrf_exempt
def place_cart_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            products = data.get('products', [])
            if not products:
                return JsonResponse({'success': False, 'message': 'No products in cart.'})

            # Only use valid product names, and error if any are missing
            product_names = ', '.join([str(p['name']) for p in products if p.get('name')])
            if not product_names or len(products) != len([p for p in products if p.get('name')]):
                return JsonResponse({'success': False, 'message': 'Invalid product data (missing product name). Please refresh and try again.'})

            total_price = sum([float(p['price']) * int(p['quantity']) for p in products])
            total_quantity = sum([int(p['quantity']) for p in products])

            order = Order.objects.create(
                user=request.user,
                product_name=product_names,
                product_price=0,  # Optional: store as 0 or first product price
                quantity=total_quantity,
                total_price=total_price,
                shipping_address=request.user.first_name or "Address not provided",
                phone_number=request.user.last_name or "Not provided",
                status='confirmed'
            )

            # Update stock for each product
            for p in products:
                prod = Product.objects.get(id=p['id'])
                prod.stock_quantity -= int(p['quantity'])
                prod.save()
                
                # Check for stock alerts after updating stock
                StockAlert.create_low_stock_alert(prod)
                StockAlert.create_out_of_stock_alert(prod)

            return JsonResponse({'success': True, 'order_id': order.id, 'redirect_url': '/myorders/'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# ============================
# Stock Alert API Endpoints
# ============================

@require_GET
def api_stock_alerts(request):
    """Get all stock alerts"""
    try:
        alerts = StockAlert.objects.filter(is_resolved=False).order_by('-created_at')
        
        # Convert to JSON-serializable format
        alerts_data = []
        for alert in alerts:
            alerts_data.append({
                'id': alert.id,
                'product_id': alert.product.id,
                'product_name': alert.product.name,
                'alert_type': alert.alert_type,
                'message': alert.message,
                'stock_quantity': alert.stock_quantity,
                'is_read': alert.is_read,
                'created_at': alert.created_at.isoformat(),
                'time_ago': get_time_ago(alert.created_at)
            })
        
        return JsonResponse({
            'success': True,
            'alerts': alerts_data,
            'count': len(alerts_data)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_GET
def api_stock_alerts_count(request):
    """Get count of unread stock alerts"""
    try:
        unread_count = StockAlert.objects.filter(is_read=False, is_resolved=False).count()
        return JsonResponse({
            'success': True,
            'count': unread_count
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@csrf_exempt
def mark_alert_read(request):
    """Mark a specific alert as read"""
    if request.method == 'POST':
        try:
            alert_id = request.POST.get('alert_id')
            alert = get_object_or_404(StockAlert, id=alert_id)
            alert.mark_as_read()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@csrf_exempt
def mark_alert_resolved(request):
    """Mark a specific alert as resolved"""
    if request.method == 'POST':
        try:
            alert_id = request.POST.get('alert_id')
            alert = get_object_or_404(StockAlert, id=alert_id)
            alert.mark_as_resolved()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@csrf_exempt
def clear_all_alerts(request):
    """Mark all alerts as read"""
    if request.method == 'POST':
        try:
            StockAlert.objects.filter(is_read=False).update(is_read=True)
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

@csrf_exempt
def check_stock_alerts(request):
    """Check all products for stock alerts and create new ones"""
    if request.method == 'POST':
        try:
            products = Product.objects.filter(is_active=True)
            new_alerts = []
            
            for product in products:
                # Check for low stock alerts
                low_stock_alert = StockAlert.create_low_stock_alert(product)
                if low_stock_alert:
                    new_alerts.append({
                        'id': low_stock_alert.id,
                        'product_name': product.name,
                        'stock_quantity': product.stock_quantity,
                        'message': low_stock_alert.message
                    })
                
                # Check for out of stock alerts
                out_of_stock_alert = StockAlert.create_out_of_stock_alert(product)
                if out_of_stock_alert:
                    new_alerts.append({
                        'id': out_of_stock_alert.id,
                        'product_name': product.name,
                        'stock_quantity': 0,
                        'message': out_of_stock_alert.message
                    })
            
            return JsonResponse({
                'success': True,
                'new_alerts': new_alerts,
                'count': len(new_alerts)
            })
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)

# ============================
# User Data API Endpoints
# ============================

@require_GET
def api_users_stats(request):
    """Get user statistics for reports dashboard"""
    try:
        # Total registered users
        total_users = User.objects.count()
        
        # Active users (users who have placed at least one order)
        active_users = User.objects.filter(order__isnull=False).distinct().count()
        
        # New users this month
        current_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        new_users = User.objects.filter(date_joined__gte=current_month).count()
        
        return JsonResponse({
            'success': True,
            'total_users': total_users,
            'active_users': active_users,
            'new_users': new_users
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)


@require_GET
def api_business_analytics(request):
    """Get business analytics data for dashboard"""
    try:
        # Calculate total revenue from all orders
        total_revenue = Order.objects.aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        # Total orders
        total_orders = Order.objects.count()
        
        # Active products
        active_products = Product.objects.filter(is_active=True).count()
        
        # Total customers (users who have placed orders)
        total_customers = User.objects.filter(order__isnull=False).distinct().count()
        
        # Calculate revenue for different periods
        today = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        year_ago = today - timedelta(days=365)
        
        today_revenue = Order.objects.filter(created_at__gte=today).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        week_revenue = Order.objects.filter(created_at__gte=week_ago).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        month_revenue = Order.objects.filter(created_at__gte=month_ago).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        year_revenue = Order.objects.filter(created_at__gte=year_ago).aggregate(
            total=Sum('total_price')
        )['total'] or 0
        
        # Calculate orders for different periods
        today_orders = Order.objects.filter(created_at__gte=today).count()
        week_orders = Order.objects.filter(created_at__gte=week_ago).count()
        month_orders = Order.objects.filter(created_at__gte=month_ago).count()
        year_orders = Order.objects.filter(created_at__gte=year_ago).count()
        
        # Calculate new products for the month
        new_products = Product.objects.filter(created_at__gte=month_ago).count()
        
        # Calculate new customers for the month
        new_customers = User.objects.filter(
            order__isnull=False,
            order__created_at__gte=month_ago
        ).distinct().count()
        
        # Calculate new customers for the week
        new_customers_week = User.objects.filter(
            order__isnull=False,
            order__created_at__gte=week_ago
        ).distinct().count()
        
        return JsonResponse({
            'success': True,
            'analytics': {
                'total_revenue': float(total_revenue),
                'total_orders': total_orders,
                'active_products': active_products,
                'total_customers': total_customers,
                'today_revenue': float(today_revenue),
                'week_revenue': float(week_revenue),
                'month_revenue': float(month_revenue),
                'year_revenue': float(year_revenue),
                'today_orders': today_orders,
                'week_orders': week_orders,
                'month_orders': month_orders,
                'year_orders': year_orders,
                'new_products': new_products,
                'new_customers': new_customers,
                'new_customers_week': new_customers_week
            }
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_GET
def api_users_list(request):
    """Get list of all users with their details"""
    try:
        users = User.objects.all().order_by('-date_joined')
        users_data = []
        
        for user in users:
            # Count orders for each user
            order_count = Order.objects.filter(user=user).count()
            
            users_data.append({
                'id': user.id,
                'first_name': user.username,  # Show username as name
                'last_name': '',  # Empty last name
                'username': user.username,
                'email': user.email,
                'phone': user.last_name or 'Not provided',  # Phone stored in last_name field
                'date_joined': user.date_joined.isoformat(),
                'is_active': user.is_active,
                'order_count': order_count,
                'last_login': user.last_login.isoformat() if user.last_login else None
            })
        
        return JsonResponse({
            'success': True,
            'users': users_data,
            'count': len(users_data)
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

@require_GET
def api_user_detail(request, user_id):
    """Get detailed user information including complete order history"""
    try:
        user = get_object_or_404(User, id=user_id)
        orders = Order.objects.filter(user=user).order_by('-created_at')
        
        # User basic info
        user_info = {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'phone': user.last_name or 'Not provided',
            'address': user.first_name or 'Not provided',
            'date_joined': user.date_joined.isoformat(),
            'is_active': user.is_active,
            'last_login': user.last_login.isoformat() if user.last_login else None,
            'total_orders': orders.count()
        }
        
        # Order history with detailed information
        orders_data = []
        for order in orders:
            # Get feedback for this order if it exists
            feedback = None
            try:
                feedback_obj = Feedback.objects.get(order=order)
                feedback = {
                    'rating': feedback_obj.rating,
                    'comment': feedback_obj.comment,
                    'created_at': feedback_obj.created_at.isoformat()
                }
            except Feedback.DoesNotExist:
                pass
            
            orders_data.append({
                'id': order.id,
                'product_name': order.product_name,
                'quantity': order.quantity,
                'product_price': float(order.product_price),
                'total_price': float(order.total_price),
                'status': order.status,
                'order_date': order.created_at.isoformat(),
                'order_date_formatted': order.created_at.strftime('%d %b %Y, %I:%M %p'),
                'shipping_address': order.shipping_address,
                'phone_number': order.phone_number,
                'time_ago': get_time_ago(order.created_at),
                'rating': feedback['rating'] if feedback else None,
                'comment': feedback['comment'] if feedback else None,
                'feedback_created_at': feedback['created_at'] if feedback else None
            })
        
        return JsonResponse({
            'success': True,
            'user': user_info,
            'orders': orders_data
        })
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)

def get_time_ago(datetime_obj):
    """Helper function to get relative time"""
    now = timezone.now()
    diff = now - datetime_obj
    
    if diff.days > 0:
        return f"{diff.days} day{'s' if diff.days != 1 else ''} ago"
    elif diff.seconds >= 3600:
        hours = diff.seconds // 3600
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    elif diff.seconds >= 60:
        minutes = diff.seconds // 60
        return f"{minutes} minute{'s' if minutes != 1 else ''} ago"
    else:
        return "Just now"
    
@login_required
def get_current_user_details(request):
    """API endpoint for fetching current user details."""
    user = request.user
    user_details = {
        'username': user.username,
        'email': user.email,
        'phone': user.last_name or '',  # Phone stored in last_name field
        'address': user.first_name or '',  # Address stored in first_name field
    }
    return JsonResponse({'success': True, 'user': user_details})

@require_GET
def api_ratings(request):
    """API endpoint for fetching all ratings and feedback for owner dashboard"""
    try:
        # Get all feedback from both Feedback and ProductFeedback models
        order_feedbacks = Feedback.objects.select_related('order', 'user').all()
        product_feedbacks = ProductFeedback.objects.select_related('product', 'user').all()

        ratings_data = []

        # Process order feedback
        for feedback in order_feedbacks:
            ratings_data.append({
                'id': f"order_{feedback.id}",
                'type': 'order',
                'product_name': feedback.order.product_name,
                'customer_name': feedback.user.username,
                'customer': feedback.user.username,
                'rating': feedback.rating,
                'comment': feedback.comment,
                'feedback': feedback.comment,
                'created_at': feedback.created_at.isoformat(),
                'order_id': feedback.order.id,
                'status': feedback.order.status
            })

        # Process product feedback
        for feedback in product_feedbacks:
            ratings_data.append({
                'id': f"product_{feedback.id}",
                'type': 'product',
                'product_name': feedback.product.name,
                'customer_name': feedback.user.username,
                'customer': feedback.user.username,
                'rating': feedback.rating,
                'comment': feedback.comment,
                'feedback': feedback.comment,
                'created_at': feedback.created_at.isoformat(),
                'product_id': feedback.product.id
            })

        # Sort by creation date (newest first)
        ratings_data.sort(key=lambda x: x['created_at'], reverse=True)

        return JsonResponse({
            'success': True,
            'ratings': ratings_data,
            'total_count': len(ratings_data),
            'order_feedbacks_count': order_feedbacks.count(),
            'product_feedbacks_count': product_feedbacks.count()
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'ratings': []
        }, status=500)

def contact_us_view(request):
    user = request.user
    context = {
        'username': user.username if user.is_authenticated else '',
        'phone': user.last_name if user.is_authenticated else '',
        'email': user.email if user.is_authenticated else '',
    }
    if request.method == 'POST':
        CustomerInquiry.objects.create(
            username=request.POST.get('username', ''),
            phone=request.POST.get('phone', ''),
            email=request.POST.get('email', ''),
            message=request.POST.get('message', '')
        )
        context['message_sent'] = True
    return render(request, 'core/contact_us.html', context)

def is_management(user):
    return user.is_staff or user.is_superuser

@user_passes_test(is_management)
def customer_inquiry_list(request):
    inquiries = CustomerInquiry.objects.order_by('-created_at')
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        inquiry_list = []
        for inquiry in inquiries:
            inquiry_list.append({
                'id': inquiry.id,
                'username': inquiry.username,
                'phone': inquiry.phone,
                'email': inquiry.email,
                'message': inquiry.message,
                'submitted_at': inquiry.created_at.strftime('%Y-%m-%d %H:%M:%S')
            })
        return JsonResponse({'inquiries': inquiry_list})
    else:
        return render(request, 'core/customer_inquiry_list.html', {'inquiries': inquiries})
