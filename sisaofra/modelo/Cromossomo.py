"""
:mod:`Cromossomo` -- classe que representa um cromossomo com uma lista de fontes
=====================================================================

Neste modulo esta implementado uma lista com a representacao de todas as fontes
distribuidas numa gaiola presente em um predio de rejeitos radioativos.
"""
#from sisaofra.__main__ import fontes
from math import sqrt
from random import shuffle
from sisaofra.constantes import receptores

class Cromossomo(object):
    
    def __init__(self, identificador, fontes):
        """ Classe Cromossomo - Conjunto de fontes
        O inicializador da representacao cromossomica, pode receber
        uma quantidade indefinidas de fontes
        
        Exemplo:
            >>> fonte1 = Fonte(2.3, 1, 1, 'A')
            >>> fonte2 = Fonte(2.1, 2, 1, 'B')
            >>> fonte3 = Fonte(0.2, 3, 1, 'C')
            >>> cromossomo = Cromossomo('01', fonte1, fonte2, fonte3)
            
            >>> fr = Util.criaFontesRandomicas()
            >>> cromossomo02 = Cromossomo('02', fr[0], fr[1], fr[2], fr[3], fr[4], fr[5], fr[6], fr[7], fr[8])
            
            >>> cromossomo03 = Cromossomo('03', Util.criaFontesRandomicas())

        :param identificador: identificador do cromossomo
        :param fontes: 'list' com objetos do tipo Fonte
        """
        self.id = identificador
        self.fontes = fontes
        self.score = [0, 0, 0]
        self.receptores = receptores()
    
    def __repr__(self):
        """Retorna uma  string com a representacao do cromossomo"""
        _ret = "- Cromossomo:\t%s\n" % (self.id)
        _ret += "\tScore:\t%s" % (self.score[2])+" - %s\n"%(self.score[1])
        for fonte in self.fontes:
            _ret += '\t|' + fonte.identificador
        _ret += '\n'
        for fonte in self.fontes:
            _ret += '\t|' + str(fonte.taxa_dose)
        _ret += '\n'
        for fonte in self.fontes:
            _ret += '\t|' + str(round(fonte.x,2)) + 'x' + str(round(fonte.y))
        return _ret + '\n'
    
    def __len__(self):
        return len(self.fontes)
    
    def __iter__(self):
        for i in self.fontes:
            yield i
    
    def __eq__(self, outro_cromossomo):
        """ Sobrescreve o metodo equals do Python. Dois cromossomos sao tidos
        como iguais quando suas fontes sao iquais.
        
        :param outro_cromossomo: 'Cromossomo' a ser comparado
        
        :rtype: 'bool'
        """
        for fonte_s in self.fontes:
            for fonte_o in outro_cromossomo:
                if not fonte_s == fonte_o:
                    return False
        return True
    
    def __embaralhar_cromossomo(self):
        vetor_posicoes = []
        for fonte in self.fontes:
            vetor_posicoes.append([fonte.x, fonte.y])
        
        shuffle(vetor_posicoes)
        
        i = 0
        for fonte in self.fontes:
            fonte.x = vetor_posicoes[i][0]
            fonte.y = vetor_posicoes[i][1]
            i += 1
    
    def funcao_avaliacao(self):
        """ Funcao de Avaliacao
        
        Este metodo atribui o valor do score do cromossomo como
        a soma das taxas de dose de cada uma de suas fontes.
        
        FIXME: lembrar de trocar esses dois 'for' por um vetor
        """
        # calculo de colisao #
        self.score[1] = 0
        parar = False
        colisao = False
        for fonteA in self.fontes:
            for fonteB in self.fontes:
                if fonteA != fonteB:
                    #distancia = sqrt(pow((fonteA.x - fonteB.x), 2) + pow((fonteA.y - fonteB.y), 2))
                    distancia = sqrt((fonteA.x - fonteB.x)*(fonteA.x - fonteB.x) + (fonteA.y - fonteB.y)*(fonteA.y - fonteB.y))
                    somaRaios = (fonteA.raio + fonteB.raio)
                    #print("distancia = " + str(distancia) + "; Soma dos raios = " + str(somaRaios))
                    if distancia < somaRaios:
                        self.score[1] = 1
                        parar = True
                        break
                    else:
                        colisao = False
            if parar:
                break
        # calculo do score #
        if colisao == False:
            score_receptor = 0
            score_receptores = []
            for pm_receptor in self.receptores:
                for fonte in self.fontes:
                    score_receptor += fonte.calcula_taxa_dose(pm_receptor[0], pm_receptor[1])
                score_receptores.append(score_receptor)
                score_receptor = 0
            self.score[2] = max(score_receptores)
            self.score[0] = self.score[2]*pow(10,self.score[1])
