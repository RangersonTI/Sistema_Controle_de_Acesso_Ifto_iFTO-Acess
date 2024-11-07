from django.urls import path, include
from gerenciar_controle_ifto.view import home,pessoa,rfid,funcao, corRfid, usuario, historico_acesso_ifto, pessoa_rfid, login

urlpatterns = [
    path('', home.home, name="homepage"),
    
    #PATH PARA CADASTROS
    path('cadastrar/tagRfid/', rfid.cadastrarRFID, name="cadastro_tagRfid"),
    path('cadastrar/pessoa/', pessoa.cadastrarPessoa, name="cadastro_pessoa"),
    path('cadastrar/funcao/',funcao.cadastrarFuncao, name="cadastro_funcao"),
    path('cadastrar/corRfid/', corRfid.cadastrarCorRfid, name="cadastro_corRfid"),
    path('cadastrar/usuario/', usuario.cadastrarUsuario, name="cadastro_usuario"),
    
    # PATH PARA EDICAO
    path('editar/tagRfid/<int:id>', rfid.editarRFID, name="editar_tagRfid"),
    path('editar/pessoa/<int:id>', pessoa.editarPessoa, name="editar_Pessoa"),
    path('editar/funcao/<int:id>', funcao.editarFuncao, name="editar_Funcao"),
    path('editar/corRfid/<int:id>', corRfid.editarCorRfid, name="editar_corRfid"),
    path('editar/usuario/<int:id>', usuario.editarUsuario, name="editar_usuario"),
    
    #PATH PARA LISTAGEM
    path('listar/tagRfid/', rfid.listarRFID, name="visualizar_tagRfid"),
    path('listar/pessoa/',pessoa.listarPessoa, name="visualizar_pessoa"),
    path('listar/funcao/', funcao.listarFuncao, name="visualizar_funcao"),
    path('listar/corRfid/', corRfid.listarCorRfid, name="visualizar_corRfid"),
    path('listar/usuario/', usuario.listarUsuario, name="visualizar_usuario"),
    path('historico_acesso_ifto/',historico_acesso_ifto.listarHistoricoAcesso_Ifto, name="historico_acesso_ifto"),
    path('vincular_rfid/<int:id>', pessoa_rfid.vincularRfid, name="vincular_rfid_pessoa"),
    path('desvincular_rfid/<int:id>', pessoa_rfid.desvincularRfid, name="desvincular_rfid_pessoa"),
    
    #PATH DE LOGIN
    path('login/', login.login, name="login"),
    
]