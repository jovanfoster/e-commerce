def get_total(request):
    user = request.user
    total = 0
    if user.is_authenticated:
        for item in user.order.item.all():
            total += item.product.price * item.quantity
        return total
    else:
        if 'cart' in request.session:
            for key, item in request.session['cart'].items():
                total += float((item['product']['price']).strip(' "')) * item['quantity']
    return total

from users.models import Order

def get_items(request):
    user = request.user
    quantity = 0
    if user.is_authenticated:
<<<<<<< HEAD
        if not user.order:
            user.order = Order.objects.create(user=user)
=======
        order = Order.objects.get_or_create(user=user)
>>>>>>> tmp
        for item in user.order.item.all():
                quantity += item.quantity
        return quantity
    else:
        if 'cart' in request.session:
            for key, item in request.session['cart'].items():
                quantity += item['quantity']
    return quantity
