from django.shortcuts import render,redirect, get_object_or_404
from m_benz.models import Car
from django.contrib.auth.decorators import login_required
from .models import CartItem,Order,OrderItem,Favorite
from django.contrib import messages
from django.db import transaction
from .forms import CheckoutForm
from django.http import JsonResponse
# Create your views here.

@login_required
def cart(request):
    item = CartItem.objects.filter(user=request.user)
    cart_quantity = sum(i.quantity for i in item)
    total_sum = sum(i.car.price for i in item)
    context = {"item":item,"cart_quantity":cart_quantity, "total_sum":total_sum}
    return render(request, "store/cart.html",context)
    

@login_required
def add_to_cart(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    quantity = int(request.POST.get('quantity', 1))

    # Проверка: уже есть такая запись?
    cart_item, created = CartItem.objects.get_or_create(
        user=request.user,
        car=car,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    
    messages.success(request, f"{car.name} ({quantity} шт.) добавлен в корзину!")

    return redirect("m_benz:car", car_id=car.id)  


@login_required
def remove_cart(request,item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, user=request.user)
    cart_item.delete()
    return redirect("store:cart")


@login_required
def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_car = sum(item.car.price * item.quantity for item in cart_items)
    total = sum(item.car.price * item.quantity for item in cart_items) + 100
    cart_quantity = sum(item.quantity for item in cart_items)
    if not cart_items.exists():
        return redirect("store:cart")
    
    for item in cart_items:
        if item.quantity > item.car.quantity:
            messages.error(request, f"Машины '{item.car}' недостаточно в наличии")
            return redirect("store:cart")
        
    if request.method == "POST":
        form = CheckoutForm(request.POST)
        if form.is_valid():
            
            with transaction.atomic():
                order = Order.objects.create(
                    user = request.user,
                    total_price = total,
                    city = form.cleaned_data["city"],
                    street = form.cleaned_data["street"],
                    house = form.cleaned_data["house"],
                    payment_method = form.cleaned_data["payment_method"],
                    comment = form.cleaned_data["comment"],
                )
                for item in cart_items:
                    OrderItem.objects.create(
                        order = order,
                        car = item.car, 
                        quantity = item.quantity,
                        price_at_purchase = item.car.price,
                    )
                  
                    item.car.quantity -= item.quantity
                    item.car.save()
                cart_items.delete()
            return render(request,"store/order_success.html", {"order": order})
    else:
        form = CheckoutForm()
    
    context = {"cart_quantity":cart_quantity, "total":total,"form":form, "cart_items": cart_items,"total_car":total_car}
    return render(request, "store/checkout.html",context)



@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "store/my_orders.html", {"orders":orders})



def toggle_favorite(request):
    if request.method == "POST":
        car_id = request.POST.get("car_id")
        car = Car.objects.filter(id=car_id).first()
        if not car:
            return JsonResponse({"error": "car not found"}, status=404)
        fav ,created = Favorite.objects.get_or_create(user=request.user, car=car)
        if not created:
            fav.delete()
            return JsonResponse({"favorited": False})
        return JsonResponse({"favorited": True})
        
    print(car_id)
    return JsonResponse({"error": "Invalid request"}, status=400)            

def favorites(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("car")
    return render(request,"store/favorites.html",{"favorites": favorites})

def liked(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("car")
    return render(request, "store/liked.html",{"favorites":favorites})
