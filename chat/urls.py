from django.urls import path
from . import views

app_name = "chat"
urlpatterns = [
    path("chat_owner/<int:car_id>/",views.chat_owner,name="chat_owner"),
    path("chat_tg/",views.chat_tg, name="chat_tg"),
]