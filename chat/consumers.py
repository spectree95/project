import json
from m_benz.models import Car 
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from .models import Message,Room
from django.contrib.auth import get_user_model
User = get_user_model()


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if hasattr(self.user, "_wrapped") and self.user._wrapped is not None:
            self.user = self.user._wrapped
        car_id = self.scope["url_route"]["kwargs"].get("car_id")
        if car_id:
            car = await self.get_car(car_id)
            owner = car.owner
            print("car:", car)
            print("owner:", owner)
            print("type(owner):", type(owner))
            room , created = await self.get_or_create_room(car, self.user, owner)
            self.group_name = f"chat_car_{room.id}"
            self.room = room
            await self.channel_layer.group_add(self.group_name, self.channel_name)
        else:
            pass
        await self.accept()
    
       
    
    async def receive(self, text_data):
        data = json.loads(text_data or "{}")
        command = data.get("command",None)
        
        if command == "join":
            room_id = data.get("room_id")
            self.car_id = data.get("car_id")
            await self.join_room(room_id)
            return
        
        elif command == "send":
            message = data.get("message", "")
            car_id = int(data.get("car_id", ""))
            room_id = data.get("room_id", "")
            if room_id:
                self.room = await database_sync_to_async(Room.objects.get)(id=room_id)
            car = await database_sync_to_async(Car.objects.get)(id=car_id)
            
            await database_sync_to_async(Message.objects.create)(
                car=car,
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
                "car_id": car_id 
            }) 
         
        
            
        
        
        
        

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    
    
    async def chat_message(self,event):
        await self.send(text_data=json.dumps({
            "message":event["message"],
            "sender_id":event["sender_id"],
            "sender_name": event["sender_name"],
            "room_id": event["room_id"],
            }))
    
    
    
    async def join_room(self, room_id):
        if getattr(self, "group_name", None):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

        room = await database_sync_to_async(Room.objects.get)(id=room_id)
        self.group_name = f"chat_car_{room.id}"
        
        
        await self.channel_layer.group_add(self.group_name, self.channel_name)
    
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
    
    
    
    
    
    
    
    @database_sync_to_async
    def get_car(self, car_id):
        return Car.objects.select_related("owner").get(id=car_id)
    
    @database_sync_to_async
    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    @database_sync_to_async
    
    def get_or_create_room(self, car, user_a, user_b):
        print("user_a:", user_a, type(user_a))
        print("user_b:", user_b, type(user_b))

        if not hasattr(user_a, "id") or not hasattr(user_b, "id"):
            raise ValueError("user_a или user_b не пользователь!")
        user_a, user_b = sorted([user_a, user_b], key=lambda u: u.id)

    # Ищем или создаём комнату для этой пары и машины
        return Room.objects.get_or_create(
        car=car,
        user_a=user_a,
        user_b=user_b
    )
        
    