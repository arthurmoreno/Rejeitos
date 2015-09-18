from random import randrange
from sisaofra.selecao.extremo import extremo

def roleta(populacao, p_melhores=30):
    
    n_elementos = int((len(populacao) * p_melhores) / 100)
    ''' TODO: Lancar uma excecao caso:
        se p_melhores > 100
        se p_melhores <=0
        se n_elementos <= 0
    '''
    #com os sem sobreposicao na frente
    populacao_ordenada = extremo(populacao, len(populacao))
    
    # pesos
    pesos = []
    for i in range(len(populacao_ordenada)):
        pesos.append(randrange(1, 10) * i + 1)
    
    # roleta
    selecionados = []
    while len(selecionados) < n_elementos:
        for i in range(len(populacao_ordenada)):
            if pesos[i] == min(pesos):
                selecionados.append(populacao_ordenada[i])
                pesos[i] = max(pesos)
    
    return selecionados
