from django.db import models
from products.models import Product

class DemandForecast(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='forecasts')
    forecast_date = models.DateField()
    forecasted_demand = models.IntegerField()
    model_version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.name} forecast on {self.forecast_date}"