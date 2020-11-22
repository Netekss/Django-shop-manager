from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Categories"


class Item(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, models.CASCADE)
    price = models.FloatField()
    description = models.TextField()
    quantity_on_stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title
