from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Car, CarImage
from .forms import CarForm
from django.http import Http404
from django.http import JsonResponse
# Create your views here.
def home(request):
    return render(request,"m_benz/Nurbol.html")

def showroom(request):
    cars = Car.objects.all()
    context = {'cars': cars}
    return render(request,"m_benz/showroom.html",context)

def car(request,car_id):
    car = Car.objects.get(id=car_id)
    return render(request, 'm_benz/car.html', {'car': car})
    
    
def available_cars(request):
    cars = Car.objects.all()
    available_carss = []
    for car in cars:
        if car.quantity > 0:
            available_carss.append(car)
    context = {"available_cars":available_carss}
    return render(request, 'm_benz/available_cars.html',context)
    
    
@login_required    
def add_car(request):
    if request.method == "GET":
        form = CarForm()
    else:
        form = CarForm(request.POST,request.FILES)
        if form.is_valid():
            new_car = form.save(commit=False)
            new_car.owner = request.user 
            new_car.save()
            images = request.FILES.getlist('image')
            for img in images:
                CarImage.objects.create(car=new_car, image=img)
            return redirect("m_benz:showroom")
    context = {"form":form}
    return render(request,"m_benz/add_car.html",context)

def my_cars(request):
    cars = Car.objects.filter(owner=request.user)
    context = {"cars": cars}
    return render(request,"m_benz/my_cars.html",context)
    
    
@login_required
def edit_car(request,car_id):
    car = Car.objects.get(id=car_id)
    check_car_owner(request,car)
    if request.method == "GET":
        form = CarForm(instance=car)
    else:
        form = CarForm(request.POST, request.FILES, instance=car)
        if form.is_valid():
            form.save()
            for img in request.FILES.getlist("images"):
                CarImage.objects.create(image=img, car=car)
            return redirect("m_benz:showroom")
    context={"car":car,"form":form}
    return render(request,"m_benz/edit_car.html",context)    
    
def check_car_owner(request,car):
    if request.user != car.owner:
        raise Http404

@login_required
def car_delete(request,car_id):
    car = get_object_or_404(Car, id=car_id, owner=request.user)
    car.delete()
    return redirect("m_benz:my_cars")