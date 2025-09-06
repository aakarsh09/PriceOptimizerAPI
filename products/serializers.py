from rest_framework import serializers
from .models import Product, Sales


class ProductSerializer(serializers.ModelSerializer):
    units_sold = serializers.IntegerField(read_only=True)
    customer_rating = serializers.FloatField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'category',
            'cost_price',
            'stock_available',
            'customer_rating',
            'demand_forecast',
            'optimized_price',
            'units_sold',
            'description'
        ]


from rest_framework import serializers
from .models import Product, Sales

class SaleWithProductSerializer(serializers.ModelSerializer):
    # Flatten product fields
    name = serializers.CharField(source='product.name')
    category = serializers.CharField(source='product.category')
    cost_price = serializers.DecimalField(source='product.cost_price', max_digits=10, decimal_places=2)
    selling_price = serializers.DecimalField(max_digits=10, decimal_places=2)  # from Sales
    stock_available = serializers.IntegerField(source='product.stock_available')
    customer_rating = serializers.FloatField(required=False, allow_null=True)
    demand_forecast = serializers.FloatField(required=False, allow_null=True)
    optimized_price = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=False, allow_null=True
    )
    description = serializers.CharField(source='product.description', allow_blank=True, allow_null=True)

    class Meta:
        model = Sales
        fields = [
            'id',
            'name',
            'category',
            'cost_price',
            'selling_price',      # from Sales
            'stock_available',
            'customer_rating',
            'demand_forecast',
            'optimized_price',
            'description',
            'units_sold',
        ]

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        product, _ = Product.objects.get_or_create(
            name=product_data['name'],
            category=product_data['category'],
            defaults=product_data
        )
        return Sales.objects.create(product=product, **validated_data)

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product', None)

        # Update sales data
        instance.units_sold = validated_data.get('units_sold', instance.units_sold)
        instance.selling_price = validated_data.get('selling_price', instance.selling_price)
        instance.save()

        # Update product data if provided
        if product_data:
            product = instance.product
            for field, value in product_data.items():
                setattr(product, field, value)
            product.save()

        return instance
