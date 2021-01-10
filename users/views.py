from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
import json

from .models import Order, OrderItem
from products.models import Product
from ecommerce_website.utils import get_total, get_items

def user_register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        # If form not submitted, render blank form
        form = UserRegisterForm()
 
    context = {'form': form}

    return render(request, 'users/register.html', context)


def user_login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, 'Logged in as %s' % MyUser.objects.get(email=email))
                # Redirect to a success page.
                return redirect('/')
            else:
                # Return an 'invalid login' error message.
                messages.error(request, 'Invalid username or password')
        else:
            messages.error(request, 'Invalid username or password')
    else:
        # If form not submitted, render blank form
        form = UserLoginForm()

    context = {'form': form}

    return render(request, 'users/login.html', context)


def user_logout_view(request):
    logout(request)
    return render(request, 'users/logout.html')
    

def order_view(request):
    if request.user.is_authenticated:
        order       =   request.user.order
        order_items =   order.item.all()
        
    else:
        order_items = []
        if not 'cart' in request.session:
            request.session['cart'] = {}
        for key, item in request.session['cart'].items():
            order_items.append(item)
        

    context     =   {
            'order_items': order_items,
            'items': get_items(request),
            'total': get_total(request)
        }
    return render(request, 'users/order.html', context)


def add_to_cart(request, pk):
    user                    =   request.user
    product                 =   get_object_or_404(Product, pk=pk)

    if user.is_authenticated:     
        order, created          =   Order.objects.get_or_create(user=user)
        order_item, created     =   OrderItem.objects.get_or_create(order=order, product=product)
        order_item.quantity    +=   1
        order_item.save()

    else:        
        if not 'cart' in request.session:
            request.session['cart'] = {}
        if str(product.id) in request.session['cart']:
            request.session['cart'][str(product.id)]['quantity'] += 1
        else:
            request.session['cart'][str(product.id)] = {
                'product': {
                    'pk': product.pk,
                    'name': product.name,
                    'imageURL': product.imageURL,
                    'price': product.serialized_price
                },
                'quantity': 1
            }   

        print('Cart: %s' % request.session['cart']) 

    messages.success(request, 'Item added to cart!', extra_tags='primary')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


def remove_from_cart(request, pk):
    user                    =   request.user
    product                 =   get_object_or_404(Product, pk=pk)

    if user.is_authenticated:     
        order          =   Order.objects.get(user=user)
        order_item     =   OrderItem.objects.get(order=order, product=product)
        order_item.quantity    -=   1
        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()

    else:        
        request.session['cart'][str(product.id)]['quantity'] -= 1
        if request.session['cart'][str(product.id)]['quantity'] <= 0:
            del request.session['cart'][str(product.id)]
    
    messages.warning(request, 'Item removed from cart!')

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

def remove_item_from_cart(request, pk):
    user        =   request.user
    product     =   get_object_or_404(Product, pk=pk)

    if user.is_authenticated:
        order       =   Order.objects.get(user=user)
        order_item  =   OrderItem.objects.get(order=order, product=product)

        order_item.delete()

    else:
        del request.session['cart'][str(product.id)]

    messages.warning(request, 'Item(s) removed from cart!', extra_tags='danger')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
