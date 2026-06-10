from django.urls import path
from . import views
from .api_views import welcome, get_customer_inquiries
from .views import contact_us_view

urlpatterns = [

    path('login/',views.login_view, name="login" ),
    path('logout/', views.logout_view, name='logout'),
    path('home/',views.home_view, name="home" ),
    path('forgetpassword/',views.forgetpassword_view, name="forgetpassword" ),
    path('signup/', views.signup_view, name='signup'),
    path('aboutus/', views.aboutus_view, name='aboutus'),
    path('product/', views.product_view, name='product'),
    path('product/<int:product_id>/', views.productinfo_view, name='productinfo'),
    path('myorders/', views.myorders_view, name='myorders'),
    path('api/feedback/submit/', views.submit_feedback, name='submit_feedback'),
    path('api/product/feedback/submit/', views.submit_product_feedback, name='submit_product_feedback'),
    path('edit-order/<int:order_id>/', views.edit_order, name='edit_order'),
    path('cancel-order/<int:order_id>/', views.cancel_order, name='cancel_order'),
    path('create-sample-order/', views.create_sample_order, name='create_sample_order'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('add-sample-products/', views.add_sample_products, name='add_sample_products'),
    path('about/', views.about_view, name='about'),
    path('get-user-details/', views.get_user_details, name='get_user_details'),
    path('generate-bill/<int:order_id>/', views.generate_bill, name='generate_bill'),
    path('owner/', views.owner_dashboard, name='owner'),
    path('api/products/', views.api_products, name='api_products'),
    path('api/products/count/', views.api_products_count, name='api_products_count'),
    # Stock update endpoints
    path('api/products/<int:product_id>/', views.update_product_stock, name='api_product_detail'),
    path('api/products/update_stock/', views.update_product_stock, name='api_product_update_stock'),
    path('api/products/delete/', views.delete_product, name='api_product_delete'),
    path('api/orders/', views.api_orders, name='api_orders'),
    path('api/orders/count/', views.api_orders_count, name='api_orders_count'),
    path('api/products/toggle_active/', views.toggle_product_active, name='toggle_product_active'),
    path('api/orders/mark_completed/', views.mark_order_completed, name='mark_order_completed'),
    path('api/orders/cancel/', views.cancel_order_api, name='cancel_order_api'),
    path('api/orders/mark_shipped/<int:order_id>/', views.mark_order_shipped, name='mark_order_shipped'),
    path('api/orders/mark_out_for_delivery/', views.mark_order_out_for_delivery, name='mark_order_out_for_delivery'),
    path('api/orders/mark_delivered/', views.mark_order_delivered, name='mark_order_delivered'),
    path('place-cart-order/', views.place_cart_order, name='place_cart_order'),
    
    # Stock Alert API endpoints
    path('api/stock-alerts/', views.api_stock_alerts, name='api_stock_alerts'),
    path('api/stock-alerts/count/', views.api_stock_alerts_count, name='api_stock_alerts_count'),
    path('api/stock-alerts/mark-read/', views.mark_alert_read, name='mark_alert_read'),
    path('api/stock-alerts/mark-resolved/', views.mark_alert_resolved, name='mark_alert_resolved'),
    path('api/stock-alerts/clear-all/', views.clear_all_alerts, name='clear_all_alerts'),
    path('api/stock-alerts/check/', views.check_stock_alerts, name='check_stock_alerts'),
    
    # User Data API endpoints
    path('api/users/stats/', views.api_users_stats, name='api_users_stats'),
    path('api/users/list/', views.api_users_list, name='api_users_list'),
    path('api/users/<int:user_id>/', views.api_user_detail, name='api_user_detail'),
    
    # Business Analytics API endpoint
    path('api/business-analytics/', views.api_business_analytics, name='api_business_analytics'),
    
    # Order status checking endpoint
    path('api/check-order-status/', views.check_order_status_updates, name='check_order_status'),
    
    # Current user details endpoint
    path('api/current-user-details/', views.get_current_user_details, name='current_user_details'),

    # Ratings API endpoint for owner dashboard
    path('api/ratings/', views.api_ratings, name='api_ratings'),

    # Welcome API endpoint
    path('api/welcome/', welcome, name='api_welcome'),
    # Customer Inquiries API endpoint
    path('api/customer-inquiries/', get_customer_inquiries, name='api_customer_inquiries'),
    path('contact/', contact_us_view, name='contact_us'),
    path('management/inquiries/', views.customer_inquiry_list, name='customer_inquiry_list'),
]
