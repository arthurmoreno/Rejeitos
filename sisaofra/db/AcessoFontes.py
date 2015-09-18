from psycopg2 import connect
from sisaofra.modelo.Fonte import Fonte
from sisaofra.modelo.Cromossomo import Cromossomo

"""
:mod:`AcessoDados` -- Acesso ao banco de dados
=====================================================================

Com este modulo e possivel acessar o bancos de
dados PostgreSQL atraves de metodos CRUD
"""

class AcessoFontes():
    """ Classe AcessoDadosPg - CRUD no banco de dados PostgreSQL
    
    Com a instancia desta classe e possivel dar inicio a uma sesao no banco de
    dados PostgreSQL, inserir dados pre-definidos de forma otimizada em uma
    tabela e consultar as taxas de dose armazenadas.
    """
    def __init__(self):
        self._conn = None
        self._cursor = None
    
    def iniciarSesao(self):
        self._conn = connect("host='localhost' dbname='postgres' user='postgres' password='123456' ")
        #self._conn = connect("host='localhost' dbname='sisaofra' user='sisaofra' password='senhanova' ")
        #self._conn = connect("host='localhost' dbname='sisaofra' user='postgres' password='123456' ")
        self._cursor = self._conn.cursor()
    
    def fecharSesao(self):
        self._cursor.close()
        self._conn.close()
        
    def limpaBanco(self):
        """Limpa o Banco de Dados no inicio do algoritmo"""
        self.iniciarSesao()
        self._cursor.execute("DELETE FROM fontes_cromossomos;")
        self._cursor.execute("DELETE FROM cromossomos;")
        self._cursor.execute("DELETE FROM fontes_historico;")
        self._cursor.execute("DELETE FROM historico;")
        self._conn.commit()
        self.fecharSesao()
        
    def povoamento(self, populacao, tam_populacao, tabela):
        """Povoa o banco de dados com a populacao inicial"""
        self.iniciarSesao()
        for cromossomo in populacao:
            self._cursor.execute("INSERT INTO " + tabela + " (id_cromossomo, score) VALUES (%s, %s);""",(str(cromossomo.id) , 0))
            for fonte in cromossomo.fontes:
                self._cursor.execute("INSERT INTO fontes_" + tabela + " (id_fonte, id_cromossomo, taxaDose, raio, X, Y) VALUES (%s, %s, %s, %s , %s , %s);""",(str(cromossomo.id) + str(fonte.identificador),
                                                                                                                                       str(cromossomo.id),
                                                                                                                                       fonte.taxa_dose,
                                                                                                                                       fonte.raio,
                                                                                                                                       fonte.x,
                                                                                                                                       fonte.y));
        self._conn.commit()
        self.fecharSesao()
        
    def get_fontes(self): #retorna objetos do tipo fonte do banco
        """Retorna uma lista com todas as fontes do banco"""
        self.iniciarSesao()
        self._cursor.execute("SELECT * FROM fonte;")
        
        fontes = []
        for linha in self._cursor.fetchall():
            fontes.append(Fonte(linha[1], linha[2], linha[3], linha[4]))
        self.fecharSesao()
        return fontes
    
    def save_cromossomo(self, cromossomo, tabela):
        """Salva o cromossomo no banco de dados"""
        self.iniciarSesao()
        self._cursor.execute("UPDATE " + tabela + " SET score = %s WHERE id_cromossomo = %s;",
                             (cromossomo.score[0],
                              str(cromossomo.id)))
        for fonte in cromossomo.fontes:
            self._cursor.execute("UPDATE fontes_" + tabela + " SET taxaDose = %s, raio = %s, X = %s, Y = %s WHERE id_fonte = %s;",
                                 (fonte.taxa_dose,
                                  fonte.raio,
                                  fonte.x,
                                  fonte.y,
                                  str(cromossomo.id) + str(fonte.identificador)))
        self._conn.commit()
        self.fecharSesao()

    def get_populacao(self, tabela):#converter a consula sql para uma unica
        """Retorna uma lista com a populacao do banco"""
        populacao = []
        #Realiza a query SQL
        self.iniciarSesao()
        self._cursor.execute("SELECT * FROM " + tabela + " a, fontes_" + tabela + " b WHERE a.id_cromossomo = b.id_cromossomo;")
        fontes_lin = self._cursor.fetchall()
        
        #Armazena os dados em populacao
        existe = False
        for linha_fonte in fontes_lin:
            for cromossomo in populacao:
                if linha_fonte[0] == cromossomo.id:
                    cromossomo.fontes.append(Fonte(linha_fonte[3], linha_fonte[4], linha_fonte[5], linha_fonte[6], linha_fonte[7]))
                    existe = True
                    break
                    
            if not existe:
                fontes = []
                fontes.append(Fonte(linha_fonte[3], linha_fonte[4], linha_fonte[5], linha_fonte[6], linha_fonte[7]))
                populacao.append(Cromossomo(linha_fonte[0],fontes))
            existe = False
        
        self.fecharSesao()
        return populacao