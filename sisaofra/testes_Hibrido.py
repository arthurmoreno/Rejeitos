# -*- coding: latin-1 -*-

from copy import deepcopy
from multiprocessing.pool import ThreadPool
from os.path import join
import os.path
import sys
import cv2
import numpy as np
import time

import matplotlib.pyplot as plt
from sisaofra.constantes import fontes_iniciais
from sisaofra.hibrido_SA_AG.Hibrido import Hibrido
from sisaofra.modelo.Cromossomo import Cromossomo
from sisaofra.modelo.Fonte import Fonte
from sisaofra.mutacao.embaralhar import embaralhar
from sisaofra.mutacao.janela import janela
from sisaofra.selecao.extremo import extremo
from sisaofra.selecao.media import media
from sisaofra.selecao.roleta import roleta
from sisaofra.utils.Util import calcula_Scores
from sisaofra.utils.Util import log_resultado
from sisaofra.mutacao.centraliza import centraliza
from sisaofra.mutacao.trocaTemperatura import troca_temperatura
from sisaofra.mutacao.colocaFontes import colocaFontes


cromossomo = Cromossomo('0', fontes_iniciais())

def arquivar(f, n_evolucao, experimento, score_ini, melhores_evolucao, tempo):
    
    if not os.path.exists(join('dados', str(n_evolucao))):  # cria a pasta, se necessario
        os.makedirs(join('dados', str(n_evolucao)))
    
    txt = open(join('dados', str(n_evolucao), str(f) + '.txt'), mode='w')
    txt.write(experimento+'\n\n')
    for score in score_ini:
        txt.write(str(score[2])+'\t'+str(score[1])+'\n')
    txt.write('\nTempo de execucao:\t' + str(tempo)+'\n')
    txt.write('Melhor Cromossomo:\t' + str(extremo(deepcopy(melhores_evolucao), 1)[0].score[2])+'\t'+str(extremo(deepcopy(melhores_evolucao), 1)[0].score[1])+'\n\n')
    
    """
    #arquiva cada cromossomo do historico
    for cromossomo in melhores_evolucao:
        txt.write(str(cromossomo.score[2])+'\t'+str(cromossomo.score[1])+'\n')
        log_resultado(f, str(melhores_evolucao.index(cromossomo)), n_evolucao, experimento, cromossomo)
    """
        
    log_resultado(f, 'melhor_resultado', n_evolucao, experimento, extremo(deepcopy(melhores_evolucao), 1)[0])
    txt.close

def gerar_gafico(f, n_experimento, melhores_evolucao):
    pass
    plt.figure()  # nova figura
    plt.title('Experimento ' + str(n_experimento) + ' - ' + str(f))
    plt.ylabel('score')
    plt.xlabel('Evolução')
    plt.grid(True)
    
    scores = list(map(lambda x: x.score[2], melhores_evolucao))
    
    plt.plot(scores, linewidth=2.0)
    plt.savefig(join('dados', str(n_experimento), str(f) + '.png'))
    plt.close()
    
def __experimento(i, f, prob_ini, prob_fin, evoH, evoAG, nr, tp, mut, mutSA, sel, list_melhores_evolucao):
    ini = time.time()
    experimento = str(i) + '\t' + str(f) + '\t'+str(prob_ini) + '\t'+str(prob_fin) + '\t'+str(evoH) + '\t'+str(evoAG) + '\t'+str(nr) + '\t'+str(tp) + '\t'+str(mut) + '\t'+str(mutSA)
    print(experimento)
                                        
    hibrido = Hibrido()
    hibrido.set_Hibrido(experimento, cromossomo, tam_populacao=tp, prob_inicial=prob_ini, prob_final=prob_fin, evolucoesH=evoH, evolucoesAG=evoAG)
    score_ini = calcula_Scores(hibrido._populacao)
                                        
    if sel is extremo:
        hibrido.set_selecao(sel, int((10/100)*tp))
    else:
        hibrido.set_selecao(sel)
                                         
    if mut is janela:
        hibrido.set_mutacao(mut, 3, True)
    else:
        hibrido.set_mutacao(mut)
    
    if mutSA is janela:
        hibrido.set_mutacao_SA(mutSA, 3, True)
    else:
        hibrido.set_mutacao_SA(mutSA)
    
    melhores_evolucao = hibrido.evoluir()
                                            
    fim = time.time()
    arquivar(f+1, i, experimento, score_ini, melhores_evolucao, fim-ini)  # salvar em arquivo
    list_melhores_evolucao.append((f+1, i, melhores_evolucao))
    gerar_gafico(f+1, i, melhores_evolucao) #salvar o grafico
    del(melhores_evolucao)
    

# Configuracoes
prob_inicial = [0.9]
prob_final = [0.05]
evolucoesH = [100]
evolucoesAG = [50]
tamanho_populacao = [500]
nrs = [30]
selecao = [extremo]
mutacao = [troca_temperatura, embaralhar, janela]
mutacaoSA = [embaralhar, janela]
N = 30
num_experimentos = len(prob_inicial) * len(prob_final) * len(evolucoesH) * len(evolucoesAG) * len(tamanho_populacao) * len(nrs) * len(selecao) * len(mutacao) * len(mutacaoSA) * N
print(5*N)
paralelo = 'nao'

i = 1
pool = ThreadPool(processes=num_experimentos)#numero de experimentos
async_result = []
list_melhores_evolucao = []

cromossomo.funcao_avaliacao()
#print(cromossomo)

#cinco melhores configuracoes
for f in range(N):
    __experimento(1, f+1, 0.9, 0.05, 100, 50, 30, 500, troca_temperatura, embaralhar, extremo, list_melhores_evolucao)
for f in range(N):
    __experimento(2, f+1, 0.9, 0.05, 100, 50, 30, 500, colocaFontes, embaralhar, extremo, list_melhores_evolucao)
for f in range(N):
    __experimento(3, f+1, 0.9, 0.05, 100, 50, 30, 500, janela, embaralhar, extremo, list_melhores_evolucao)
for f in range(N):
    __experimento(4, f+1, 0.9, 0.05, 100, 20, 30, 500, colocaFontes, embaralhar, extremo, list_melhores_evolucao)
for f in range(N):
    __experimento(5, f+1, 0.9, 0.05, 100, 50, 30, 500, embaralhar, embaralhar, extremo, list_melhores_evolucao)

"""
for prob_ini in prob_inicial:
    for prob_fin in prob_final:
        for evoH in evolucoesH:
            for evoAG in evolucoesAG:
                for nr in nrs:
                    for tp in tamanho_populacao:
                        for sel in selecao:
                            for mut in mutacao:
                                for mutSA in mutacaoSA:
                                    for f in range(N):
                                        if i >= 1:#apenas roda a partir do experimento i
                                            if paralelo == 'sim':
                                                async_result.append(pool.apply_async(__experimento, (i, f, prob_ini, prob_fin, evoH, evoAG, nr, tp, mut, mutSA, list_melhores_evolucao)))
                                            else:
                                                __experimento(i, f, prob_ini, prob_fin, evoH, evoAG, nr, tp, mut, mutSA, list_melhores_evolucao)
                                            
                                    i += 1
"""
    
pool.close()
pool.join()
                                
print(len(list_melhores_evolucao))
for melhores_evolucao in list_melhores_evolucao:
    gerar_gafico(melhores_evolucao[0], melhores_evolucao[1], melhores_evolucao[2]) #salvar o grafico