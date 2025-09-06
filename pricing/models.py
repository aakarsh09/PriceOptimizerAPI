from django.db import models
from products.models import Product


class PriceOptimization(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    demand_forecast = models.ForeignKey(DemandForecast, on_delete=models.SET_NULL, null=True)
    optimized_price = models.DecimalField(max_digits=10, decimal_places=2)
    optimization_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.name} optimized to {self.optimized_price}"
