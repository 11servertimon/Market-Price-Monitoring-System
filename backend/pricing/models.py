from django.db import models

from products.models import Product
from stores.models import Store


class PriceRecord(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='price_records')
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='price_records')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10)
    captured_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-captured_at']
        unique_together = ('product', 'store', 'captured_at')

    def __str__(self):
        return f"{self.product} - {self.store}: {self.price} {self.currency}"
