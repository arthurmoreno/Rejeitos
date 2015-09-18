--Script para povoar o banco de dados

SELECT * FROM fontes f WHERE f.id_cromossomo = '0';

--Atualizando cromossomo
UPDATE cromossomos SET score = 30 WHERE id_cromossomo = '0';

--Atualizando fonte
UPDATE fontes SET taxaDose = 15.7, X = 0, Y = 1 WHERE id_fonte = '00';


SELECT * FROM fontes f WHERE f.id_fonte = '00';