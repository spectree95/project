from django.db import models
from m_benz.models import Car
from django.conf import settings
# Create your models here.

class CartItem(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user','car')
        
    def __str__(self):
        return f"{self.car} x {self.quantity}"
    

    
class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=20, decimal_places=3)
    status = models.CharField(max_length=50, default="В обработке")
    city = models.CharField(max_length=50, blank=False, null=False)
    street = models.CharField(max_length=100, blank=False,null=False)
    house = models.CharField(max_length=50, blank=False,null=False)
    payment_method = models.CharField(max_length=100)
    comment = models.TextField(blank=True,null=True)


    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price_at_purchase = models.DecimalField(max_digits=20,decimal_places=3)
    
    
    
    
class Favorite(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ("user", "car")
        
    def __str__(self):
        return f"{self.user.username}, {self.car}"