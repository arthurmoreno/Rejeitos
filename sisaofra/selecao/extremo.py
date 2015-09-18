# coding: utf-8
from sisaofra.modelo.Cromossomo import Cromossomo
def extremo(populacao, n_melhores, metodo=min):
    """ Funcao de Selecao por extremo.
    
    Retorna uma lista com os n_melhores melhores cromossomos da populacao.
    
    :type populacao: list
    :type n_melhores: int
    :type metodo: builtin function (default: min)
    
    FIXME: E preciso validar se n_melhores � menor ou igual a len(genoma)
    (n_melhores <= populacao.__len__)
    """
    
    semColisao = []
    comColisao = []
    lista_melhores = []
    
    for cromossomo in populacao:
        if cromossomo.score[1] == 0:
            semColisao.append(cromossomo.score[0])
        else:
            comColisao.append(cromossomo.score[0])
            
    for _ in range(n_melhores):
        if len(semColisao) > 0:
            for cromossomo in populacao:
                if cromossomo.score[0] == metodo(semColisao):
                    lista_melhores.append(cromossomo)
                    semColisao.remove(metodo(semColisao))
                    populacao.remove(cromossomo)
                    break
        elif len(comColisao) > 0:
            for cromossomo in populacao:
                if cromossomo.score[0] == metodo(comColisao):
                    lista_melhores.append(cromossomo)
                    comColisao.remove(metodo(comColisao))
                    populacao.remove(cromossomo)
                    break
            
    return lista_melhores
    """ codigo antigo - sem sobreposicao de fontes
    
    scores = []
    
    # Preenche uma lista com todos os scores do genoma
    for cromossomo in populacao:
        scores.append(cromossomo.score[0])
    
    for _ in range(n_melhores):
        # Varre a populacao em busca do melhor cromossomo pelo minimo score
        for cromossomo in populacao:
            if cromossomo.score == metodo(scores):
                lista_melhores.append(cromossomo)
                scores.remove(metodo(scores))
                populacao.remove(cromossomo)
                break
    return lista_melhores
    """