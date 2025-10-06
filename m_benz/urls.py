from django.urls import path,include
from . import views
app_name = "m_benz"
urlpatterns = [
    path('',views.home, name="Nurbol"),
    path('showroom/', views.showroom, name="showroom"),
    path('car/<int:car_id>/',views.car, name="car"),
    path('add_car/', views.add_car,name="add_car"),
    path('my_cars/',views.my_cars,name='my_cars'),
    path('edit_car/<int:car_id>',views.edit_car,name="edit_car"),
    path("car_delete/<int:car_id>",views.car_delete,name="car_delete"),
]
 