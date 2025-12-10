from django.db import models


class Store(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    is_online = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
