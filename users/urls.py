from django.urls import path,include
from . import views
app_name = 'users'
urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('login',views.login_view, name='login'),
    path('register/',views.register, name="register"),
]
