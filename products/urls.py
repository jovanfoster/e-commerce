from django.urls import path
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('products/<pk>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('products/categories/<pk>/', views.CategoryDetailView.as_view(), name='list-by-category'),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)