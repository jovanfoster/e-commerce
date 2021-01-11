import os

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *

from users.models import MyUser
from ecommerce_website.utils import get_items
from ecommerce_website import settings

from django.views.generic import DetailView, ListView 


# Create your views here.
def home(request):
    featured_products = Product.objects.filter(featured=True)
    categories = Category.objects.all()
    context = {
        'products': featured_products,
        'categories': categories,
        'items': get_items(request)
    }
    
    return render(request, 'products/index.html', context)


class ProductDetailView(DetailView):

    model = Product
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['items'] = get_items(self.request)
        context['categories'] = Category.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        product = self.get_object()

        if user.is_authenticated:
            review = Review.objects.create(
                user=user, 
                product=product, 
                rating=request.POST['rating'],
                summary=request.POST['summary'])

            return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

        else:
            return HttpResponseRedirect(os.path.join(settings.BASE_DIR, '%s?next=%s' % (settings.LOGIN_URL, request.path)))

class CategoryDetailView(DetailView):

    model = Category
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['items'] = get_items(self.request)
        context['products'] = self.object.products.all()
        context['categories'] = Category.objects.all()
        return context
