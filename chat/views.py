from django.shortcuts import render,get_object_or_404
from m_benz.models import Car
from .models import Room,Message
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from itertools import groupby
from django.utils.timezone import localtime
# Create your views here.

@login_required
def chat_owner(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request,"chat/chat_owner.html",{"car":car,})




@login_required
def chat_tg(request):
    rooms = Room.objects.filter(
        Q(user_a = request.user) | Q(user_b = request.user)
    ).distinct().order_by("latest_message__created")
    return render(request, "chat/chat_tg.html", {"rooms": rooms})