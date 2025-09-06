from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_available = models.IntegerField()
    customer_rating = models.FloatField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)


    # Cached fields to store latest values
    demand_forecast = models.IntegerField(null=True, blank=True)
    optimized_price = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

class Sales(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sales')
    sale_date = models.DateTimeField(auto_now_add=True)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    units_sold = models.IntegerField()

    def __str__(self):
        return f"Sale of {self.units_sold} units of {self.product.name} on {self.sale_date}"

class DemandForecast(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    forecast_date = models.DateField()
    forecasted_demand = models.IntegerField()
    model_version = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.name} forecast on {self.forecast_date}"

class PriceOptimization(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    demand_forecast = models.ForeignKey(DemandForecast, on_delete=models.SET_NULL, null=True)
    optimized_price = models.DecimalField(max_digits=10, decimal_places=2)
    optimization_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.product.name} optimized to {self.optimized_price}"
