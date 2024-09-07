create database rfid;
use rfid;
create table rfid(
	id INT PRIMARY KEY AUTO_INCREMENT,
    rfid_value VARCHAR(12)
);

create table Pessoa(
	id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(20),
    cod_rfid INT,
    FOREIGN KEY (cod_rfid) REFERENCES rfid(id)
);

create table Papel_pessoa(
	id INT PRIMARY KEY AUTO_INCREMENT,
    papel_pessoa VARCHAR(15)
);


create table historico_acesso_campus(
	id INT PRIMARY KEY AUTO_INCREMENT,
    cod_rfid INT,
    cod_pessoa INT,
    funcao_pessoa INT,
    data_acesso DATETIME,
    FOREIGN KEY (cod_rfid)REFERENCES rfid(id),
    FOREIGN KEY (cod_pessoa) REFERENCES Pessoa(id),
    FOREIGN KEY (funcao_pessoa) REFERENCES Papel_pessoa(id)
);

SELECT * FROM Pessoa;
SELECT * FROM rfid;
SELECT * FROM Papel_pessoa;


INSERT INTO Pessoa(nome) VALUES ("Sandra Da  Silva");

ALTER TABLE Papel_pessoa MODIFY papel_pessoa VARCHAR(25);

SELECT P.id,P.nome, rfid.rfid_value FROM Pessoa AS P
INNER JOIN rfid ON P.cod_rfid = rfid.id
WHERE rfid_value = "1C 5A F6 7Y";