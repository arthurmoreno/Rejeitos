# -*- coding: latin-1 -*-

from copy import deepcopy
from os.path import join
from os.path import os
import time

import matplotlib.pyplot as plt
from sisaofra.constantes import fontes_iniciais
from sisaofra.modelo.Cromossomo import Cromossomo
from sisaofra.modelo.Fonte import Fonte
from sisaofra.mutacao.colocaFontes import colocaFontes
from sisaofra.mutacao.embaralhar import embaralhar
from sisaofra.mutacao.janela import janela
from sisaofra.mutacao.trocaFontes import trocaFontes
from sisaofra.mutacao.trocaTemperatura import troca_temperatura
from sisaofra.regranegocio.Evolucao import Evolucao
from sisaofra.selecao.extremo import extremo
from sisaofra.selecao.media import media
from sisaofra.selecao.roleta import roleta
from sisaofra.utils.Util import calcula_Scores
from sisaofra.utils.Util import log_resultado


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
    for cromossomo in melhores_evolucao:
        txt.write(str(cromossomo.score[2])+'\t'+str(cromossomo.score[1])+'\n')
        log_resultado(f, str(melhores_evolucao.index(cromossomo)), n_evolucao, experimento, cromossomo)
    """
    log_resultado(f, 'melhor_resultado', n_evolucao, experimento, extremo(deepcopy(melhores_evolucao), 1)[0])
    txt.close

def gerar_gafico(f, n_evolucao, melhores_evolucao):
    
    plt.figure()  # nova figura
    plt.title('Experimento ' + str(n_evolucao) + ' - ' + str(f))
    plt.ylabel('score')
    plt.xlabel('Evolução')
    plt.grid(True)
    
    scores = []
    for cromossomo in melhores_evolucao:
        scores.append(cromossomo.score)
    
    plt.plot(scores, linewidth=2.0)
    plt.savefig(join('dados', str(n_evolucao), str(f) + '.png'))
    plt.close()
    
def __experimento(i, f, tp, ev, sel, mut):
    ini = time.time()
    experimento = str(i) + '\t' + str(f) + '\t'+str(tp) + '\t'+str(ev) + '\t'+sel.__name__ + '\t'+mut.__name__
    print(experimento)
                    
    evolucao = Evolucao()
    evolucao.set_evolucao(cromossomo, tam_populacao=tp, condicao_parada=ev)
    score_ini = calcula_Scores(evolucao._populcacao)
                    
    if sel is extremo:
        evolucao.set_selecao(sel, int((10/100)*tp))
    else:
        evolucao.set_selecao(sel)
    
    if mut is janela:
        evolucao.set_mutacao(mut, 3, True)
    else:
        evolucao.set_mutacao(mut)
    
    melhores_evolucao = evolucao.evoluir()
    
    fim = time.time()
    arquivar(f+1, i, experimento, score_ini, melhores_evolucao, fim-ini)  # salvar em arquivo
    gerar_gafico(f+1, i, melhores_evolucao) # salvar o grafico
    del(melhores_evolucao)
    
        
# Configuracoes
tamanho_populacao = [50, 100]
evolucoes = [100, 200]
selecao = [extremo]
mutacao = [embaralhar, colocaFontes, janela]
N = 30

i = 1

#cinco melhores configuracoes

for f in range(N):
    __experimento(1, f, 500, 200, extremo, embaralhar)
for f in range(N):
    __experimento(2, f, 500, 200, extremo, janela) 
for f in range(N):
    __experimento(3, f, 500, 200, extremo, colocaFontes)
for f in range(N):
    __experimento(4, f, 500, 100, extremo, embaralhar)
for f in range(N):
    __experimento(5, f, 500, 200, extremo, janela)

"""
for tp in tamanho_populacao:
    for ev in evolucoes:
        for sel in selecao:
            for mut in mutacao:
                for f in range(N):
                    ini = time.time()
                    experimento = str(i) + '\t'+str(tp) + '\t'+str(ev) + '\t'+sel.__name__ + '\t'+mut.__name__
                    print(experimento)
                    
                    evolucao = Evolucao()
                    evolucao.set_evolucao(cromossomo, tam_populacao=tp, condicao_parada=ev)
                    score_ini = calcula_Scores(evolucao._populcacao)
                    
                    if sel is extremo:
                        evolucao.set_selecao(sel, int((10/100)*tp))
                    else:
                        evolucao.set_selecao(sel)
                    
                    if mut is janela:
                        evolucao.set_mutacao(mut, 3, True)
                    else:
                        evolucao.set_mutacao(mut)
                    
                    melhores_evolucao = evolucao.evoluir()
                    
                    fim = time.time()
                    arquivar(f+1, i, experimento, score_ini, melhores_evolucao, fim-ini)  # salvar em arquivo
                    gerar_gafico(f+1, i, melhores_evolucao) # salvar o grafico
                    del(melhores_evolucao)
                i += 1
"""