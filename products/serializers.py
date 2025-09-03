from rest_framework import serializers
from .models import Product  

class ProductSerializer(serializers.ModelSerializer):
    customer_rating = serializers.FloatField(required=False, allow_null=True)
    demand_forecast = serializers.IntegerField(required=False, allow_null=True)
    optimized_price = serializers.DecimalField(required=False, allow_null=True, max_digits=10, decimal_places=2)
        
    class Meta:
        model = Product
        exclude = ['id']