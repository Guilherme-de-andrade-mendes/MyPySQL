create database prmns;

use prmns;

create table usuario(
    codUsu int unique primary key not null,
    nome varchar(100) not null,
    estado varchar(7) not null,
    departamento varchar(20)
);

create table dispositivo(
    codDisp varchar(10) unique not null primary key,
	codUsu int,
    estado varchar(7) not null,
    alocacao varchar(15) not null,
    montagem varchar(20) not null,
    nota_fiscal varchar(30) not null,
    sistema_operacional varchar(50) not null,
    chave_ativacao varchar(29) not null unique,
    conexao_rede varchar(8) not null,
    data_atualizacao date,
    constraint pk_usuario foreign key (codUsu) references usuario(codUsu)
);

create table componente(
	codComp varchar(10) not null unique primary key,
    codDisp varchar(10),
    descricao varchar(50) not null,
    quantidade int not null,
    constraint pk_dispositivo foreign key (codDisp) references dispositivo(codDisp)
);

create table placaMae(
	codComp varchar(10),
    tipagem varchar(4) not null,
    slot_ram int not null,
    constraint pk_componente foreign key (codComp) references componente(codComp)
);

create table memoria(
	codComp varchar(10),
    capacidade varchar(5) not null,
    tipagem varchar(4) not null,
    voltagem varchar(6) not null,
    constraint pk_comp_memoria foreign key (codComp) references componente(codComp)
);

create table processador(
	codComp varchar(10),
    velocidade varchar(6) not null,
    constraint pk_comp_processador foreign key (codComp) references componente(codComp)
);

create table armazenamento(
	codComp varchar(10),
    espaco int not null,
    constraint pk_comp_armazenamento foreign key (codComp) references componente(codComp)
);

create table fonte(
	codComp varchar(10),
    watts varchar(10) not null,
    constraint pk_comp_fonte foreign key (codComp) references componente(codComp)
);

create table placaGrafica(
	codComp varchar(10),
    marca varchar(20) not null,
    entrada varchar(10) not null,
    ram varchar(5) not null,
    constraint pk_comp_pgrafica foreign key (codComp) references componente(codComp)
);