create database rfid;
use rfid;

create table Pessoa(
	id INT PRIMARY KEY AUTO_INCREMENT,
    nome VARCHAR(20)
);

create table Papel_pessoa(
	id INT PRIMARY KEY AUTO_INCREMENT,
    papel_pessoa VARCHAR(15)
);

create table rfid(
	id INT PRIMARY KEY AUTO_INCREMENT,
    rfid_value VARCHAR(12)
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
SELECT * FROM Papel_pessoa;
SELECT * FROM rfid;

ALTER TABLE Papel_pessoa ADD COLUMN cod_rfid FOREIGN KEY  key();