from rest_framework import serializers
from products.models import Product, Sales
from forecast.models import DemandForecast

class SalesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sales
        fields = ['sale_date', 'units_sold']

class DemandForecastSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemandForecast
        fields = ['forecast_date', 'forecasted_demand']

class ProductChartDataSerializer(serializers.ModelSerializer):
    sales = SalesSerializer(many=True, read_only=True)
    forecasts = DemandForecastSerializer(source='demandforecast_set', many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'sales', 'forecasts']
