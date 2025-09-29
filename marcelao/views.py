from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import VwExtrato

# Create your views here.

def index(request):
    
    #retorna todos os dados da vwExtratos
    dados_extratos = VwExtrato.objects.all().order_by('-DataOperacao')

    #Convertendo para JSON
    lista_extrato = list(dados_extratos.values())

    #Retornando como JSON
    return JsonResponse({'extrato': lista_extrato})

def extrato_por_correntista(request,correntista_id):

    dados_extrato = VwExtrato.objects.filter(CorrentistaID=correntista_id).order_by('-DataOperacao')
    
    lista_extrato = list(dados_extrato.values())

    return JsonResponse({'extrato': lista_extrato})
