use controle_acesso_ifto;
select * from mysql.user;
SELECT * FROM mysql.user;
drop database controle_acesso_ifto;
create database controle_acesso_ifto;
show databases;
use controle_acesso_ifto;


insert into gerenciar_controle_ifto_papel_pessoa(descricao) VALUES("Aluno");
insert into gerenciar_controle_ifto_papel_pessoa(descricao) VALUES("Professor");
insert into gerenciar_controle_ifto_papel_pessoa(descricao) VALUES("Visitante");
select * from gerenciar_controle_ifto_papel_pessoa;


insert into gerenciar_controle_ifto_corRFID_funcao(corRFID, cod_cargo_id) VALUES("Vermelho",1);
insert into gerenciar_controle_ifto_corRFID_funcao(corRFID, cod_cargo_id) VALUES("Verde",2);
insert into gerenciar_controle_ifto_corRFID_funcao(corRFID, cod_cargo_id) VALUES("Cinza",3);
select * from gerenciar_controle_ifto_corRFID_funcao;


insert into gerenciar_controle_ifto_rfid(tag_rfid_value,data_cadastro, cod_corRFID_funcao_id, vinculado, ativo) VALUES("14 9B 9E 6F", now(),1,0,1);
insert into gerenciar_controle_ifto_rfid(tag_rfid_value,data_cadastro, cod_corRFID_funcao_id, vinculado, ativo) VALUES("4E 2 EC 6F", now(),1,0,1);
insert into gerenciar_controle_ifto_rfid(tag_rfid_value,data_cadastro, cod_corRFID_funcao_id, vinculado, ativo) VALUES("73 95 CC 13", now(),4,0,1);
insert into gerenciar_controle_ifto_rfid(tag_rfid_value,data_cadastro, cod_corRFID_funcao_id, vinculado, ativo) VALUES("C3 CD 5 2D", now(),2,0,1);
select * from gerenciar_controle_ifto_rfid;


insert into gerenciar_controle_ifto_pessoa(nome,sobrenome,cpf,idade,data_nascimento,vinculado,cod_Papel_pessoa_id,cod_Rfid_id) values("Lowane","Vieira","185.459.712-10",20,"2005-05-12",1,1,1);
insert into gerenciar_controle_ifto_pessoa(nome,sobrenome,cpf,idade,data_nascimento,vinculado,cod_Papel_pessoa_id,cod_Rfid_id) values("Tales","Oliveira","194.365.198-90",19,"2006-01-02",1,1,2);
insert into gerenciar_controle_ifto_pessoa(nome,sobrenome,cpf,idade,data_nascimento,vinculado,cod_Papel_pessoa_id,cod_Rfid_id) values("Israel","Clementino","194.674.281-30",30,"1994-05-30",1,2,5);
select P.nome,P.sobrenome,P.cpf,P.idade,P.data_nascimento,P.vinculado,P.cod_Papel_pessoa_id, Rfid.tag_rfid_value from gerenciar_controle_ifto_pessoa as P
inner join gerenciar_controle_ifto_rfid as Rfid ON P.cod_Rfid_id = Rfid.id;


select * from gerenciar_controle_ifto_historico_acesso_campus;

select hai.id, hai.data_acesso, Fc.descricao, P.nome,P.sobrenome, rfid.tag_rfid_value from gerenciar_controle_ifto_historico_acesso_campus as hai
inner join gerenciar_controle_ifto_rfid as rfid on hai.cod_rfid_id = rfid.id
inner join gerenciar_controle_ifto_papel_pessoa as Fc on hai.funcao_pessoa_id = Fc.id
inner join gerenciar_controle_ifto_pessoa as P on hai.cod_pessoa_id = P.id
order by hai.id;