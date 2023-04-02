from django.contrib import admin
from .models import User, Product, Order, OrderItem, MarketBasketCharts, AssociationRules, RFMTable
# Register your models here.

admin.site.register(User)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(MarketBasketCharts)
admin.site.register(AssociationRules)
admin.site.register(RFMTable)