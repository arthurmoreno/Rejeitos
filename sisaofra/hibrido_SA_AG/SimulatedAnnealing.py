"""
:mod:`SimulatedAnnealing` -- modulo que representa o algoritmo de SA
=====================================================================

Neste modulo -- Falta concluir
"""
import math
from copy import deepcopy
from random import Random
from sisaofra.db.AcessoFontes import AcessoFontes
from threading import Thread
from sisaofra.mutacao.embaralhar import embaralhar
from sisaofra.mutacao.trocaFontes import trocaFontes
from sisaofra.mutacao.janela import janela

class SimulatedAnnealing():
    """
    classdocs
    """

    def __init__(self, cromossomo, T, NR):
        """ Classe Fonte - Fonte radioativa do predio de rejeitos
            
        Exemplo:
            >>> fonte = Fonte('A', 2.3, 1, 1)
            >>> fonte.calculaTaxaDose(6)
    
        :param alfa: identificador da fonte
        :param NR: --falta fazer--
        :param populacao: guarda a populacao atual vista pelo SA
        :param T: Temperatura Maxima (inicial)
        :param TMin: Temperatura Minima (final)
        
        :attention: As posicoes x e y da fonte devem ser maiores que zero
        """
        Thread.__init__(self)
        self._NR = NR
        self._T = T
        self._cromossomo = cromossomo
        
    def set_mutacao(self, mutacao, *args):
        self._mutacao = mutacao
        
        if self._mutacao is janela:
            self._janela = args[0]
            self._randomizar_janela = args[1]
        
    def __save_cromossomo(self, cromossomo):
        banco = AcessoFontes()
        banco.save_cromossomo(cromossomo,"cromossomos")

    def run(self, cromossomo, T, NR):
        ran = Random()
        self._NR = NR
        self._T = T
        self._cromossomo = cromossomo
        for _ in range(self._NR):
            #Funcao de visinhanca - Mutacao
            if self._mutacao is embaralhar:
                self._cromossomo_2 = self._mutacao(deepcopy(self._cromossomo))
            elif self._mutacao is janela:
                popula = []
                popula.append(deepcopy(self._cromossomo))
                self._cromossomo_2 = self._mutacao(popula, self._janela, self._randomizar_janela, 1)[0]
            elif self._mutacao is trocaFontes:
                self._cromossomo_2 = trocaFontes(deepcopy(self._cromossomo))
            
            self._cromossomo_2.funcao_avaliacao()
            self._cromossomo.funcao_avaliacao()
            
            deltaE = self._cromossomo_2.score[0] - self._cromossomo.score[0]
            
            if deltaE <= 0:
                self._cromossomo = self._cromossomo_2
            else:
                if ran.random() < math.exp(-deltaE / self._T):
                    self._cromossomo = self._cromossomo_2
                
        #self.__save_cromossomo(self._cromossomo)
        return self._cromossomo