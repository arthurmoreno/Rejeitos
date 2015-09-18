-- Database generated with pgModeler (PostgreSQL Database Modeler).
-- pgModeler  version: 0.7.0
-- PostgreSQL version: 9.3
-- Project Site: pgmodeler.com.br
-- Model Author: EricK Simoes
-- Author Site: ericksimoes.com.br

SET check_function_bodies = false;

CREATE TABLE public.fonte(
	id serial,
	identificador varchar(20),
	taxa_dose real,
	x smallint,
	y smallint,
	CONSTRAINT id_fonte PRIMARY KEY (id)
);