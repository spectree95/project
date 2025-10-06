from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from m_benz.models import Car
from .models import Message,Room
from django.contrib.auth import get_user_model
from django.db.models import Q
# Create your views here.


def chat_owner(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    owner_id = car.owner.id
    ids = sorted([owner_id,request.user.id])
    room = f"chat_car_{car_id}_{ids[0]}_{ids[1]}"
    return render(request,"chat/chat_owner.html",{"car":car,})





def chat_tg(request):
    rooms = Room.objects.filter(
        Q(user_a = request.user) | Q(user_b = request.user)
    ).distinct()
    return render(request, "chat/chat_tg.html", {"rooms": rooms})