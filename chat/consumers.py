import json
from m_benz.models import Car 
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message,Room
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.car_id = self.scope["url_route"]["kwargs"]["car_id"]
        self.user = self.scope["user"]
        self.car = await self.get_car(self.car_id)
        self.owner = self.car.owner

        

        if "user_id" in self.scope["url_route"]["kwargs"]:
            
            self.received_id = self.scope["url_route"]["kwargs"]["user_id"]
            user2 = await self.get_user(self.received_id)
            
            room, created = await self.get_or_create_room(self.user, user2)
            self.group_name = f"chat_car_{self.car_id}_{room.id}"
        else:
            room, created = await self.get_or_create_room(self.user, self.owner)
            self.group_name = f"chat_car_{self.car_id}_{room.id}"
        
        self.room = room

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    # загружаем историю сообщений
        messages = await database_sync_to_async(list)(
            Message.objects.filter(room=room)
            .order_by("created")
            .values("sender__username", "text", "created")
        )
        for msg in messages:
            await self.send(text_data=json.dumps({
                "message": msg["text"],
                "sender_name": msg["sender__username"],
                "created": str(msg["created"])
            }))
    
    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data or "{}")
        message = data.get("message", "")
        
        
        await database_sync_to_async(Message.objects.create)(
            car=self.car,
            sender=self.user,
            room = self.room,
            text = message,
        )

        await self.channel_layer.group_send(self.group_name, {
            "type": "chat_message",
            "message": message,
            "sender_id": self.user.id,
            "room_id": self.room.id,
            "sender_name": self.user.username, 
        })

    
    
    
    async def chat_message(self,event):
        await self.send(text_data=json.dumps({
            "message":event["message"],
            "sender_id":event["sender_id"],
            "sender_name": event["sender_name"],
            "room_id": event["room_id"],
            }))
    
    @database_sync_to_async
    def get_car(self, car_id):
        return Car.objects.select_related("owner").get(id=car_id)
    
    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    def get_or_create_room(self, user_a, user_b):
        return Room.objects.get_or_create(
            user_a=min(user_a, user_b, key=lambda u: u.id),
            user_b=max(user_a, user_b, key=lambda u: u.id),
        )