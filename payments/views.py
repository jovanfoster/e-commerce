from django.shortcuts import render
from django.conf import settings 
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import stripe

from users.models import Order

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


def create_checkout_session(request):
    items_to_purchase = []
    if request.user.is_authenticated:
        for order_item in request.user.order.item.all():
            item = {
                'name': order_item.product.name,
                'quantity': order_item.quantity,
                'currency': 'cad',
                'amount': order_item.product.serialized_price.replace('.', ''),
            }
            items_to_purchase.append(item)
    else:
        if 'cart' in request.session:
            for key, order_item in request.session['cart'].items():
                item = {
                    'name': order_item['product']['name'],
                    'quantity': order_item['quantity'],
                    'currency': 'cad',
                    'amount': order_item['product']['price'].replace('.', ''),
                }
                items_to_purchase.append(item)

    if request.method == 'GET':
        domain_url = 'http://localhost:3000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'payment/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'payment/cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=items_to_purchase
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


def success(request):
    user = request.user

    if user.is_authenticated:
        order               =   Order.objects.get(user=user)
        order.completed     =   True
        user.order.delete()
        user.order          =   Order.objects.create(user=user)          

    else:
        request.session['cart'] = {}

    return render(request, 'payments/success.html')


def cancelled(request):
    return render(request, 'payments/cancelled.html')
