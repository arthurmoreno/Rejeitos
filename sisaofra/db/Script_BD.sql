--Script para criar o banco de dados

DROP TABLE populacao;
DROP TABLE fontes_cromossomos;
DROP TABLE cromossomos;
DROP TABLE fontes_historico;
DROP TABLE historico;

CREATE TABLE cromossomos (
     id_cromossomo varchar(8),
     score float,
     CONSTRAINT tb_cromossomo_pkey PRIMARY KEY (id_cromossomo)
     );
     
CREATE TABLE fontes_cromossomos (
     id_fonte varchar(8),
     id_cromossomo varchar(8) references cromossomos(id_cromossomo),
     taxaDose float,
     raio float,
     X int,
     Y int,
     CONSTRAINT tb_fonte_pkey PRIMARY KEY (id_fonte)
     );
     
CREATE TABLE historico (
     id_cromossomo varchar(8),
     score float,
     CONSTRAINT tb_historico_pkey PRIMARY KEY (id_cromossomo)
     ); 
     
CREATE TABLE fontes_historico (
     id_fonte varchar(8),
     id_cromossomo varchar(8) references historico(id_cromossomo),
     taxaDose float,
     X int,
     Y int,
     CONSTRAINT tb_fonte_h_pkey PRIMARY KEY (id_fonte)
     );
        
--CREATE TABLE populacao (
--     ID serial,
--     cromossomos cromossomo[]
--     );
