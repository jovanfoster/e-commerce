from django.contrib import admin
from .models import MyUser, Order, OrderItem

# Register your models here.
class ItemInline(admin.TabularInline):
    model = OrderItem


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ItemInline,
    ]

admin.site.register(MyUser)
admin.site.register(Order, OrderAdmin)