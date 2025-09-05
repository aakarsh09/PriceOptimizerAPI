from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    cost_price = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    stock_available = models.IntegerField()
    units_sold = models.IntegerField()
    customer_rating = models.FloatField(null=True, blank=True)
    demand_forecast = models.IntegerField(null=True, blank=True)
    optimized_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'products'

    def __str__(self):
        return self.name
