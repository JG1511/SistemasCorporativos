from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name= "index"),
    path("<int:correntista_id>/", views.extrato_por_correntista, name= "extrato_por_correntista")
]