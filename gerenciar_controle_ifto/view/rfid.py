from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_list_or_404
from gerenciar_controle_ifto.models import Rfid,CorRFID_Funcao
from gerenciar_controle_ifto.forms import EditarRfidForm
from datetime import datetime

def cadastrarRFID(request):
    
    cores = CorRFID_Funcao.objects.all()
    
    context = {
        'title' : 'Cadastro de Tag-Rfid',
        'cores' : cores,
        'nome_usuario_logado' : 'Rangerson'
    }

    if request.method == 'POST':
        tag_rfid_value = request.POST.get('tag_rfid_value')
        cod_corRfid = int(request.POST.get('cod_corRfid'))
        rfid_ativo = (request.POST.get('rfid_ativo') == "on")
        motivo_desativacao = request.POST.get('motivo_desativacao')
        data_desativacao = request.POST.get('data_desativacao')

        if rfid_ativo == False:
            if request.POST.get('data_desativacao') == None:
                return HttpResponse("Campo motivo_desativação deve ser preenchido para justificar a inativação da Tag")
        else:
            data_desativacao = None

        if tag_rfid_value == None:
            return HttpResponse("Campo Tag RFID não pode ser nulo")

        rfid = Rfid(tag_rfid_value=tag_rfid_value,
                    cod_corRFID_funcao=CorRFID_Funcao.objects.get(pk=cod_corRfid),
                    data_cadastro=datetime.now().strftime('%Y-%m-%d %H:%M'),
                    data_desativacao = data_desativacao,
                    vinculado = False,
                    ativo=rfid_ativo,
                    motivo_desativacao = motivo_desativacao
                    )

        rfid.save()
        return HttpResponseRedirect('/iftoAcess/listar/tagRfid/')
        
    return render(request, 'pages/rfid/cadastrarRfid.html',context)

def editarRFID(request, id):

    #corRfid_Funcao = []
    #tagRfid = get_list_or_404(Rfid, pk=id)
    #
    #tg = Rfid.objects.get(pk=id)
    #for corRfid in CorRFID_Funcao.objects.all():
    #    if corRfid.id != tg.cod_corRFID_funcao.id:
    #        corRfid_Funcao.append(corRfid)



    #if request.method == 'POST':
        #cod_corRfid = int(request.POST.get('cod_corRfid'))
        #rfid_ativo = (request.POST.get('rfid_ativo'))
        #motivo_desativacao = request.POST.get('motivo_desativacao')
        #data_desativacao = request.POST.get('data_desativacao')
        #
        #print(request.POST.get('rfid_ativo')+"\n")
        #print(rfid_ativo)

        #if rfid_ativo == False:
        #    if request.POST.get('data_desativacao') == None:
        #        return HttpResponse("Campo 'motivo_desativação' deve ser preenchido para justificar a inativação da Tag")
        #else:
        #    data_desativacao = None

    #    form = EditarRfid(request.POST, instance=tagRfid)
    #    if form.is_valid():
    #        form.save()
    #        return HttpResponseRedirect('/listarRfid')
    #    else:
    #        print(form.errors)
    #else:
    #    form = EditarRfid(instance=tagRfid)
    #    
    #context = {
    #    'title' : 'Edição de Tag Rfid',
    #    'tagRfid' : form,
    #    'corRfid_Funcao': corRfid_Funcao,
    #    'nome_usuario_logado' : 'Rangerson'
    #}
    
    if request.method == 'POST':
        form = EditarRfidForm(request.POST)
        
        if form.is_valid():
            print(form.cleaned_data)
            form = EditarRfidForm()
            
        context = {
            'form' : form
        }
        
        return render(request, 'pages/rfid/editarRfid.html', context)

    form = EditarRfidForm()
    
    context = {
        
        'form' : form,
        'title' : 'Edição de Tag-Rfid',
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/rfid/editarRfid.html', context)

def listarRFID(request):
    
    rfids = Rfid.objects.all()
    
    context = {
        'title' : 'Listagem de Tags-Rfid',
        'tagsRfid' : rfids,
        'nome_usuario_logado' : 'Rangerson'
    }
    
    return render(request, 'pages/rfid/listarRfid.html', context)