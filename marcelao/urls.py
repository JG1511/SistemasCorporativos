from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name= "index"),
    path("<int:correntista_id>/", views.extrato_por_correntista, name= "extrato_por_correntista"),
    path("deposito/<int:correntista_id>/", views.realizar_deposito, name= "realizar_deposito"),
    path("transferencia/<int:correntista_id>/", views.realizar_transferencia, name= "realizar_transferencia"),
    path("pagamento/<int:correntista_id>/", views.pagamento, name= "pagamento"),
    path("saque/<int:correntista_id>/", views.realizar_saque, name= "realizar_saque"),
    
]