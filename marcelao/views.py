from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import VwExtrato, Correntista
from decimal import Decimal  # Importar para garantir o tipo de dado para Valor
from django.contrib import messages
from django.db import transaction, connection

# Create your views here.

# def index(request):
    
#     #retorna todos os dados da vwExtratos
#     dados_extratos = VwExtrato.objects.all().order_by('-DataOperacao')

#     #Convertendo para JSON
#     lista_extrato = list(dados_extratos.values())

#     #Retornando como JSON
#     return JsonResponse({'extrato': lista_extrato})

def extrato_por_correntista(request,correntista_id):

    dados_extrato = VwExtrato.objects.filter(CorrentistaID=correntista_id).order_by('-DataOperacao')
    
    lista_extrato = list(dados_extrato.values())

    return JsonResponse({'extrato': lista_extrato})

def realizar_deposito(request, correntista_id):

    correntista = Correntista.objects.get(CorrentistaID=correntista_id)
    
    context = { 
        'correntista': correntista
    }

    if request.method == 'POST':
        
        try:
            valor_str = request.POST.get('valor_deposito', '0') 
            valor = Decimal(valor_str)  # Convertendo para Decimal

            if valor <= 0:

                messages.error(request, 'O valor do depósito deve ser maior que zero.')
                return render(request, 'marcelao/realizar_deposito.html', context)
        
        except Exception:
            messages.error(request, 'Valor inválido. Por favor, insira um número válido.')
            return render(request, 'marcelao/realizar_deposito.html', context)


        try:
            with transaction.atomic(): # serve para garantir que todas as operações dentro do bloco sejam concluídas com sucesso ou nenhuma delas seja aplicada em caso de erro.
                with connection.cursor() as cursor: # serve para criar um cursor de banco de dados que permite executar comandos SQL diretamente.
                    
                    cursor.execute("SELECT sp_deposito(%s, %s)", [correntista_id, valor])
                    messages.success(request, 'Depósito realizado com sucesso!')
                    return render(request, 'marcelao/realizar_deposito.html', context)

        except Exception as e:
            messages.error(request, f'Erro ao realizar o depósito: {str(e)}')
            return render(request, 'marcelao/realizar_deposito.html', context)

    else:
        return render(request, 'marcelao/realizar_deposito.html', context)
    
def realizar_saque(request,correntista_id):
    correntista = Correntista.objects.get(CorrentistaID=correntista_id)

    context = {
        'correntista': correntista
    }

    if request.method == 'POST':
        try:
            valor_str = request.POST.get('valor_saque', '0') 
            valor_de_saque = Decimal(valor_str)

            if valor_de_saque <= 0:
                messages.error(request, 'O valor do saque deve ser maior que zero.')
                return render(request, 'marcelao/form_saque.html', context)
        except Exception:
            messages.error(request, 'Valor inválido. Por favor, insira um número válido.')
            return render(request, 'marcelao/form_saque.html', context)
        try:
            with transaction.atomic(): # o transaction.atomic() serve para garantir que todas as operações dentro do bloco sejam concluídas com sucesso ou nenhuma delas seja aplicada em caso de erro.
                with connection.cursor() as cursor:
                    cursor.execute("SELECT sp_saque(%s,%s)", [correntista_id, valor_de_saque])
                    messages.success(request, 'Saque realizado com sucesso!')
                    return render(request,'marcelao/form_saque.html', context)
                
        except Exception as e: # captura qualquer exceção que possa ocorrer durante a execução do bloco try.
            messages.error(request, f'Erro ao realizar o saque: {str(e)}')
            return render(request, 'marcelao/form_saque.html', context)
    else:
        return render(request, 'marcelao/form_saque.html', context)

def realizar_transferencia(request, correntista_id):
    correntista = Correntista.objects.get(CorrentistaID=correntista_id)

    context = {
        'correntista': correntista
    }

    if request.method == 'POST':
        try:
            valor_str = request.POST.get('valor_transferencia', '0') 
            valor_de_transferencia = Decimal(valor_str)
            beneficiario_id = int(request.POST.get('beneficiario_id', '0'))

            if valor_de_transferencia <= 0:
                messages.error(request, 'O valor da transferência deve ser maior que zero.')
                return render(request, 'marcelao/form_transferencia.html', context)
            if beneficiario_id <= 0:
                messages.error(request, 'Beneficiário inválido.')
                return render(request, 'marcelao/form_transferencia.html', context)
            
            if beneficiario_id == correntista_id:
                messages.error(request, 'Não é possível transferir para si mesmo.')
                return render(request, 'marcelao/form_transferencia.html', context)
        
        except Exception:
            messages.error(request, 'Valor inválido. Por favor, insira um número válido.')
            return render(request, 'marcelao/form_transferencia.html', context)
        
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT sp_transferencia(%s,%s,%s)", [correntista_id, beneficiario_id, valor_de_transferencia])
                    messages.success(request, 'Transferência realizada com sucesso!')
                    return render(request, 'marcelao/form_transferencia.html', context)
                
        except Exception as e:
            messages.error(request, f'Erro ao realizar a transferência: {str(e)}')
            return render(request, 'marcelao/form_transferencia.html', context)

    return render(request, 'marcelao/form_transferencia.html', context)

def pagamento(request,correntista_id):
    correntista = Correntista.objects.get(CorrentistaID=correntista_id)

    context = {
        'correntista': correntista
    }

    if request.method == 'POST':
        
        try:
            valor_str = request.POST.get('valor_pagamento', '0') 
            valor_de_pagamento = Decimal(valor_str)
            descricao = request.POST.get('descricao')

            if valor_de_pagamento <= 0:
                messages.error(request, 'O valor do pagamento deve ser maior que zero.')
                return render(request, 'marcelao/form_pagamento.html', context)
        
            if not descricao:
                messages.error(request, 'A descrição do pagamento não pode estar vazia.')
                return render(request, 'marcelao/form_pagamento.html', context)
        
        except Exception:
            messages.error(request, 'Valor inválido. Por favor, insira um número válido.')
            return render(request, 'marcelao/form_pagamento.html', context)
        
        try:
            with transaction.atomic():
                with connection.cursor() as cursor:
                    cursor.execute("SELECT sp_pagamento(%s,%s,%s)", [correntista_id, valor_de_pagamento, descricao])
                    messages.success(request, 'Pagamento realizado com sucesso!')
                    return render(request, 'marcelao/form_pagamento.html', context)
        except Exception as e:
            messages.error(request, f'Erro ao realizar o pagamento: {str(e)}')
            return render(request, 'marcelao/form_pagamento.html', context)
    
    return render(request, 'marcelao/form_pagamento.html', context)


def index(request):
    return render(request, 'marcelao/main.html')


        
        
        
        