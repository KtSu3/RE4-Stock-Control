from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from rest_framework import viewsets
from django.views.decorators.csrf import csrf_exempt
import json
from .serializers import ListVSerializer
from .models import EquipamentoRegistrado, EquipamentoEmTeste, EquipamentoTestado, EquipamentoReteste, EquipamentoRetestado, EquipamentoParaCampo, CadastroViabilidade, CadastroTecnicos, Status
from django.contrib.auth import authenticate, login
from .forms import CustomUserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
#----------------------------------------------------------------------------------------------------------------------------------------------------------#

#Views HTML Render
def cv(request):
    return render(request, 'ApPj/CadastroV.html')

@login_required
def ct(request):
    return render(request, 'ApPj/CadastrarTec.html')

@login_required
def index(request):
    return render(request, 'App/Index.html')

#----------------------------------------------------------------------------------------------------------------------------------------------------------#
#API response
class ListViewSet(viewsets.ModelViewSet):
    queryset = CadastroViabilidade.objects.all()
    serializer_class = ListVSerializer






#----------------------------------------------------------------------------------------------------------------------------------------------------------#
#Views para exibir Banco

@login_required
def list_reteste(request):
    reteste = EquipamentoReteste.objects.all()
    paginator = Paginator(reteste, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'App/Reteste.html', {
        'page_obj': page_obj,
    })

@login_required
def campo(request):
    emcampo = EquipamentoParaCampo.objects.filter(status=Status.CAMPO)
    paginator = Paginator(emcampo, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'App/EqCampo.html', {'page_obj': page_obj})

@login_required
def tc(request):
    tecnicos = CadastroTecnicos.objects.filter()
    paginator = Paginator(tecnicos, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ApPj/TecCadastrados.html', {'page_obj': page_obj})

@login_required
def teste_concluido(request):
    equipamentos = EquipamentoTestado.objects.all()
    paginator = Paginator(equipamentos, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'App/EqTestados.html', {'page_obj': page_obj})

@login_required
def retestado(request):
    equipamentos = EquipamentoRetestado.objects.all()
    paginator = Paginator(equipamentos, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'App/EqRetestados.html', {'page_obj': page_obj})

@login_required
def vc(request):
    viabilidades = CadastroViabilidade.objects.all()
    paginator = Paginator(viabilidades, 200)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'ApPj/ViabilidadesC.html', {'page_obj': page_obj})


@login_required
def testar(request):
    emteste = EquipamentoEmTeste.objects.all()
    paginator = Paginator(emteste, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'App/Testar.html', {'page_obj': page_obj})

@login_required
def list_equipamentos(request):
    registrados = EquipamentoRegistrado.objects.filter(status='C')
    paginator = Paginator(registrados, 30)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    em_teste = EquipamentoEmTeste.objects.filter(status='ET')
    testados = EquipamentoTestado.objects.filter(status='Testado')
    retestado = EquipamentoRetestado.objects.filter(status='Retestado')
    campo = EquipamentoParaCampo.objects.filter(status='CP')
    

    return render(request, 'App/EqCadastrados.html', {  
        'page_obj': page_obj,
        'em_teste': em_teste,
        'testados': testados,
        'retestado': retestado,
        'campo': campo,
        
        
    })

#----------------------------------------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------------------------------------------#
#Mudança de Status TESTE
@csrf_exempt
@login_required
def mudar_status_equipamento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        equipamento_id = data.get('id')
        new_status = data.get('status')
        relato_teste = data.get('relato_teste', '')

        if equipamento_id and new_status:
            if new_status == 'ET':
                equipamento = get_object_or_404(EquipamentoRegistrado, id=equipamento_id)
                EquipamentoEmTeste.objects.create(
                    equipamento=equipamento.equipamento,
                    modelo=equipamento.modelo,
                    fabricante=equipamento.fabricante,
                    problema=equipamento.problema,
                    mac=equipamento.mac,
                    status=Status.EMTESTE,
                    usuario=request.user
                )
                equipamento.delete()
                
            elif new_status == 'T':
                equipamento = get_object_or_404(EquipamentoEmTeste, id=equipamento_id)
                EquipamentoTestado.objects.create(
                    equipamento=equipamento.equipamento,
                    modelo=equipamento.modelo,
                    fabricante=equipamento.fabricante,
                    problema=equipamento.problema,
                    mac=equipamento.mac,
                    relato_teste=relato_teste,
                    status=Status.TESTADO,
                    usuario=request.user
                )
                equipamento.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'ID do equipamento ou status não fornecido'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Método inválido'}, status=405)
    


#Mudança de Status CAMPO
@csrf_exempt
@login_required
def mudar_status_campo(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        equipamento_id = data.get('id')
        new_status = data.get('status')

        if equipamento_id and new_status == 'T':
            equipamento = get_object_or_404(EquipamentoTestado, id=equipamento_id)
            EquipamentoParaCampo.objects.create(
                modelo=equipamento.modelo,
                equipamento=equipamento.equipamento,
                fabricante=equipamento.fabricante,
                problema=equipamento.problema,
                relato_teste=equipamento.relato_teste,
                mac=equipamento.mac,
                status=Status.CAMPO,
                usuario=request.user
            )
            equipamento.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'ID do equipamento ou status inválido'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Método inválido'}, status=405)
    

#Mudança de Status RETESTADO
@csrf_exempt
@login_required
def mudar_status_retestado(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        equipamento_id = data.get('id')
        new_status = data.get('status')
        relato_teste = data.get('relato_teste', '')

        if equipamento_id and new_status:
            if new_status == 'RE':
                equipamento = get_object_or_404(EquipamentoReteste, id=equipamento_id)
                EquipamentoRetestado.objects.create(
                    equipamento=equipamento.equipamento,
                    modelo=equipamento.modelo,
                    fabricante=equipamento.fabricante,
                    problema=equipamento.problema,
                    mac=equipamento.mac,
                    relato_teste=relato_teste,
                    status=Status.RETESTADO,
                    usuario=request.user
                )
                equipamento.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'ID do equipamento ou status não fornecido'}, status=400)
    else:
        return JsonResponse({'success': False, 'error': 'Método inválido'}, status=405)
#----------------------------------------------------------------------------------------------------------------------------------------------------------#

#----------------------------------------------------------------------------------------------------------------------------------------------------------#
#View para adicionar Equipamento
@csrf_exempt
@login_required
def add_equipamento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        equipamento = data.get('equipamento')
        modelo = data.get('modelo')
        fabricante = data.get('fabricante')
        problema = data.get('problema')
        mac = data.get('mac')

        if equipamento and fabricante and problema and mac and modelo:
            exists_in_registrado = EquipamentoRegistrado.objects.filter(mac=mac).exists()
            exists_in_em_teste = EquipamentoEmTeste.objects.filter(mac=mac).exists()
            exists_in_testado = EquipamentoTestado.objects.filter(mac=mac).exists()

            if exists_in_registrado or exists_in_em_teste or exists_in_testado:
                EquipamentoReteste.objects.create(
                    equipamento=equipamento, modelo=modelo, fabricante=fabricante, problema=problema, mac=mac, usuario=request.user
                )
                return JsonResponse({'success': 'Equipamento já existe. Registrado para Re-teste.'})
            else:
                EquipamentoRegistrado.objects.create(
                    equipamento=equipamento, modelo=modelo, fabricante=fabricante, problema=problema, mac=mac, usuario=request.user
                )
                return JsonResponse({'success': 'Equipamento cadastrado com sucesso!'})
        else:
            return JsonResponse({'error': 'Todos os campos são obrigatórios'}, status=400)
    return JsonResponse({'error': 'Método não permitido'}, status=405)

#Views Para Adicionar Viabilidade
@csrf_exempt
def AddViabilidade(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        vendedor = data.get('vendedor')
        projetista = data.get('projetista')
        descricaoVendedor = data.get('descricaoVendedor')
        descricaoProjetista = data.get('descricaoProjetista')
        status = data.get('viavel')

        if vendedor and projetista and descricaoVendedor and descricaoProjetista and status:
            CadastroViabilidade.objects.create(
                projeto_responsavel=projetista,
                comercial_responsavel=vendedor,
                descricao_projeto=descricaoProjetista,
                descricao_comercial=descricaoVendedor,
                status=status,
            )
            return JsonResponse({'success': 'Viabilidade cadastrada com sucesso!'}, status=201)
        else:
            return JsonResponse({'error': 'Preencha todos os campos.'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

#----------------------------------------------------------------------------------------------------------------------------------------------------------#
#Views Para Adicionar Técnicos
@csrf_exempt
def AddTecnico(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        projeto_responsavel = data.get('projeto_responsavel')
        tecnico_responsavel = data.get('tecnico_responsavel')
        assunto = data.get('Assunto')
        info_atendimento = data.get('info_atendimento')
        

        if projeto_responsavel and tecnico_responsavel and info_atendimento and assunto:
            CadastroTecnicos.objects.create(
                projeto_responsavel=projeto_responsavel,
                tecnico_responsavel=tecnico_responsavel,
                assunto=assunto,
                info_atendimento=info_atendimento,
                
            )
            return JsonResponse({'success': 'Viabilidade cadastrada com sucesso!'}, status=201)
        else:
            return JsonResponse({'error': 'Preencha todos os campos.'}, status=400)
    else:
        return JsonResponse({'error': 'Método não permitido.'}, status=405)

#----------------------------------------------------------------------------------------------------------------------------------------------------------#
#teste
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            error_message = "Usuário ou senha incorretos."
            return render(request, 'App/Login.html', {'error_message': error_message})
    else:
        return render(request, 'App/Login.html')
    

@login_required
def menu_view(request):
    registrados_count = EquipamentoRegistrado.objects.count()
    em_teste_count = EquipamentoEmTeste.objects.count()
    testados_count = EquipamentoTestado.objects.count()
    reteste_count = EquipamentoReteste.objects.count()
    emcampo_count = EquipamentoParaCampo.objects.count()
   

    labels = ['Equipamentos Cadastrados', 'Equipamentos em Teste', 'Equipamentos Testados', 'Equipamentos para Reteste', 'Equipamentos para Campo']
    data = [registrados_count, em_teste_count, testados_count, reteste_count, emcampo_count]

    context = {
        'registrados_count': registrados_count,
        'em_teste_count': em_teste_count,
        'testados_count': testados_count,
        'reteste_count': reteste_count,
        'emcampo_count': emcampo_count,
        'labels': labels,
        'data': data
    }

    return render(request,'App/Menu.html',context)

    

@login_required
def menu_projeto(request):
    viabilidades_count = CadastroViabilidade.objects.count()
    tecnicos_count = CadastroTecnicos.objects.count()
    labels = ['Viabilidades Cadastradas', 'Contagem dos Tecnicos']
    data = [viabilidades_count, tecnicos_count]
    context = {

        'viabilidades_count': viabilidades_count,
        'tecnicos_count': tecnicos_count,
        'labels': labels,
        'data': data

    }
    return render(request, 'ApPj/MenuProjeto.html', context)



@login_required
def registrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu_view')
        else:
            error_message = "Usuário ou Senha incorretos."
            return render(request, 'App/Login.html', {'error_message': error_message})
    else:
        return render(request, 'App/Login.html')

@login_required
def testado(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu_view')
        else:
            error_message = "Usuário ou Senha incorretos."
            return render(request, 'App/Login.html', {'error_message': error_message})
    else:
        return render(request, 'App/Login.html')
    

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    else:
        form = CustomUserCreationForm()
    return render(request, 'App/CadastrarEq.html', {'form': form})

def logout_view(request):
    return render(request, 'App/Login.html')



@login_required
def testado(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu_view')
        else:
            error_message = "Usuário ou Senha incorretos."
            return render(request, 'App/Login.html', {'error_message': error_message})
    else:
        return render(request, 'App/Login.html')


@login_required
def em_teste(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu_view')
        else:
            error_message = "Usuário ou Senha incorretos."
            return render(request, 'App/Login.html', {'error_message': error_message})
    else:
        return render(request, 'App/Login.html')
    

@login_required
def registrar(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('menu_view')
        else:
            error_message = "Usuário ou Senha incorretos."
            return render(request, 'App/login.html', {'error_message': error_message})
    else:
        return render(request, 'App/Login.html')
#----------------------------------------------------------------------------------------------------------------------------------------------------------#

@login_required
def teste(request):
    if request in index:
        return render('App/index')