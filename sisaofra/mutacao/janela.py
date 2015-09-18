from random import randint, uniform

from sisaofra.constantes import coordenadas
from sisaofra.selecao.extremo import extremo


def janela(populacao, janela, randomizar_janela=False, n_elementos_mutados=0):
    """ Mutador atraves do algoritmo janela
    
    Este metodo faz a troca das posicoes das fontes segundo uma janela.
    Se randomizar_janela for 'False' o valor da janela nao sofre alteracoes.
    Caso contrario, o valor pode variar randomicamente entre 1 e o tamanho da janela.
    
    :param populacao: list de 'Crommossomos'
    :param janela: int
    :param randomizar_janela: bool (default: False)
    :param n_elementos_mutados: int (default: 0) quantidade de elementos a serem mutados
    
    FIXME: O valor da janela deve ser menor ou igual ao tamanho do cromossomo
    """
    
    populacao_mutada = []
    i = 0
    for _ in range(n_elementos_mutados):
        populacao_mutada.append(populacao[i])
        i += 1
        if(i >= len(populacao)):
            i = 0
            
    #populacao_mutada = extremo(populacao, n_elementos_mutados, min)
    for cromossomo in populacao_mutada:
        if randomizar_janela:
            n_janela = randint(1, janela) # garantia de variedade na populacao
        
        
        vetor_posicoes = [] # Vetor com todas as posicoes das fontes
        for fonte in cromossomo:
            vetor_posicoes.append([round(fonte.x),round(fonte.y)])
        
        """
        vetor_posicoes = coordenadas()
        verifica = vetor_posicoes
        """
        
        for i in range(len(vetor_posicoes)): # Aplicacao da tecnica janela
            if i+n_janela < len(vetor_posicoes):
                vetor_posicoes[i][0], vetor_posicoes[i+n_janela][0] = vetor_posicoes[i+n_janela][0] + uniform(-0.05, 0.05), vetor_posicoes[i][0] + uniform(-0.05, 0.05)
                vetor_posicoes[i][1], vetor_posicoes[i+n_janela][1] = vetor_posicoes[i+n_janela][1] + uniform(-0.05, 0.05), vetor_posicoes[i][1] + uniform(-0.05, 0.05)
            else: break
        
        # Insere o vetor de posicoes no cromossomo
        i = 0
        for fonte in cromossomo:
            fonte.x = vetor_posicoes[i][0]
            fonte.y = vetor_posicoes[i][1]
            i += 1
    return populacao_mutada