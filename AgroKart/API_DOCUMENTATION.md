# Agrokart Django Application - API Documentation

## Overview
This document provides comprehensive documentation for all URL patterns and API endpoints in the Agrokart Django application.

## URL Patterns Structure

### Main URL Configuration (`Agrokart/urls.py`)
- **Admin Interface**: `admin/`
- **Core Application**: Includes all routes from `core.urls`

### Core Application URLs (`core/urls.py`)

## Authentication & User Management

| Endpoint | Method | Description | Authentication | Parameters |
|----------|--------|-------------|----------------|------------|
| `login/` | GET/POST | User login page and authentication | None | - |
| `logout/` | GET | User logout | None | - |
| `forgetpassword/` | GET | Password reset page | None | - |
| `get-user-details/` | GET | Get current user details | Login Required | - |

## Product Management

| Endpoint | Method | Description | Authentication | Parameters |
|----------|--------|-------------|----------------|------------|
| `product/` | GET | Product listing page with search/filter | None | `search`, `category`, `page` |
| `product/<int:product_id>/` | GET | Product detail page | None | `product_id` |
| `add-sample-products/` | GET | Add sample products (demo) | None | - |

## Order Management

| Endpoint | Method | Description | Authentication | Parameters |
|----------|--------|-------------|----------------|------------|
| `myorders/` | GET | User's order history | Login Required | - |
| `edit-order/<int:order_id>/` | POST | Edit order details | Login Required | `order_id`, `quantity`, `address`, `phone` |
| `cancel-order/<int:order_id>/` | POST | Cancel an order | Login Required | `order_id` |
| `create-sample-order/` | POST | Create sample order (demo) | Login Required | - |
| `add-to-cart/` | POST | Add product to cart/place order | Login Required | `product_id`, `quantity` |
| `place-cart-order/` | POST | Place order from cart | Login Required | `products[]` |
| `generate-bill/<int:order_id>/` | GET | Generate order bill/receipt | Login Required | `order_id` |

## API Endpoints

### Products API

| Endpoint | Method | Description | Authentication | Parameters |
|----------|--------|-------------|----------------|------------|
| `api/products/` | GET | List all products | None | - |
| `api/products/` | POST | Create new product | Staff Required | `name`, `description`, `price`, `stock_quantity`, `category`, `image` |
| `api/products/count/` | GET | Get product count | None | - |
| `api/products/<int:product_id>/` | PATCH/PUT | Update product stock | None | `stock_quantity` |
| `api/products/update_stock/` | POST | Update product stock | None | `product_id`, `stock_quantity` |
| `api/products/delete/` | POST | Delete product | Staff Required | `product_id` |
| `api/products/toggle_active/` | POST | Toggle product active status | Staff Required | `product_id`, `make_active` |

### Orders API

| Endpoint | Method | Description | Authentication | Parameters |
|----------|--------|-------------|----------------|------------|
| `api/orders/` | GET | List all orders (paginated) | Staff Required | `page`, `page_size` |
| `api/orders/count/` | GET | Get order count | None | - |
| `api/orders/mark_completed/` | POST | Mark order as completed | Staff Required | `order_id` |
| `api/orders/cancel/` | POST | Cancel order via API | Staff Required | `order_id` |
| `api/orders/mark_shipped/` | POST | Mark order as shipped | Staff Required | `order_id` |
| `api/orders/mark_out_for_delivery/` | POST | Mark order as out for delivery | Staff Required | `order_id` |
| `api/orders/mark_delivered/` | POST | Mark order as delivered | Staff Required | `order_id` |
| `mark-shipped/<int:order_id>/` | POST | Mark order as shipped (user) | Login Required | `order_id` |

### Stock Alerts API

| Endpoint | Method | Description | Authentication | Parameters |
|----------|--------|-------------|----------------|------------|
| `api/stock-alerts/` | GET | Get all stock alerts | Staff Required | - |
| `api/stock-alerts/count/` | GET | Get unread alert count | Staff Required | - |
| `api/stock-alerts/mark-read/` | POST | Mark alert as read | Staff Required | `alert_id` |
| `api/stock-alerts/mark-resolved/` | POST | Mark alert as resolved | Staff Required | `alert_id` |
| `api/stock-alerts/clear-all/` | POST | Mark all alerts as read | Staff Required | - |
| `api/stock-alerts/check/` | POST | Check for new stock alerts | Staff Required | - |

### User Management API

| Endpoint | Method | Description | Authentication | Parameters |
|----------|--------|-------------|----------------|------------|
| `api/users/stats/` | GET | Get user statistics | Staff Required | - |
| `api/users/list/` | GET | List all users | Staff Required | - |
| `api/users/<int:user_id>/` | GET | Get user details with orders | Staff Required | `user_id` |

### Feedback API

| Endpoint | Method | Description | Authentication | Parameters |
|----------|--------|-------------|----------------|------------|
| `api/feedback/submit/` | POST | Submit order feedback | Login Required | `order_id`, `rating`, `comment` |
| `api/product/feedback/submit/` | POST | Submit product feedback | Login Required | `product_id`, `rating`, `comment` |

### Utility Endpoints

| Endpoint | Method | Description | Authentication | Parameters |
|----------|--------|-------------|----------------|------------|
| `api/check-order-status/` | GET | Check order status updates | Login Required | - |
| `home/` | GET | Home page with featured products | None | - |
| `aboutus/` | GET | About Us page | None | - |
| `about/` | GET | About page | None | - |
| `owner/` | GET | Owner dashboard | Session-based | - |

## Media Serving
- **Media Files**: Serves media files when `DEBUG=True` (configured in `Agrokart/urls.py`)

## Authentication Requirements
- **Login Required**: User must be authenticated
- **Staff Required**: User must have staff privileges (`is_staff=True`)
- **Session-based**: Requires specific session flag (e.g., owner access)

## Data Formats
- **GET Requests**: Typically return HTML pages or JSON data
- **POST Requests**: Accept form data or JSON payloads
- **JSON Responses**: Most API endpoints return JSON with `success` boolean and relevant data

## Error Handling
- Standard HTTP status codes (200, 400, 404, 500)
- JSON responses include `success` flag and error messages
- User-friendly error messages for frontend display

## Security Considerations
- CSRF protection enabled for forms
- Authentication required for sensitive operations
- Staff permissions required for admin operations
- Input validation on all endpoints

## Usage Examples

### Getting Product List
```bash
curl http://localhost:8000/api/products/
```

### Creating a New Order
```javascript
// JavaScript example
fetch('/add-to-cart/', {
    method: 'POST',
    headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': getCSRFToken()
    },
    body: JSON.stringify({
        product_id: 1,
        quantity: 2
    })
})
```

### Checking Stock Alerts
```bash
curl http://localhost:8000/api/stock-alerts/count/
```

This documentation covers all 40+ URL patterns in your Agrokart application, providing a comprehensive reference for developers and API consumers.
