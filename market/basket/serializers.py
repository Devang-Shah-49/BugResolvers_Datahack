from rest_framework import serializers
from .models import User, Product, Order, OrderItem, MarketBasketCharts, AssociationRules, RFMTable

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('client_id', 'email', 'last_transaction','first_name','last_name')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('item_name', 'price', 'season')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('order_id', 'client_id', 'order_date', 'order_status')

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('order', 'item_name')

class MarketBasketChartsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MarketBasketCharts
        fields = '__all__'

class AssociationRulesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssociationRules
        fields = '__all__'

class RFMTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = RFMTable
        fields = '__all__'