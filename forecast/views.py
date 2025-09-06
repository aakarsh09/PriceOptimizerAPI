from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from datetime import date, timedelta
from products.models import Product, Sales
from .models import DemandForecast
import random 
from dateutil.relativedelta import relativedelta 
from .serializers import ProductChartDataSerializer


class DemandForecastView(APIView):

    def post(self, request):
        product_ids = request.data.get('product_ids', None)

        # Filter products to forecast
        if product_ids:
            products = Product.objects.filter(id__in=product_ids)
        else:
            products = Product.objects.all()

        if not products.exists():
            return Response({"detail": "No products found for forecasting."}, status=status.HTTP_404_NOT_FOUND)

        forecast_months = 1
        model_version = "v1.0"

        for product in products:
            # Delete old forecasts for this product (optional)
            DemandForecast.objects.filter(product=product).delete()

            total_forecast = 0

            for month_offset in range(forecast_months):
                forecast_date = (date.today().replace(day=1) + relativedelta(months=+month_offset))

                # Simulate a monthly demand forecast
                forecasted_demand = random.randint(100, 500)  # monthly range
                total_forecast += forecasted_demand

                DemandForecast.objects.create(
                    product=product,
                    forecast_date=forecast_date,
                    forecasted_demand=forecasted_demand,
                    model_version=model_version
                )

            # Update cached field in the product table
            product.demand_forecast = total_forecast
            product.save()

        return Response({
            "detail": f"Monthly demand forecast generated for {products.count()} products.",
        }, status=status.HTTP_200_OK)

class ChartDataView(APIView):
    def post(self, request):
        product_ids = request.data.get('product_ids', [])

        if not product_ids:
            return Response({"error": "product_ids is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product_ids = [int(pid) for pid in product_ids]
        except ValueError:
            return Response({"error": "Invalid product_ids format"}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(id__in=product_ids).prefetch_related('sales', 'forecasts')

        if not products.exists():
            return Response({"error": "No products found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductChartDataSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)