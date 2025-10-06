from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from .forms import CustomUserCreationForm
from django.contrib import messages
# Create your views here.

def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user:
            login(request,user)
            return redirect("m_benz:showroom")
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
        return render(request, 'users/login.html', {'username': username})
    return render(request, "users/login.html")

def register(request):
    if request.method == "GET":
        form = CustomUserCreationForm()
    else:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user = form.instance
            login(request,new_user)
            return redirect("m_benz:showroom")
    context = {"form":form}
    return render(request,"users/register.html",context)
