from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from marcelao.models import Correntista
from django.contrib.auth import authenticate, login

# Create your views here.

def user_login(request):
    error = None

    if request.method == 'POST':
        user = request.POST.get('username')

        if not user:
            error = 'Nome do usuário é obrigatório'

        if error is None:
            try:
                #Salvando o estado do correntista
                correntista = Correntista.objects.get(NomeCorrentista=user)
                request.session['correntista_id'] = correntista.CorrentistaID
                request.session['correntista_nome'] = correntista.NomeCorrentista

            except Correntista.DoesNotExist:
                return render(request, 'login.html', {'error': 'Usuário não encontrado'})
     
            
            # Redireciona para a index — ela irá ler o correntista da sessão
            return redirect('index')

        return render(request, 'login.html', {'error': error})

    return render(request, 'login.html')

def user_signUp(request):
    error = None

    # retorna todos os nomes dos correntistas
    correntista_all = Correntista.objects.values_list('NomeCorrentista', flat= True)
    
    if request.method == 'POST':
        username = request.POST.get('username')

        # for nome in correntista_all:
        #     if username == nome:
        #         error = 'Esse nome já existe'
        #         break

        if not username:
            error = 'Nome do usuário é obrigatorio'

        if username in correntista_all:
            error = 'Esse nome já existe'
        
        if error is None:
            try:
                correntista = Correntista(NomeCorrentista = username)
                correntista.save()
                return render(request, 'login.html')
            except Exception as e:
                error = f'Não deu para registar o Usuário :{str(e)}'
                return render(request,'signUp.html', {'error': error})
            
    return render(request,'signUp.html', {'error': error})