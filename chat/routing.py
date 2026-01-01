from django.urls import re_path,path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r"ws/chat_owner/(?P<car_id>\d+)/$", ChatConsumer.as_asgi()),
    re_path(r"ws/chat_tg/$", ChatConsumer.as_asgi()),
]