from django.urls import re_path,path
from .consumers import ChatConsumer


websocket_urlpatterns = [
    re_path(r"ws/chat_owner/(?P<car_id>\d+)/$", ChatConsumer.as_asgi()),
    path("ws/chat/<int:car_id>/<int:user_id>/<int:other_user_id>/", ChatConsumer.as_asgi()),
]