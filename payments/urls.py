from django.urls import path
from . import views

urlpatterns = [
    path('config/', views.stripe_config, name='config'),
    path('create-checkout-session/', views.create_checkout_session, name='checkout'),
    path('success/', views.success, name='success'), 
    path('cancelled/', views.cancelled, name='cancelled'), 
]