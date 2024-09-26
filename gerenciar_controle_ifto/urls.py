from django.urls import path, include
from gerenciar_controle_ifto.view import home,pessoa,rfid,funcao, corRfid, usuario, historico_acesso_ifto

urlpatterns = [
    path('', home.home, name="homepage"),
    
    #PATH PARA CADASTROS
    path('cadastrar/tagRfid/', rfid.cadastrarRFID, name="cadastro_tagRfid"),
    path('cadastrar/pessoa/', pessoa.cadastrarPessoa, name="cadastro_pessoa"),
    path('cadastrar/funcao/',funcao.cadastrarFuncao, name="cadastro_funcao"),
    path('cadastrar/corRfid/', corRfid.cadastrarCorRfid, name="cadastro_corRfid"),
    path('cadastrar/usuario/', usuario.cadastrarUsuario, name="cadastro_usuario"),
    
    # PATH PARA EDICAO
    path('editar/TagRfid/<int:id>', rfid.editarRFID),
    
    #PATH PARA LISTAGEM
    path('listar/tagRfid/', rfid.listarRFID, name="visualizar_tagRfid"),
    path('listar/pessoa/',pessoa.listarPessoa, name="visualizar_pessoa"),
    path('listar/funcao/', funcao.listarFuncao, name="visualizar_funcao"),
    path('listar/corRfid/', corRfid.listarCorRfid, name="visualizar_corRfid"),
    path('listar/usuario/', usuario.listarUsuario, name="visualizar_usuario"),
    path('historico_acesso_ifto/',historico_acesso_ifto.listarHistoricoAcesso_Ifto, name="historico_acesso_ifto"),
]