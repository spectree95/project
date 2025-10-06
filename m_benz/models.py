from django.db import models
from django.contrib.auth.models import User 
from django.conf import settings
import os
# Create your models here.
class Car(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    description = models.TextField()
    year = models.IntegerField(blank=False,null=False)
    price = models.DecimalField(max_digits=20, decimal_places=2, blank=False, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    city = models.CharField(max_length=100,blank=False,null=False)
    generation = models.CharField(max_length=100,blank=False,null=False)
    car_body = models.CharField(max_length=100,blank=False,null=False)
    engine_capacity = models.FloatField(blank=False,null=False)
    mileage = models.IntegerField(blank=False,null=False)
    drivetrain = models.CharField(max_length=100,blank=False,null=False)
    drive_type = models.CharField(max_length=50,blank=False,null=False)
    steering_wheel = models.CharField(max_length=50,blank=False,null=False)
    color = models.CharField(max_length=50,blank=False,null=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    quantity = models.IntegerField(blank=False,null=False)
    def __str__(self):
        return self.name
 
def car_image_upload_path(instance, filename):
    car = instance.car  
    car_folder = f"{car.name.replace(' ', '_').lower()}_{car.id}"  # amg_gt_5
    ext = filename.split('.')[-1]
    filename = f"{instance.id or 'image'}.{ext}"
    return os.path.join("car_images", car_folder, filename)

class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")   
    image = models.ImageField(upload_to=car_image_upload_path, blank=False,null=False)
    

        