from django.db import models
from m_benz.models import Car
from mercedes_benz import settings
# Create your models here.


class Room(models.Model):
    user_a = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="rooms_a")
    user_b = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,related_name="rooms_b")

    @property
    def last_message(self):
        return self.messages.last()
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user_a","user_b"], name="unique_name_pair")
        ]
        
    

class Message(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    sender = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name="sent_messages")
    
    room = models.ForeignKey(Room, on_delete=models.CASCADE,related_name="messages")
        
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ["created"]

    def __str__(self):
        return f"[{self.room}] {self.sender}: {self.text[:30]}"