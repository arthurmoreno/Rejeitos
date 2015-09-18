from copy import deepcopy
from sisaofra.selecao.media import media
from sisaofra.selecao.roleta import roleta
from sisaofra.selecao.extremo import extremo
from sisaofra.mutacao.embaralhar import embaralhar
from sisaofra.mutacao.janela import janela
from sisaofra.mutacao.trocaFontes import trocaFontes
from sisaofra.mutacao.randomPosition import randomPosition
from sisaofra.mutacao.colocaFontes import colocaFontes
from sisaofra.mutacao.centraliza import centraliza
from sisaofra.mutacao.trocaTemperatura import troca_temperatura

class Evolucao:
    
    def __init__(self):
        self._populcacao = []
        self._cromossomo = None
        self._tam_populacao = None
        self._condicao_parada = None
        self._iteracoes = 0
        self._selecao = None
        self._mutacao = None
    
    def set_evolucao(self, cromossomo, tam_populacao, condicao_parada):
        self._tam_populacao = tam_populacao
        self._condicao_parada = condicao_parada
        
        # nova populacao (genoma)
        self._populcacao.append(cromossomo)
        for _ in range((tam_populacao * 4) - 1):
            cromossomo_mutado = embaralhar(deepcopy(cromossomo))
            cromossomo_mutado.funcao_avaliacao()
            self._populcacao.append(cromossomo_mutado)
        self._populcacao = extremo(self._populcacao, tam_populacao, max)
    
    def set_selecao(self, selecao, *args):
        self._selecao = selecao

        if self._selecao is extremo:
            self._n_melhores = args[0]
    
    def set_mutacao(self, mutacao, *args):
        self._mutacao = mutacao
        
        if self._mutacao is janela:
            self._janela = args[0]
            self._randomizar_janela = args[1]
    
    def __condicao_parada(self):  # True se a condicao for atendida
        if isinstance(self._condicao_parada, int):
            self._iteracoes += 1
            if self._iteracoes > self._condicao_parada:
                return True
            else:
                return False
            
    def evoluir(self):
        self.a = 0
        # execultar o calculo de aptidao / func avaliacao
        for cromossomo in self._populcacao:
            cromossomo.funcao_avaliacao()  # atualiza o score do cromossomo
        
        historico_populacao = []  # melhor populacao em cada evolucao
        while not self.__condicao_parada():
            #print('evol\t' + str(self.a))
            self.a = self.a+1
            # selecao #
            if self._selecao is extremo:
                nova_populacao = self._selecao(deepcopy(self._populcacao), self._n_melhores)
            elif self._selecao is media:
                nova_populacao = self._selecao(deepcopy(self._populcacao))
            elif self._selecao is roleta:
                nova_populacao = self._selecao(deepcopy(self._populcacao))
            
            # mutacao #
            n_elementos_mutados = self._tam_populacao - len(nova_populacao)
            if self._mutacao is embaralhar:
                nova_populacao.extend(self._mutacao(deepcopy(nova_populacao), n_elementos_mutados))
            elif self._mutacao is janela:
                nova_populacao.extend(self._mutacao(deepcopy(nova_populacao), self._janela, self._randomizar_janela, n_elementos_mutados))
            elif self._mutacao is randomPosition:
                nova_populacao.extend(self._mutacao(deepcopy(nova_populacao), n_elementos_mutados))
            elif self._mutacao is trocaFontes:
                nova_populacao.extend(self._mutacao(deepcopy(nova_populacao), n_elementos_mutados))
            elif self._mutacao is centraliza:
                nova_populacao.extend(self._mutacao(deepcopy(nova_populacao), n_elementos_mutados))
            elif self._mutacao is colocaFontes:
                nova_populacao.extend(self._mutacao(deepcopy(nova_populacao), n_elementos_mutados))
            """  a temperatura não funciona no AG
            elif self._mutacao is troca_temperatura:
                nova_populacao.extend(self._mutacao(deepcopy(nova_populacao), self._T, n_elementos_mutados))
            """
            
            self._populcacao = deepcopy(nova_populacao)
            
            # execultar o calculo de aptidao / func avaliacao #
            for cromossomo in self._populcacao:
                cromossomo.funcao_avaliacao()  # atualiza o score do cromossomo
            
            historico_populacao.append(extremo(self._populcacao, 1)[0])  # vetor com o melhor de cada populacao
        
        return historico_populacao
