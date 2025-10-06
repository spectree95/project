from django.urls import path
from . import views
app_name = "store"
urlpatterns = [
    path("add_to_cart/<int:car_id>",views.add_to_cart,name="add_to_cart"),
    path("cart", views.cart, name="cart"),
    path("remove_cart/<int:item_id>", views.remove_cart,name="remove_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("my_orders/", views.my_orders, name="my_orders"),
    path("toggle_favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("favorites/",views.favorites,name="favorites"),
    path("liked/",views.liked,name="liked"),
]
 