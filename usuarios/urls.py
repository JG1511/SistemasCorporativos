from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('signUp/', views.user_signUp, name ='signUp')
]