"""
Created on 03/02/2015

@author: Arthur
"""
from copy import deepcopy
from random import Random
import math
from multiprocessing.pool import Pool

from sisaofra.selecao.extremo import extremo
from sisaofra.selecao.media import media
from sisaofra.selecao.roleta import roleta

from sisaofra.utils.Util import gera_alfa, gera_TMax_TMin, log_resultado, desenha_cromossomo, gera_populacao_inicial

from sisaofra.mutacao.embaralhar import embaralhar
from sisaofra.mutacao.janela import janela
from sisaofra.mutacao.trocaFontes import trocaFontes
from sisaofra.mutacao.randomPosition import randomPosition
from sisaofra.mutacao.colocaFontes import colocaFontes
from sisaofra.mutacao.centraliza import centraliza
from sisaofra.mutacao.trocaTemperatura import troca_temperatura

#funcao exponecial otimizada - utilizada no simulated annealing
def __exp(self, y):
    return 1513096 * y + (1072693248 - 90.253)

#funcao SA
def simulated_annealing(cromossomo, NR, T, mutacao_SA, *args):
    #configuração da mutação
    _mutacao_SA = mutacao_SA
    #print(args)
    if _mutacao_SA is janela:
        _janela = args[0][0]
        _randomizar_janela = args[0][1]
            
    ran = Random()
    _NR = NR
    _T = T
    cromossomo_sa = cromossomo
    cromossomo_sa_2 = None
    for _ in range(_NR):
        #Funcao de visinhanca - Mutacao
        if _mutacao_SA is embaralhar:
            cromossomo_sa_2 = _mutacao_SA(deepcopy(cromossomo_sa))
        elif _mutacao_SA is randomPosition:
            cromossomo_sa_2 = _mutacao_SA(deepcopy(cromossomo_sa))
        elif _mutacao_SA is centraliza:
            cromossomo_sa_2 = _mutacao_SA(deepcopy(cromossomo_sa))
        elif _mutacao_SA is troca_temperatura:
            cromossomo_sa_2 = _mutacao_SA(deepcopy(cromossomo_sa), _T)
        elif _mutacao_SA is colocaFontes:
            cromossomo_sa_2 = _mutacao_SA(deepcopy(cromossomo_sa))
        elif _mutacao_SA is janela:
            popula = []
            popula.append(deepcopy(cromossomo_sa))
            nova_populacao = []
            nova_populacao.extend(_mutacao_SA(popula, _janela, _randomizar_janela, 1)[0])
            nova_populacao.extend(_mutacao_SA(popula, _janela, _randomizar_janela+1, 1)[0])
            nova_populacao.extend(_mutacao_SA(popula, _janela, _randomizar_janela+2, 1)[0])
            nova_populacao.extend(_mutacao_SA(popula, _janela, _randomizar_janela+3, 1)[0])
            cromossomo_sa_2 = extremo(deepcopy(popula), 1)[0]
            
        #calculo do delta
        cromossomo_sa_2.funcao_avaliacao()
        cromossomo_sa.funcao_avaliacao()
        deltaE = cromossomo_sa_2.score[0] - cromossomo_sa.score[0]
            
        #decisão de escolha - probabilidade em funcao da temperatura
        #print('probabilidade de escolha SA: '+str(math.exp(-deltaE / T)))
        if deltaE <= 0 or (cromossomo_sa.score[1] == 1 and cromossomo_sa_2.score[1] == 0):
            cromossomo_sa = cromossomo_sa_2
        else:
            #if ran.random() < (1513096 * (-deltaE / _T) + (1072693248 - 90.253)):77


            if ran.random() < math.exp(-deltaE / _T):
                cromossomo_sa = cromossomo_sa_2
                
    return cromossomo_sa

class Hibrido:
    """
    Esta classe representa o algoritmo Hibrido - AG e SA
    
    :param experimento: String que representa os parametros do experimento
    :param cromossomo: Cromossomo base que ira gerar a populacao inicial
    :param tam_populacao: Tamanho da populacao inicial desejada
    :param prob_inicial: Probabilidade inicial de selecao do Simulated Annealing
    :param prob_final: Probabilidade final de selecao do Simulated Annealing
    :param evolucoes: Numerotam_populacao de evolucoes desejadas para o Algoritmo Genetico
    
    Obs: na classe esta presente apenas o algoritmo genetico.
    O algoritmo do simulated annealing esta em uma metodo externo a classe
    """

    def __init__(self):
        self._experimento = None
        self._populacao = []
        self._cromossomo = None
        self._selecao = None
        self._mutacao = None
        self._mutacao_SA = None
        self._argumentos = None
        self._tam_populacao = 0
        self._T = 0
        self._T_Min = 0
        self._alfa = 0
        self._NR = 0
        
    # Metodo que define os parametros iniciais do algoritmo Hibrido
    def set_Hibrido(self, experimento, cromossomo, tam_populacao, prob_inicial, prob_final, evolucoesH, evolucoesAG):
        self._cromossomo = cromossomo
        self._cromossomo_inicial = cromossomo
        self._tam_populacao = tam_populacao
        self._experimento = experimento
        self._evolucoesAG = evolucoesAG
        
        """
        # Nova populacao (genoma)
        self._populacao.append(cromossomo)
        for _ in range((tam_populacao * 4) - 1):
            cromossomo_mutado = embaralhar(deepcopy(cromossomo))
            cromossomo_mutado.funcao_avaliacao()
            self._populacao.append(cromossomo_mutado)
        
        # Seleciona os piores individuos
        self._populacao = extremo(self._populacao, tam_populacao, max)
        """
        
        #print("tamanho da populacao inicial: "+ str(self._tam_populacao))
        self._populacao = gera_populacao_inicial(self._cromossomo, self._tam_populacao)
        i = 0
        for cromossomo in self._populacao:
            cromossomo.id = str(i)
            i += 1
            
        # Configuracoes sugeridas
        temperaturas = gera_TMax_TMin(self._populacao, prob_inicial, prob_final)
        self._T = temperaturas[0]
        self._T_Min = temperaturas[1]
        self._alfa = gera_alfa(self._T_Min, self._T, epocas=evolucoesH)
        self._NR = 50 #len(self._populacao)
        """prints de controle
        print("Temperatura inicial sugerida: " + str(self._T))
        print("Temperatura final sugerida: " + str(self._T_Min))
        print("Alfa sugerido: " + str(self._alfa))
        """
        
    # Define a funcao de selecao do algoritmo genetico
    def set_selecao(self, selecao, *args):
        self._selecao = selecao

        if self._selecao is extremo:
            self._n_melhores = args[0]
    
    # Define a funcao de mutacao do algoritmo genetico
    def set_mutacao(self, mutacao, *args):
        self._mutacao = mutacao
        
        if self._mutacao is janela:
            self._janela = args[0]
            self._randomizar_janela = args[1]
    
    # Define a funcao de mutacao do Simulated Annealing
    def set_mutacao_SA(self, mutacao, *args):
        self._mutacao_SA = mutacao
        
        if self._mutacao_SA is janela:
            self._argumentos = args
    
    # Verifica a condicao de parada
    def __condicao_parada(self, melhor_cromossomo):  # True se a condicao for atendida
        melhora = ((self._cromossomo_inicial.score[2] - melhor_cromossomo.score[2]) / self._cromossomo_inicial.score[2])
        #print('melhora - ' + str(melhora) + '         score - ' + str(melhor_cromossomo.score[2]))
        return (self._T >= self._T_Min) and not(melhora > 0.15 and melhor_cromossomo.score[1] == 0)
    
    # Realiza as evolucoes do algoritmo genetico
    def evoluir(self):
        self.a = 0
        global result_list
        
        historico_populacao = [] # melhor populacao em cada evolucao
        historico_populacao.append(self._cromossomo_inicial)
        melhor_cromossomo = self._cromossomo_inicial
        while self.__condicao_parada(extremo(deepcopy(historico_populacao), 1)[0]):
            #print('evol\t' + str(self.a) + ' - ' + self._experimento)
            self.a = self.a+1
            
            """prints de controle
            print("evolucao - " + str(self.a) + '       temperatura - ' + str(self._T))
            
            # Debug print ---- Remover apos corrigir os erros
            print("Inicio do AG e antes do SA - \n")
            print(self._populacao)
            print("\n\n")
            """

            #--------   Simulated Annealing  ---------------#
            
            pool = Pool()
            results = []
            i = 0
            #Dispara as N threads de SA (onde N e o tamanho da populacao)
            for cromossomo in self._populacao:
                results.append(pool.apply_async(func = simulated_annealing, args = (cromossomo, self._NR, self._T, self._mutacao_SA, self._argumentos)))
                i += 1
            pool.close()
            pool.join()
            
            self._populacao = list(map(lambda x, y: x.get(timeout = y), results, range(self._tam_populacao)))
            
            """
            # Debug print ---- Remover apos corrigir os erros
            print("Depois do SA - \n")
            print(self._populacao)
            print("\n\n")
            """
            
            #--------  Algoritmo genetico  -----------------#
            for _ in range(self._evolucoesAG):
                # execultar o calculo de aptidao / func avaliacao #
                for cromossomo in self._populacao:
                    cromossomo.funcao_avaliacao()  # atualiza o score do cromossomo
                
                # selecao #
                if self._selecao is extremo:
                    nova_populacao = self._selecao(deepcopy(self._populacao), self._n_melhores)
                elif self._selecao is media:
                    nova_populacao = self._selecao(deepcopy(self._populacao))
                elif self._selecao is roleta:
                    nova_populacao = self._selecao(deepcopy(self._populacao))
                
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
                elif self._mutacao is troca_temperatura:
                    nova_populacao.extend(self._mutacao(deepcopy(nova_populacao), self._T, n_elementos_mutados))
                elif self._mutacao is colocaFontes:
                    nova_populacao.extend(self._mutacao(deepcopy(nova_populacao), n_elementos_mutados))
                    
                self._populacao = deepcopy(nova_populacao)
            
            """
            # Debug print ---- Remover apos corrigir os erros
            print("Final do AG - \n")
            print(self._populacao)
            print("\n\n")
            """
            #print(extremo(deepcopy(self._populacao), 1))
            melhor_cromossomo = extremo(deepcopy(self._populacao), 1)[0]
            historico_populacao.append(melhor_cromossomo)  # vetor com o melhor de cada populacao
            
            self._T = self._T * self._alfa
            
            if self.a % 5 == 0:
                desenha_cromossomo("evolucao_" + str(self.a),melhor_cromossomo)
        
        melhor_solucao = extremo(deepcopy(historico_populacao), 1)
        if melhor_solucao[0].score[1] == 1:
            print("Nenhuma solucao viavel encontrada")
        else:
            print("Melhor solucao:")
            print(melhor_solucao)
            #desenha_cromossomo("melhor solucao",melhor_solucao[0])
        return historico_populacao