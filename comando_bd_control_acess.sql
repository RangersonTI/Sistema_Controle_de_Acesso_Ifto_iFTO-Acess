use controle_acesso_ifto;
select * from mysql.user;
SELECT * FROM mysql.user;
drop database controle_acesso_ifto;
create database controle_acesso_ifto;
show databases;
use controle_acesso_ifto;


select * from gerenciar_controle_ifto_papel_pessoa;
insert into gerenciar_controle_ifto_papel_pessoa(descricao) VALUES("Aluno");

select * from gerenciar_controle_ifto_corRFID_funcao;
insert into gerenciar_controle_ifto_corRFID_funcao(corRFID, cod_cargo_id) VALUES("Vermelho",1);

select * from gerenciar_controle_ifto_rfid;
insert into gerenciar_controle_ifto_rfid(tag_rfid_value,data_cadastro, cod_corRFID_funcao_id, vinculado, ativo) VALUES("14 9B 9E 6F", now(),1,0,1);
insert into gerenciar_controle_ifto_rfid(tag_rfid_value,data_cadastro, cod_corRFID_funcao_id, vinculado, ativo) VALUES("4E 2 EC 6F", now(),1,0,1);


select * from gerenciar_controle_ifto_pessoa;
insert into gerenciar_controle_ifto_pessoa(nome,sobrenome,cpf,idade,data_nascimento,vinculado,cod_Papel_pessoa_id,cod_Rfid_id)
values("Lowane","Vieira","185.459.712-10",20,"2005-05-12",1,1,1);

select * from gerenciar_controle_ifto_historico_acesso_campus;