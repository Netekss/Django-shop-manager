from django.db import models
from warehouse.models import Item


class OrderItem(models.Model):
    item = models.ForeignKey(Item, models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    order_id = models.CharField(max_length=11)
    item_order_id = models.CharField(max_length=100)
    # TODO foreign key to Order

    def __str__(self):
        return f"{self.item.title}-{self.order_id}"

    def get_item_name(self):
        return self.item.title

    def get_item_price(self):
        return self.item.price

    def get_total_item_price(self):
        item_total_price = (self.quantity * self.item.price)
        return item_total_price


class Order(models.Model):
    order_id = models.CharField(max_length=11)
    # TODO we can remove it
    items = models.ManyToManyField(OrderItem)
    creation_date = models.DateTimeField(auto_now_add=True)
    open_status = models.BooleanField(default=True)
    waiting_status = models.BooleanField(default=False)
    send_status = models.BooleanField(default=False)
    close_status = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ['creation_date']

    def __str__(self):
        return self.order_id

    def get_total_price(self):
        order = Order.objects.get(order_id=self.order_id)
        items = order.items.all()
        total = 0

        for item in items:
            total += item.get_total_item_price()
        return total
