import math

import cv2
import os.path
import numpy as np
from sisaofra.db.AcessoFontes import AcessoFontes
from sisaofra.modelo.Cromossomo import Cromossomo
from os.path import join
from copy import deepcopy
from sisaofra.mutacao.embaralhar import embaralhar
from sisaofra.selecao.extremo import extremo

""" funcao obsoleta - codigo nao utiliza mais banco de dados
def gera_cromossomo_banco():
    acesso_fontes = AcessoFontes()
    return Cromossomo('00', acesso_fontes.get_fontes())
"""

def calcula_Scores(populacao):
    scores = []
    for cromossomo in populacao:
        scores.append(cromossomo.score)
    return scores

def calcula_Media(quant_experimentos, N):
    """
    Funcao que calcula a Media das populacoes iniciais
    e as coloca em um arquivo .txt em formato proprio para excel
    """
    print("Calculando a media da populacao inicial...")
    mediaPop = open(join('dados', 'mediaPopulacao.txt'), mode='w')
    for n_experimentos in range(1, quant_experimentos + 1):
        for f in range(1, N + 1):
            txt = open(join('dados', str(n_experimentos), str(f) + '.txt'), mode='r')
            contar = False
            somatorio = 0
            i = 0
            for linha in txt:
                if linha == "\n" and contar == False:
                    contar = True
                elif linha == "\n" and contar == True:
                    break
                elif contar == True:
                    i += 1
                    somatorio += float(linha.strip('01'+'\t'+'\n'))
            media = somatorio / i
            mediaPop.write(str(media)+'\t')
            txt.close()
        mediaPop.write('\n')
    mediaPop.close()
    
def resultado_excel(quant_experimentos, N):
    """
    Funcao que passa os resultados para um arquivo .txt
    em formato proprio para excel
    """
    print('convertendo dados...')
    mediaPop = open(join('dados', 'resultadoExcel.txt'), mode='w')
    #exibe valores de taxa dose
    for n_experimentos in range(1, quant_experimentos + 1):
        for f in range(1, N + 1):
            txt = open(join('dados', str(n_experimentos), str(f) + '.txt'), mode='r')
            for linha in txt:
                if 'Melhor Cromossomo:' in linha:
                    melhor = linha.strip('01'+'\t'+'\n'+'Melhor Cromossomo:')
                    break
            mediaPop.write(melhor+'\t')
            txt.close()
        mediaPop.write('\n')
    mediaPop.write('\n\n')
    #exibe a viabilidade dos resultados
    for n_experimentos in range(1, quant_experimentos + 1):
        for f in range(1, N + 1):
            txt = open(join('dados', str(n_experimentos), str(f) + '.txt'), mode='r')
            for linha in txt:
                if 'Melhor Cromossomo:' in linha:
                    melhor = linha[len(linha) - 2]
                    break
            mediaPop.write(melhor+'\t')
            txt.close()
        mediaPop.write('\n')
    mediaPop.close()
    
def gera_populacao_inicial(cromossomo, tam_populacao):
    # Nova populacao (genoma)
    populacao = []
    populacao.append(cromossomo)
    achou = False
    for _ in range(tam_populacao):
        while not achou:
            cromossomo_mutado = embaralhar(deepcopy(cromossomo))
            cromossomo_mutado.funcao_avaliacao()
            if cromossomo_mutado.score[1] == 0:
                achou = True
        populacao.append(cromossomo_mutado)
        cromossomo_mutado = None
        achou = False
    
    return populacao

def gera_TMax_TMin(populacao, prob_inicial, prob_final):
    """
    Funcao que retorna temperaturas inicial e final
    de acordo com as probabilidades inicial e final
    desejadas.
    O valor retornado e uma lista com dois valores,
    sendo o primeiro valor a temperatura inicial
    e o segundo valor a temperatura final
    """
    temperaturas = []
    # execultar o calculo de aptidao / func avaliacao #
    for cromossomo in populacao:
        cromossomo.funcao_avaliacao()
    
    deltas = []
    for a in populacao:
        for b in populacao:
            if populacao.index(a) < populacao.index(b):
                deltas.append(math.fabs(a.score[0] - b.score[0]))
                
    soma = 0
    for num in deltas:
        soma = soma + num

    media = soma / len(deltas)
    temperaturas.append(-media/math.log(prob_inicial))
    temperaturas.append(-media/math.log(prob_final))
    return temperaturas

def gera_alfa(T_Min, T_Max, epocas):
    return math.pow((T_Min / T_Max), (1 / (epocas - 1)))

def log_resultado(f, i, n_evolucao, experimento, cromossomo):
    
    if not os.path.exists(join('dados', str(n_evolucao), str(f))):  # cria a pasta, se necessario
        os.makedirs(join('dados', str(n_evolucao), str(f)))
        
    log = open(join('dados', str(n_evolucao), str(f), 'log_cromossomo_'+ i +'.txt'), mode='w')
    #log = open(''+'log_cromossomo'+ i +'.txt', mode='w')
    vetor_x = []
    vetor_y = []
    vetor_taxa_dose = []
    vetor_raio = []
    vetor_id = []
    
    log.write(experimento+'\n\n')
        
    for fonte in cromossomo.fontes:
        vetor_id.append(fonte.identificador)
        vetor_x.append(fonte.x)
        vetor_y.append(fonte.y)
        vetor_taxa_dose.append(fonte.taxa_dose)
        vetor_raio.append(fonte.raio)
            
    for iden in vetor_id:
        log.write(str(iden) + '\t')
    log.write('\n\n')
    for x in vetor_x:
        log.write(str(x) + '\t')
    log.write('\n\n')
    for y in vetor_y:
        log.write(str(y) + '\t')
    log.write('\n\n')
    for taxa_dose in vetor_taxa_dose:
        log.write(str(taxa_dose) + '\t')
    log.write('\n\n')
    for raio in vetor_raio:
        log.write(str(raio) + '\t')
    log.write('\n')

def desenha_cromossomo(titulo, cromossomo):
    canvas = np.ones((900, 900, 3)) * 255 #imagem 400x300, com fundo branco e 3 canais para as cores
    #cores
    #verde = (0, 255, 0)
    #azul = (255, 0, 0)
    preto = (0, 0, 0)
    
    #desenha a borda 
    cv2.rectangle(canvas, (100, 100), (800, 800), preto, 2)

    for fonte in cromossomo.fontes:
        #desenha as fontes
        valorR = (fonte.taxa_dose / 10) * 255
        valorR = 255 - valorR
        cor = (0, valorR, 255)
        cv2.circle(canvas, (round(fonte.x * 100 + 100), round(fonte.y * 100 + 100)), round(fonte.raio * 100), cor, -1)
        
    #cv2.imshow(titulo, canvas)
    nome_arquivo = join('dados', 'teste', 'pasta', titulo + '.png')
    cv2.imwrite(nome_arquivo, canvas)
    cv2.waitKey(100)