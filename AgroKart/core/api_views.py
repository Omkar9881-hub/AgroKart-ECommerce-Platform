from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
import json
import logging
from .models import Product, Feedback, ProductFeedback, CustomerInquiry

logger = logging.getLogger(__name__)

@csrf_exempt
@login_required
def submit_product_feedback(request):
    """API endpoint for submitting product feedback"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            rating = data.get('rating')
            comment = data.get('comment', '')
            
            if not product_id or not rating:
                return JsonResponse({'success': False, 'message': 'Product ID and rating are required'})
            
            if rating < 1 or rating > 5:
                return JsonResponse({'success': False, 'message': 'Rating must be between 1 and 5'})
            
            # Create or update feedback
            feedback, created = ProductFeedback.objects.get_or_create(
                product_id=product_id,
                user=request.user,
                defaults={'rating': rating, 'comment': comment}
            )
            
            if not created:
                feedback.rating = rating
                feedback.comment = comment
                feedback.save()
            
            return JsonResponse({'success': True, 'message': 'Feedback submitted successfully!'})
            
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@login_required
def get_product_ratings(request, product_id):
    """API endpoint for fetching product ratings"""
    try:
        product = Product.objects.get(id=product_id)
        feedbacks = Feedback.objects.filter(product=product)
        
        total_ratings = feedbacks.count()
        avg_rating = feedbacks.aggregate(Avg('rating'))['rating__avg'] or 0
        
        return JsonResponse({
            'success': True,
            'product': product.name,
            'total_ratings': total_ratings,
            'avg_rating': round(avg_rating, 1),
            'ratings': list(feedbacks.values('rating', 'comment', 'user__username', 'created_at'))
        })
        
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Product not found'})

@login_required
def get_feedback_report(request):
    """API endpoint for admin feedback reports"""
    feedback_stats = Feedback.objects.values('product__name').annotate(
        avg_rating=Avg('rating'),
        total_ratings=Count('id')
    ).order_by('-avg_rating')

    return JsonResponse({
        'success': True,
        'feedback_stats': list(feedback_stats),
        'total_feedback': Feedback.objects.count(),
        'avg_rating': Feedback.objects.aggregate(Avg('rating'))['rating__avg'] or 0
    })

@login_required
def welcome(request):
    """API endpoint that logs request and returns welcome message"""
    logger.info(f"Request received: {request.method} {request.path}")
    return JsonResponse({'message': 'Welcome to AgroKart API!'})

@login_required
def get_customer_inquiries(request):
    """API endpoint for fetching customer inquiries"""
    try:
        inquiries = CustomerInquiry.objects.all().order_by('-created_at')
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
        return JsonResponse({
            'success': True,
            'inquiries': inquiry_list
        })
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
